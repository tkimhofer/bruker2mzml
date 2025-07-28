#!/usr/bin/env python3

"""
Bruker MS data extractor.

Converts Bruker .d folders into pickled Python data using the baf_reader library.
Supports metadata ("meta") or spectral extraction ("edata").
"""

import sys
import argparse
import logging
from pathlib import Path

# Load shared object (Bruker wrapper) from local path
sys.path.append('/app/linux64')
from baf_reader import Exp1


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Pickle Bruker MS data using baf_reader.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'extraction', type=str, choices=['meta', 'edata'],
        help='Extraction type: "meta" for summary or "edata" for spectral data'
    )
    parser.add_argument(
        'directory', type=str,
        help='Path to Bruker .d directory'
    )
    parser.add_argument(
        '-l', '--mslevel', nargs='+', default=[0],
        help='MS level(s) to extract'
    )
    parser.add_argument(
        '-sm', '--smode', nargs='+', default=[0],
        help='Scan mode(s)'
    )
    parser.add_argument(
        '-am', '--amode', type=int, default=2,
        help='Acquisition mode'
    )
    parser.add_argument(
        '-s', '--segment', nargs='+', default=[3],
        help='Segment(s) to extract'
    )

    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()

    data_dir = Path(args.directory)
    if not data_dir.exists() or not data_dir.is_dir():
        logging.error(f"Directory not found: {args.directory}")
        sys.exit(1)

    logging.info(f"Starting extraction: type={args.extraction}, dir={args.directory}")

    try:
        Exp1(
            fname=args.directory,
            type=args.extraction,
            mslevel=args.mslevel,
            smode=args.smode,
            amode=args.amode,
            seg=args.segment
        )
        logging.info("Extraction completed successfully.")
    except Exception as e:
        logging.exception(f"Extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
