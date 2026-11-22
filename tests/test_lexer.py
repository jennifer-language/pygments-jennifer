# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: Copyright (C) 2026 mplx <mplx@jennifer-lang.dev>
"""Tests for the installed plugin: discovery, tokens, content detection."""

import os

import pytest
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import (
    find_lexer_class_by_name,
    get_lexer_by_name,
    get_lexer_for_filename,
    get_lexer_for_mimetype,
    guess_lexer,
)
from pygments.token import Error, Token

from pygments_jennifer import JenniferLexer

HERE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def render(src):
    """The format of example.tokens (see jennifer/editors/pygments/golden.py)."""
    return "".join(
        "%-32s %s\n" % (repr(val), str(tok)[len("Token."):])
        for tok, val in JenniferLexer().get_tokens(src)
    )


def test_found_by_alias():
    assert isinstance(get_lexer_by_name("jennifer"), JenniferLexer)
    assert find_lexer_class_by_name("jennifer") is JenniferLexer


def test_found_by_filename_and_mimetype():
    # Objective-J claims `*.j` too: the priority wins without source, the
    # content with it.
    assert isinstance(get_lexer_for_filename("main.j"), JenniferLexer)
    assert isinstance(get_lexer_for_filename("main.j", read("example.j")),
                      JenniferLexer)
    assert isinstance(get_lexer_for_mimetype("text/x-jennifer"), JenniferLexer)


def test_golden_tokens():
    assert render(read("example.j")) == read("example.tokens")


def test_no_error_tokens():
    toks = list(JenniferLexer().get_tokens(read("example.j")))
    assert [v for t, v in toks if t in Error] == []


def test_text_round_trips():
    src = read("example.j")
    assert "".join(v for _, v in JenniferLexer().get_tokens(src)) == src


@pytest.mark.parametrize("src", [
    "#!/usr/bin/env -S jennifer run\nio.printf(\"hi\\n\");\n",
    "# pragma-jennifer-version: >=0.27.0\nuse io;\n",
])
def test_guessed_from_content(src):
    assert isinstance(guess_lexer(src), JenniferLexer)


def test_analyse_text_scores():
    assert JenniferLexer.analyse_text("use io;\n") == 0.5
    assert JenniferLexer.analyse_text("def x as int init 1;\n") == 0.3
    assert JenniferLexer.analyse_text("print('hello')\n") == 0.0


@pytest.mark.parametrize("src, want", [
    ('"a{$x + {1: 2}[1]}b"',
     [(Token.Literal.String.Double, '"'), (Token.Literal.String.Double, "a"),
      (Token.Literal.String.Interpol, "{")]),
    ("$s.to", [(Token.Name.Variable, "$s"), (Token.Punctuation, "."),
               (Token.Name.Property, "to")]),
    ("def maybe as null;", [(Token.Name, "maybe")]),
])
def test_snippets(src, want):
    toks = [(t, v) for t, v in JenniferLexer().get_tokens(src)
            if t not in Token.Text.Whitespace]
    for item in want:
        assert item in toks


def test_highlight_html():
    html = highlight("use io;\n", JenniferLexer(), HtmlFormatter())
    assert '<span class="kn">use</span>' in html
