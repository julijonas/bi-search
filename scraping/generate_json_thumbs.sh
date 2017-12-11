#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace
shopt -s globstar
shopt -s extglob

indir=teaching
outdir=out

rm -rf $outdir
mkdir -p $outdir
tmpdir=$(mktemp -d)
trap 'rm -r $tmpdir' EXIT
errorfiles=()

for file in $indir/**/*.pdf; do
    echo "$file"
    url="https://www.inf.ed.ac.uk/$file"

    if ! fulltext="$(pdftotext "$file" -)"; then
        echo "error: extracting text failed"
        errors+=("$file")
        continue
    fi

    mapfile -d $'\f' -O 1 -t text <<< "${fulltext%$'\f'}"
    pdftoppm -png -scale-to 256 "$file" "$tmpdir/img"
    pages=${#text[@]}

    for i in "${!text[@]}"; do
        uuid=$(uuidgen)
        title="${file//+(*\/|.*)} $i"

        printf '{"title":"%s","url":"%s","uuid":"%s","text":"%s"}\n' "$title" "$url" "$uuid" "${text[i]}" > "$outdir/$uuid.json"

        mv "$tmpdir/img-$(printf "%0${#pages}d" $i).png" "$outdir/$uuid.png"
    done

    unset text
done

echo "finished: ${#errors[@]} errors:"
printf '%s\n' "${errors[@]}"
