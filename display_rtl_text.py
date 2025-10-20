
#!/usr/bin/env python3
"""
bidi_wrap.py

Helper for displaying mixed Hebrew/English text in Textual’s Tree (or any Rich
widget) without mirrored RTL lines.

Method:
1. Keep the text in logical order.
2. Word‑wrap with ICU BreakIterator so words aren’t split.
3. Prepend/append Unicode direction‑isolate marks so Rich’s branch prefix
   can’t flip the line’s direction.

Requires: pip install PyICU  (and libicu-dev on Linux).
"""

from typing import List
import shutil
import unicodedata
from icu import BreakIterator, Locale

# Direction‑isolate marks
LRI = "\u2066"   # Left‑to‑Right Isolate
RLI = "\u2067"   # Right‑to‑Left Isolate
PDI = "\u2069"   # Pop Directional Isolate


def _first_strong_dir(s: str) -> str:
    """Return 'L' or 'R' based on the first strong bidi character."""
    for ch in s:
        cls = unicodedata.bidirectional(ch)
        if cls in ("R", "AL"):
            return "R"
        if cls == "L":
            return "L"
    return "L"


def _word_wrap(text: str, width: int) -> List[str]:
    """Wrap logical text without splitting words."""
    bi = BreakIterator.createWordInstance(Locale("he"))
    bi.setText(text)

    lines, current, cur_len = [], [], 0
    start = bi.first()

    for end in bi:  # BreakIterator is iterable
        word = text[start:end]
        wlen = len(word)

        if current and cur_len + wlen > width:
            lines.append("".join(current).rstrip())
            current, cur_len = [word], wlen
        else:
            current.append(word)
            cur_len += wlen

        start = end

    if current:
        lines.append("".join(current).rstrip())

    return lines


def _wrap_line(line: str) -> str:
    """Protect one line with isolate marks."""
    return (RLI if _first_strong_dir(line) == "R" else LRI) + line + PDI


def get_text_as_lines(text: str, term_width: int) -> List[str]:
    """
    Convert logical text into isolate‑fenced, word‑wrapped lines.

    Parameters
    ----------
    text : str         Logical‑order input (may contain '\n').
    term_width : int   Max visual width per line (excluding isolates).

    Returns
    -------
    List[str]          Ready‑to‑print lines.
    """
    if text.startswith("https://"):
        # URLs are not split, so they can be copy/paste into the browser
        return [ text ]
    if term_width <= 0:
        raise ValueError("term_width must be > 0")

    out: List[str] = []
    for paragraph in text.splitlines():
        for line in _word_wrap(paragraph, term_width):
            out.append(_wrap_line(line))
    return out

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



def send_to_terminal(text: str) -> None:
    """
    Renders visually-correct RTL text to the terminal.
    Note: Currently in use only by mivzakim_cli
    Args:
        text (str): Text content to display.
    """
    term_width = shutil.get_terminal_size((80, 20)).columns
    lines = get_text_as_lines(text, term_width)
    for line in lines:
        # The code below fixes the issue of, for example. dot at the end of line appearing at the start
        start_of_line_natrual_chars = ""
        while line and get_char_type(line[0]) == "natrual":
            start_of_line_natrual_chars += line[0]
            line = line[1:]
            end_of_line_natrual_chars = ""
        while line and get_char_type(line[-1]) == "natrual":
            end_of_line_natrual_chars += line[-1]
            line = line[:-1]
        line = end_of_line_natrual_chars + line + start_of_line_natrual_chars
        print(line)


if __name__ == "__main__":
    sample = ( "אבג")
    for l in get_text_as_lines(sample, 50):
        print(l)
