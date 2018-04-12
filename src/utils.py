import re

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
    return key in form and form[key].strip()