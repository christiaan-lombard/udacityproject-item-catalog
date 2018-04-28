import re

"""Some application utility functions"""


def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    From: http://blog.dolphm.com/slugify-a-string-in-python/
    """
    s = s.lower()
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')

    return s


def form_has(form, key):
    """Convenience function for checking whether a form
    request contains a non-empty attribute

    Arguments:
        form (werkzeug.datastructures.MultiDict) -- The form request dictionary
        key (string) -- The dictionary key to check

    Returns:
        boolean -- Whether the attribute exists and is non-empty
    """

    return key in form and form[key].strip()
