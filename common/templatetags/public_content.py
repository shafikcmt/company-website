"""Public-content validation for optional CMS links."""
from django import template
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

register = template.Library()
_validate_social_url = URLValidator(schemes=["http", "https"])


@register.filter
def public_social_url(value):
    """Keep configured web URLs intact; omit blank, placeholder or invalid links."""
    if not isinstance(value, str) or not value:
        return ""
    try:
        _validate_social_url(value)
    except ValidationError:
        return ""
    return value
