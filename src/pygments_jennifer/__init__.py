# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: Copyright (C) 2026 mplx <mplx@jennifer-lang.dev>
"""Pygments lexer plugin for Jennifer (https://jennifer-lang.dev/).

Installing the package registers the lexer with Pygments under the alias
`jennifer` and the filename `*.j`; nothing needs importing.
"""

from pygments_jennifer.lexer import JenniferLexer

__all__ = ["JenniferLexer"]
__version__ = "0.1.0"
