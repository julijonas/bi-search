#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace

wget --recursive \
     --level 1 \
     --accept-regex "^http://course.inf.ed.ac.uk/[^/]+/?$" \
     http://course.inf.ed.ac.uk/

grep -ho 'http://www.inf.ed.ac.uk/teaching/courses/[^"<]\+' course.inf.ed.ac.uk/* | sort -uo course_websites.txt

wget --recursive \
    --no-clobber \
    --accept pdf \
    --level inf \
    --no-parent \
    --no-host-directories \
    --input-file course_websites.txt
