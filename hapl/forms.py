from django import forms
from django.core.validators import FileExtensionValidator

from hapl.models import JobApplication, validate_resume_size


# Shared Tailwind styling so the rendered fields match the rest of the site.
_INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 "
    "focus:border-amber-500 focus:ring-2 focus:ring-amber-500/30 focus:outline-none"
)


class JobApplicationForm(forms.ModelForm):
    """Public-facing application form. Position and status are not exposed:
    position comes from the URL and status defaults to "new"."""

    class Meta:
        model = JobApplication
        fields = (
            "full_name",
            "email",
            "phone",
            "experience_years",
            "cover_letter",
            "resume",
        )
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": _INPUT_CLASS, "placeholder": "Jane Doe"}
            ),
            "email": forms.EmailInput(
                attrs={"class": _INPUT_CLASS, "placeholder": "jane@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": _INPUT_CLASS, "placeholder": "+8801XXXXXXXXX"}
            ),
            "experience_years": forms.NumberInput(
                attrs={"class": _INPUT_CLASS, "step": "0.1", "min": "0", "placeholder": "2.5"}
            ),
            "cover_letter": forms.Textarea(
                attrs={
                    "class": _INPUT_CLASS,
                    "rows": 5,
                    "placeholder": "Tell us why you're a great fit (optional).",
                }
            ),
            "resume": forms.ClearableFileInput(
                attrs={"class": _INPUT_CLASS, "accept": ".pdf,.doc,.docx"}
            ),
        }

    def clean_experience_years(self):
        years = self.cleaned_data["experience_years"]
        if years is not None and years < 0:
            raise forms.ValidationError("Years of experience cannot be negative.")
        return years

    def clean_resume(self):
        """Mirror the model's extension + size constraints with friendly errors."""
        resume = self.cleaned_data.get("resume")
        if not resume:
            return resume
        # Only validate a freshly uploaded file (has size); skip if unchanged.
        if hasattr(resume, "size"):
            FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])(resume)
            validate_resume_size(resume)
        return resume
