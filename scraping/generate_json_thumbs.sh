#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace
shopt -s globstar
shopt -s extglob

if [[ $# -ne 2 ]] ; then
    echo "Script that extracts text and creates a PNG thumbnail for each slide"
    echo "and saves those with a new UUID filename."
    echo
    echo "Usage: $0 <scraped_pdf_directory> <output_directory>"
    echo
    echo "Example: $0 /tmp/scraped_pdfs ./out"
    exit 1
fi

indir="$1"
outdir="$2"

rm -rf $outdir
mkdir -p $outdir
tmpdir=$(mktemp -d)
trap 'rm -r $tmpdir' EXIT
errorfiles=()

for file in $indir/**/*.pdf; do
    echo "$file"
    url="https://www.inf.ed.ac.uk/${file#$indir/}"

    if ! fulltext="$(pdftotext "$file" -)"; then
        echo "error: extracting text failed"
        errors+=("$file")
        continue
    fi

    IFS=$'\f' read -d '' -r -a text <<< "${fulltext%$'\f'}" || true
    pdftoppm -png -scale-to 256 "$file" "$tmpdir/img"
    pages=${#text[@]}

    for j in "${!text[@]}"; do
        i=$((j+1))
        uuid=$(uuidgen)
        title="${file//+(*\/|.*)} $i"

        jq -n --arg title "$title" --arg content "${text[j]}" --arg url "$url#page=$i" \
            '{title: $title, content: $content, type: "slide", url: $url}' > "$outdir/$uuid.json"

        mv "$tmpdir/img-$(printf "%0${#pages}d" $i).png" "$outdir/$uuid.png"
    done

    unset text
done

echo "finished: ${#errors[@]} errors:"
printf '%s\n' "${errors[@]}"
