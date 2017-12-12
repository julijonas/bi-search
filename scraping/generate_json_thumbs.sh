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

    mapfile -d $'\f' -O 1 -t text <<< "${fulltext%$'\f'}"
    pdftoppm -png -scale-to 256 "$file" "$tmpdir/img"
    pages=${#text[@]}

    for i in "${!text[@]}"; do
        uuid=$(uuidgen)
        title="${file//+(*\/|.*)} $i"

        jq -n --arg title "$title" --arg url "$url" --arg uuid "$uuid" --arg text "${text[i]}" \
            '{title: $title, url: $url, uuid: $uuid, text: $text}' > "$outdir/$uuid.json"

        mv "$tmpdir/img-$(printf "%0${#pages}d" $i).png" "$outdir/$uuid.png"
    done

    unset text
done

echo "finished: ${#errors[@]} errors:"
printf '%s\n' "${errors[@]}"
