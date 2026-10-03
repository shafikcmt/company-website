import io
from unittest.mock import patch

from django.db import models, connection, transaction
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.test import TransactionTestCase
from django.test.utils import isolate_apps
from PIL import Image

from common.fields import OptimizedImageField
from tests.storage_helpers import disposable_storage


@isolate_apps()
class ImageRetentionTests(TransactionTestCase):
    """Use isolated test tables/storage, never application media or live records."""

    def setUp(self):
        self.directory = disposable_storage('hapl-image-test-')
        self.storage = FileSystemStorage(location=self.directory.__enter__())
        self.addCleanup(self.directory.__exit__, None, None, None)
        storage = self.storage

        class Photo(models.Model):
            image = OptimizedImageField(upload_to='photos/', storage=storage, max_dimensions=(1920, 1440), blank=True)

            class Meta:
                app_label = 'common'

        self.Photo = Photo
        with connection.schema_editor() as editor:
            editor.create_model(Photo)
        self.addCleanup(self.drop_table)
        self.photo = Photo.objects.create(image=self.upload('old.png'))
        self.old_name = self.photo.image.name

    def drop_table(self):
        with connection.schema_editor() as editor:
            editor.delete_model(self.Photo)

    def upload(self, name):
        stream = io.BytesIO()
        Image.new('RGB', (120, 80), 'navy').save(stream, 'PNG')
        return ContentFile(stream.getvalue(), name=name)

    def test_successful_replacement_retains_old_and_new_optimized_files(self):
        self.photo.image = self.upload('new.png')
        self.photo.save()
        self.assertNotEqual(self.old_name, self.photo.image.name)
        for name in [self.old_name, self.photo.image.name]:
            self.assertTrue(self.storage.exists(name))
            with self.storage.open(name) as image_file, Image.open(image_file) as image:
                self.assertEqual(image.format, 'WEBP')
                self.assertEqual(image.size, (120, 80))

    def test_replacement_rollback_keeps_restored_database_reference_readable(self):
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                self.photo.image = self.upload('replacement.png')
                self.photo.save()
                raise RuntimeError('Rollback')
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.image.name, self.old_name)
        self.assertTrue(self.storage.exists(self.old_name))

    def test_failed_save_keeps_old_file(self):
        self.photo.image = self.upload('failed.png')
        with patch.object(self.Photo, '_save_table', side_effect=RuntimeError('Database failure')):
            with self.assertRaises(RuntimeError):
                self.photo.save()
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.image.name, self.old_name)
        self.assertTrue(self.storage.exists(self.old_name))

    def test_clear_rollback_preserves_database_reference_and_file(self):
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                self.photo.image = ''
                self.photo.save()
                raise RuntimeError('Rollback clear')
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.image.name, self.old_name)
        self.assertTrue(self.storage.exists(self.old_name))

    def test_ordinary_save_does_not_reprocess_committed_image(self):
        with patch('common.fields.ImageOptimizer.optimize_image') as optimize:
            self.photo.save()
        optimize.assert_not_called()
        self.assertEqual(self.photo.image.name, self.old_name)
        self.assertTrue(self.storage.exists(self.old_name))

    def test_clear_and_delete_never_delete_a_shared_file(self):
        other = self.Photo.objects.create(image=self.old_name)
        self.photo.image = ''
        self.photo.save()
        self.assertTrue(self.storage.exists(self.old_name))
        self.photo.delete()
        self.assertTrue(self.storage.exists(self.old_name))
        other.delete()
        self.assertTrue(self.storage.exists(self.old_name))

    def test_delete_rollback_preserves_file(self):
        pk = self.photo.pk
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                self.photo.delete()
                raise RuntimeError('Rollback deletion')
        self.assertEqual(self.Photo.objects.get(pk=pk).image.name, self.old_name)
        self.assertTrue(self.storage.exists(self.old_name))
