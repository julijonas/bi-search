import os
import argparse

parser = argparse.ArgumentParser(description='Build the inverted index.')

parser.add_argument(
    '--input',
    dest='input',
    default=None,
    type=str,
    required=False,
    help='Location of the scrape (where all the .json and .png files). Defaults to the value of the TTDS_SCRAPE_LOCATION environment variable.'
)

parser.add_argument(
    '--output',
    dest='output',
    default=None,
    type=str,
    required=False,
    help='Where you want the inverted index files to be stored (overwrites existing files). Defaults to the value of the TTDS_INDEX_LOCATION environment variable.'
)

args = parser.parse_args()

if args.input is None:
    if "TTDS_SCRAPE_LOCATION" not in os.environ:
        print("Input location not specified and the TTDS_SCRAPE_LOCATION environment variable is not defined!")
        exit(1)
    else:
        args.input = os.environ.get("TTDS_SCRAPE_LOCATION")

if args.output is None:
    if "TTDS_INDEX_LOCATION" not in os.environ:
        print("Output location not specified and the TTDS_INDEX_LOCATION environment variable is not defined!")
        exit(1)
    else:
        args.output = os.environ.get("TTDS_INDEX_LOCATION")

print(args)

from indexing import build_index

build_index(args.input, args.output, silent=False)
