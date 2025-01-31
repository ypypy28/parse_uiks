﻿from shutil import which
import argparse
import signal
import sys

from parsix import __doc__ as description
from parsix import main, __version__
from parsix.config import REGIONS, OUTPUT_DIR_NAME, SHOW_CHROME


def exit_gracefully(signal, frame):
    print("\nProgram was interrupted")
    sys.exit(1)


def start():

    signal.signal(signal.SIGINT, exit_gracefully)
    if not which('chromedriver'):
        print("You need to install chromedriver, "
              "download it from here https://chromedriver.chromium.org/home")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        prog="parsix",
        description=description,
    )
    parser.add_argument("--output-dir", "-o", default=OUTPUT_DIR_NAME, nargs='?',
                        help="path to the directory where to put results")
    parser.add_argument("--show-chrome", default=SHOW_CHROME, action="store_true",
                        help="use to display Chrome window while parsing initial page")
    parser.add_argument("--version", "-v", action="version",
                        version=f'%(prog)s {__version__}')
    parser.add_argument("--region", "-r", required=True,
                        choices=REGIONS,
                        help="which regions to work with")

    args = parser.parse_args()

    main.run(region=args.region,
             out_dir=args.output_dir,
             show_chrome=args.show_chrome)


if __name__ == "__main__":
    start()
