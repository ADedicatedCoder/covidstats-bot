import re


def keepEmojis(message):
    regex1 = r":[^:\s]+:|<:[^:\s]+:[0-9]+>|<:a:[^:\s]+:[0-9]+>"
    regex2 = r"\s+"
    subst = ""
    result1 = re.sub(regex1, subst, message)
    result2 = re.sub(regex2, subst, result1)
    if result2:
        return 1
    else:
        return 0
