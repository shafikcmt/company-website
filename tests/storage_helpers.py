import shutil
from contextlib import contextmanager
from uuid import uuid4

from django.conf import settings


@contextmanager
def disposable_storage(prefix):
    # Python 3.14's Windows TemporaryDirectory ACL excludes the sandbox user.
    # Normal mkdir inherits the workspace ACL, and stays inside ignored tmp/.
    parent = (settings.BASE_DIR / 'tmp').resolve()
    root = parent / (prefix + uuid4().hex)
    root.mkdir(parents=True)
    try:
        yield str(root)
    finally:
        if root.resolve().parent != parent:
            raise RuntimeError('Refusing to remove storage outside the test directory')
        shutil.rmtree(root)
