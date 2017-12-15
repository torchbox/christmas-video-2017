import re

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim='-'):
    """Generates ASCII-only slug without digits."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = ''.join([i for i in word if i.isalpha()])
        if word:
            result.append(word)
    return str(delim.join(result))
