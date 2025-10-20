import uuid
from django.utils.text import slugify

# Generate a unique code with optional prefix
def generate_unique_code(prefix='', length=8):

    unique_id = str(uuid.uuid4()).replace('-', '')[:length].upper()
    return f"{prefix}{unique_id}" if prefix else unique_id


# Generate a slug from text
def generate_slug(text):
    return slugify(text)


# Calculate percentage
def calculate_percentage(part, whole):
    if whole == 0:
        return 0
    return round((part / whole) * 100, 2)
