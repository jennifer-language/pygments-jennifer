# pygments-jennifer

A [Pygments](https://pygments.org) lexer for [Jennifer](https://jennifer-lang.dev/),
packaged as a plugin. Once installed, Pygments highlights Jennifer wherever it
is used: `pygmentize`, Sphinx, MkDocs, Jupyter, and any other tool built on
it. Pygments takes new languages as plugins until they have a community of
their own; this is that plugin.

## Install

Until the package is on PyPI, install it from the repository:

```sh
pip install git+https://github.com/jennifer-language/pygments-jennifer.git
```

Needs Python 3.9 or newer and Pygments 2.13 or newer, the first release that
loads plugins through `importlib.metadata`. Install it into the same
environment as the tool that runs Pygments (the Sphinx or MkDocs virtualenv,
say).

## Use

The lexer registers the alias `jennifer`, the filename pattern `*.j` and the
MIME type `text/x-jennifer`:

```sh
pygmentize -l jennifer main.j          # by alias
pygmentize main.j                      # by file name
pygmentize -f html -O full -o main.html main.j
```

In Markdown for MkDocs (with `pymdownx.highlight`) or in Sphinx's MyST, fence
code as ```` ```jennifer ````. In reStructuredText:

```rst
.. code-block:: jennifer

   use io;
   io.printf("hello\n");
```

From Python:

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

html = highlight(source, get_lexer_by_name("jennifer"), HtmlFormatter())
```

`guess_lexer` recognises Jennifer by a `#!... jennifer` first line or a
`# pragma-jennifer-version:` header, which extensionless scripts carry, and
less surely by a `use name;` line.

Pygments' built-in Objective-J lexer claims `*.j` as well. With this plugin
installed, a `.j` file name alone selects Jennifer; when Pygments also sees
the source, it picks whichever lexer recognises the content, so an Objective-J
file with its `@import` lines still goes to Objective-J.

## What it highlights

The same token classes as the other Jennifer editor definitions: keywords and
type keywords, `$` variables, `UPPER_CASE` constants, `CamelCase` types,
`name(` calls, `ns.name` with the prefix as a namespace (and the name after
`use` or an alias), keyword-spelled names after a `.` or in a field position,
`#` comments, nested `/* */` comments, `/** */` docblocks with `@tags`,
`# pragma-jennifer-...:` and `# lint-disable:` directives, raw `'...'` and
cooked `"..."` strings with escapes and `{expr}` slots, and the numeric
forms.

## Development

The lexer is maintained in the interpreter repository, at
[`editors/pygments/`](https://github.com/jennifer-language/jennifer/tree/main/editors/pygments),
where it is checked against the interpreter's own lexer over every Jennifer
source file in the project. `src/pygments_jennifer/lexer.py`,
`tests/example.j` and `tests/example.tokens` are byte-for-byte copies of the
files there. Change them there, then:

```sh
tools/sync.sh            # copy from a sibling checkout ../jennifer
tools/sync.sh --check    # what CI runs
python -m pip install -e ".[test]" && python -m pytest
```

## License

BSD-2-Clause, like Pygments. See [LICENSE](LICENSE).
