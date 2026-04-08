import pytest
from bidi.algorithm import get_display
import builtins
import types

import sys
sys.path.insert(0, "..")
import display_heb_on_term as mod

def test_get_char_type():
    assert mod.get_char_type('א') == "RTL"
    assert mod.get_char_type('A') == "LTR"
    assert mod.get_char_type('z') == "LTR"
    assert mod.get_char_type('1') == "LTR"
    assert mod.get_char_type(':') == "natrual"
    assert mod.get_char_type('@') == "natrual"
    assert mod.get_char_type('~') == "natrual"
    assert mod.get_char_type('\u202B') == "natrual"

def test_is_next_seq_is_RTL():
    assert mod.is_next_seq_is_RTL("abc", 1) is False
    assert mod.is_next_seq_is_RTL("123 ABC אבג", 6) is True
    assert mod.is_next_seq_is_RTL("אבג ABC", 0) is True
    assert mod.is_next_seq_is_RTL("... ---", 0) is False  # all neutral

def test_reverse_LTR():
    input_text = "abc אבג 123"
    reversed_text = mod.reverse_LTR(input_text)
    assert "cba" in reversed_text
    assert "321" in reversed_text
    assert "אבג" in reversed_text

    ltr = "אבג"
    rtl = "abc"
    nat = "  "
    input_text = ltr + nat + rtl + nat + ltr
    reversed_text = mod.reverse_LTR(input_text)
    assert ltr in reversed_text
    assert not rtl in reversed_text

def test_get_text_as_lines_simple():
    input_text = "abc אבג 123"
    lines = mod.get_text_as_lines(input_text, term_width=40)
    assert isinstance(lines, list)
    assert all(isinstance(line, str) for line in lines)

def test_get_text_as_lines_wrapping():
    input_text = "This is a long line that should wrap around when the terminal width is small. אבג"
    lines = mod.get_text_as_lines(input_text, term_width=30)
    assert len(lines) > 1

def test_send_to_terminal(monkeypatch):
    output = []
    monkeypatch.setattr(builtins, "print", lambda s: output.append(s))
    mod.send_to_terminal("abc אבג def")
    assert any("אבג" in line or "cba" in line for line in output)

def test_display_rtl_on_terminal(monkeypatch):
    output = []
    monkeypatch.setattr(builtins, "print", lambda s: output.append(s))
    mod.display_rtl_on_terminal("abc אבג")
    assert any("אבג" in line or "cba" in line for line in output)
