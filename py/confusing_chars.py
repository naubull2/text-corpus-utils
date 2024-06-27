import unicodedata

def get_confusable_characters():
    # ASCII characters to compare against
    ascii_chars = ''.join(chr(i) for i in range(32, 127))
    
    # Non-standard whitespace characters to compare against
    whitespace_chars = [
        '\u00A0',  # NO-BREAK SPACE
        '\u2000',  # EN QUAD
        '\u2001',  # EM QUAD
        '\u2002',  # EN SPACE
        '\u2003',  # EM SPACE
        '\u2004',  # THREE-PER-EM SPACE
        '\u2005',  # FOUR-PER-EM SPACE
        '\u2006',  # SIX-PER-EM SPACE
        '\u2007',  # FIGURE SPACE
        '\u2008',  # PUNCTUATION SPACE
        '\u2009',  # THIN SPACE
        '\u200A',  # HAIR SPACE
        '\u202F',  # NARROW NO-BREAK SPACE
        '\u205F',  # MEDIUM MATHEMATICAL SPACE
        '\u3000',  # IDEOGRAPHIC SPACE
    ]
    
    # Symbols that resemble plain ASCII symbols
    similar_symbols = {
        '\u00B7': '.',  # MIDDLE DOT
        '\u2212': '-',  # MINUS SIGN
        '\u2022': '*',  # BULLET
        '\u2217': '*',  # ASTERISK OPERATOR
        '\uFF0B': '+',  # FULLWIDTH PLUS SIGN
        '\uFE62': '+',  # SMALL PLUS SIGN
        '\uFF0D': '-',  # FULLWIDTH HYPHEN-MINUS
        '\uFF0F': '/',  # FULLWIDTH SOLIDUS
        '\uFE68': '/',  # SMALL SOLIDUS
        '\uFF1D': '=',  # FULLWIDTH EQUALS SIGN
        '\uFF1A': ':',  # FULLWIDTH COLON
        '\u2236': ':',  # RATIO
        '\u02D0': ':',  # MODIFIER LETTER TRIANGULAR COLON
    }
    
    confusable_chars = {}

    # Check for confusable characters in specified Unicode ranges
    unicode_ranges = [
        (0x00A0, 0x00FF),   # Latin-1 Supplement
        (0x0100, 0x017F),   # Latin Extended-A
        (0x0180, 0x024F),   # Latin Extended-B
        (0x0250, 0x02AF),   # IPA Extensions
        (0x2C60, 0x2C7F),   # Latin Extended-C
        (0xA720, 0xA7FF),   # Latin Extended-D
        (0x1E00, 0x1EFF),   # Latin Extended Additional
        # Add more ranges as necessary
    ]

    for start, end in unicode_ranges:
        for codepoint in range(start, end + 1):
            char = chr(codepoint)
            for ascii_char in ascii_chars:
                if char != ascii_char and unicodedata.normalize('NFKD', char) == ascii_char:
                    confusable_chars[char] = ascii_char
                    break

    # Add whitespace characters
    for ws_char in whitespace_chars:
        confusable_chars[ws_char] = ' '

    # Add similar symbols
    for symbol_char, ascii_symbol in similar_symbols.items():
        confusable_chars[symbol_char] = ascii_symbol

    return confusable_chars

# Usage
confusables = get_confusable_characters()
for unicode_char, ascii_char in confusables.items():
    print(f"Unicode char '{unicode_char}' (U+{ord(unicode_char):04X}) is confusable with ASCII char '{ascii_char}'")

