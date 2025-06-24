#!/usr/bin/env python3

import shutil
import textwrap
from bidi.algorithm import get_display
from typing import List

RTL_START = u'\u202B'
PDF = '\u202C'  # Pop Directional Formatting

def get_char_type(c: str) -> str:
    """
    Determines the character direction type of a given character.

    Args:
        c (str): A single character.

    Returns:
        str: "RTL", "LTR", or "natrual" indicating direction or neutral status.
    """

    o = ord(c)
    if 32 <= o <= 47: return "natrual"
    if 48 <= o <= 57: return "LTR"
    if 58 <= o <= 64: return "natrual"
    if 65 <= o <= 90: return "LTR"
    if 91 <= o <= 96: return "natrual"
    if 97 <= o <= 122: return "LTR"
    if 123 <= o <= 126: return "natrual"
    if 0x5D0 <= o <= 0x5EA: return "RTL"
    return "natrual"

def is_next_seq_is_RTL(text: str, start: int) -> bool:
    """
    Checks whether the next sequence of characters is RTL.

    Args:
        text (str): The full text.
        start (int): The index from which to start checking.

    Returns:
        bool: True if next non-neutral character sequence is RTL, False if LTR.
    """
    i = start + 1
    while i < len(text):
        char_type = get_char_type(text[i])
        i += 1
        if char_type == "natrual":
            continue
        if char_type == "LTR":
            return False
        if char_type == "RTL":
            return True
    return False

def reverse_LTR(text: str) -> str:
    """
    Reverses LTR sequences within mixed-directional text for better RTL rendering.

    Args:
        text (str): The original text.

    Returns:
        str: Text with LTR segments reversed for visual compatibility in RTL contexts.
    """
    t = ""
    LTR_seq = ""
    for idx, c in enumerate(text):
        char_type = get_char_type(c)
        match char_type:
            case "natrual":
                if LTR_seq:
                    if is_next_seq_is_RTL(text, idx):
                        t += LTR_seq[::-1]
                        LTR_seq = ""
                        t += c
                    else:
                        LTR_seq += c
                else:
                    t += c
            case "LTR":
                LTR_seq += c
            case "RTL":
                if LTR_seq:
                    t += LTR_seq[::-1]
                    LTR_seq = ""
                t += c
    if LTR_seq:
        t += LTR_seq[::-1]
    return t

def get_text_as_lines(text: str, term_width: int) -> List[str]:
    """
    Converts a block of text into visually-correct lines for RTL terminal display.

    Args:
        text (str): The original text block.
        term_width (int): Terminal width in characters.

    Returns:
        List[str]: List of formatted lines with proper RTL rendering.
    """
    paragraphs = text.strip().split('\n\n')
    output_lines = []

    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            wrapped_lines = textwrap.wrap(
                line,
                width=term_width,
                break_long_words=False,
                break_on_hyphens=False
            )
            for line in wrapped_lines:
                start_of_line_natrual_chars = ""
                while line and get_char_type(line[0]) == "natrual":
                    start_of_line_natrual_chars += line[0]
                    line = line[1:]
                end_of_line_natrual_chars = ""
                while line and get_char_type(line[-1]) == "natrual":
                    end_of_line_natrual_chars += line[-1]
                    line = line[:-1]

                line = end_of_line_natrual_chars + line + start_of_line_natrual_chars
                visual = get_display(line)
                visual_len = len(visual)
                padding = max(0, term_width - visual_len)
                # Possible improvment: ' ' * padding + RTL_START + visual[::-1] + PDF 
                output_lines.append(' ' * padding + visual[::-1])
        output_lines.append("")
    return output_lines

def send_to_terminal(text: str) -> None:
    """
    Renders visually-correct RTL text to the terminal.

    Args:
        text (str): Text content to display.
    """
    term_width = shutil.get_terminal_size((80, 20)).columns
    lines = get_text_as_lines(text, term_width)
    for line in lines:
        print(line)

def old_send_to_terminal(text: str) -> None:
    """
    Older version of send_to_terminal with inline printing. Maintained for comparison/testing.

    Args:
        text (str): Text content to display.
    """
    term_width = shutil.get_terminal_size((80, 20)).columns
    paragraphs = text.strip().split('\n\n')

    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            wrapped_lines = textwrap.wrap(
                line,
                width=term_width,
                break_long_words=False,
                break_on_hyphens=False
            )
            for line in wrapped_lines:
                start_of_line_natrual_chars = ""
                while line and get_char_type(line[0]) == "natrual":
                    start_of_line_natrual_chars += line[0]
                    line = line[1:]
                end_of_line_natrual_chars = ""
                while line and get_char_type(line[-1]) == "natrual":
                    end_of_line_natrual_chars += line[-1]
                    line = line[:-1]

                line = end_of_line_natrual_chars + line + start_of_line_natrual_chars
                visual = get_display(line)
                visual_len = len(visual)
                padding = max(0, term_width - visual_len)
                print(' ' * padding + visual[::-1])
        print()

def display_rtl_on_terminal(text: str) -> None:
    """
    Processes and displays mixed RTL/LTR text on terminal with proper directionality.

    Args:
        text (str): Input text string to render.
    """
    # Uncomment the below line to debug the same item
    #open("item.txt", 'wb').write(text.encode('utf8'))
    text = reverse_LTR(text)
    send_to_terminal(text)

if __name__ == "__main__":
    text = open("item.txt", 'rb').read().decode('utf8')
    display_rtl_on_terminal(text)
