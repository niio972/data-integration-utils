
import argparse

import sys

from tools import functions
from tools import log as logger

if sys.version_info[0] < 3:
    raise Exception("Wrong python version, please install python 3.X version")

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str,
                    help="The path of the file or the directory which contains the files to Format",
                    required=True)
parser.add_argument("-o", type=str,
                    help="The path of the directory which will contains the formatted files",
                    required=True)
parser.add_argument("-c", type=str,
                    help="The path of yml vocabulary file",
                    required=True)
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
functions.runReplacing(args)


