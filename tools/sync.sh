#!/bin/sh
# SPDX-License-Identifier: BSD-2-Clause
#
# The lexer, its sample and its golden tokens live in the interpreter
# repository (jennifer/editors/pygments/); this repository carries
# byte-for-byte copies.
#
#   tools/sync.sh            copy them over from a sibling jennifer checkout
#   tools/sync.sh --check    exit 1 if any copy differs
#
# JENNIFER_EDITORS names the source directory; the default is the sibling
# checkout ../jennifer/editors/pygments.
set -eu
cd "$(dirname "$0")/.."

src="${JENNIFER_EDITORS:-../jennifer/editors/pygments}"
if [ ! -d "$src" ]; then
    echo "sync.sh: $src not found (set JENNIFER_EDITORS)" >&2
    exit 2
fi

status=0
pair() {
    from="$src/$1"
    to="$2"
    if [ "${mode:-}" = check ]; then
        if ! cmp -s "$from" "$to"; then
            echo "sync.sh: $to differs from $from" >&2
            status=1
        fi
    else
        cp "$from" "$to"
    fi
}

mode=""
[ "${1:-}" = "--check" ] && mode=check

pair jennifer_lexer.py src/pygments_jennifer/lexer.py
pair example.j tests/example.j
pair example.tokens tests/example.tokens

[ "$mode" = check ] && [ $status = 0 ] && echo "copies match $src"
exit $status
