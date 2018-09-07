import re

TS_EXPR = re.compile(r"^[\[\(]?\d{1,2}\:?\d{2}(\:?\d{2})?(\s*(AM|PM))?[\]\)]?\s*")
MODE_EXPR = re.compile(r"(\<)([\s\@\+])([A-z0-9_-`\\]+\>)")
NICK_FORMAT = re.compile(r"^[\s\@\+]+([A-z0-9_-`\\]+)\s*\|\s*(.*)")


def strip_timestamps(quote):
    # remove timestamps at the start of each line
    lines = []
    for line in quote.split("\n"):
        lines.append(TS_EXPR.sub("", line))
    return "\n".join(lines)


def normalize_nick_format(quote):
    # try to normalize the format in which people's nicks appear
    lines = []
    for line in quote.split("\n"):
        lines.append(NICK_FORMAT.sub(r"<\1> \2", line))
    return "\n".join(lines)


def strip_modes(quote):
    # remove @ + in front of people's nicks
    return MODE_EXPR.sub(r"\1\3", quote)


def normalize_whitespace(quote):
    # replace tabs with spaces
    quote = re.sub(r"\t+", " ", quote)

    # remove windows-style newline characters
    quote = quote.replace("\r", "")

    return quote


def prepare_quote(quote, **kwargs):
    funcs = (strip_timestamps, normalize_nick_format, strip_modes, normalize_whitespace)
    for func in funcs:
        if kwargs.get(func.__name__, True):
            quote = func(quote)
    return quote
