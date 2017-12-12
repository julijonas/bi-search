#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace

if [[ $# -ne 1 ]] ; then
    echo "Script that reads course.inf.ed.ac.uk, finds www.inf.ed.ac.uk/teaching/courses/*"
    echo "URLs and saves PDFs from those."
    echo
    echo "Usage: $0 <output_directory>"
    echo
    echo "Example: $0 /tmp/scraped_pdfs"
    exit 1
fi

outdir="$1"

wget --recursive \
     --level 1 \
     --accept-regex "^http://course.inf.ed.ac.uk/[^/]+/?$" \
     --directory-prefix "$outdir" \
     http://course.inf.ed.ac.uk/

grep -ho 'http://www.inf.ed.ac.uk/teaching/courses/[^"<]\+' "$outdir/course.inf.ed.ac.uk/"* | sort -uo "$outdir/course_websites.txt"

wget --recursive \
    --no-clobber \
    --accept pdf \
    --level inf \
    --no-parent \
    --no-host-directories \
    --input-file "$outdir/course_websites.txt" \
    --directory-prefix "$outdir"
