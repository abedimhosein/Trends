import string
from random import choices


def random_str_generator(size: int = 10, population: str = string.ascii_letters + string.digits):
    return ''.join(choices(population, k=size))


def unique_slug_generator(instance, new_slug: str = None, initial_length: int = 10):
    slug = new_slug or ''
    slug = f"{slug}{random_str_generator(size=initial_length)}"

    is_exists = instance.__class__.objects.filter(slug__iexact=slug).exists()
    if is_exists:
        return unique_slug_generator(instance, new_slug=slug, initial_length=1)
    return slug
