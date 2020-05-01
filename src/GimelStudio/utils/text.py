## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: text.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Provides utility text manipulation functions
## ----------------------------------------------------------------------------


def TruncateText(text_string, str_length=18):
    """ Truncate the text string after a certain 
    number of characters.
    """
    chars = []
    for char in text_string:
        chars.append(char)

    if len(chars) > str_length:
        words = chars[:str_length-1]
        text = ''.join(words)
        return '{}...'.format(text)
    else:
        return text_string