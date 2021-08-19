#!/usr/bin/env python

import re
import argparse


class CheckFasta:
    def __init__(self) -> None:
        self.error_count = 0

    def load_fasta(self, path_fasta: str):
        with open(path_fasta, mode="rt") as fin:
            fasta = fin.read()

        return fasta

    def error(self, message: str, terminate: bool = False):
        self.error_count = self.error_count + 1
        print(f"ERROR {self.error_count:02d}: {message}")
        if terminate:
            exit(1)
        return False

    def check_filename(self, filename: str):
        if not filename.endswith(".fa"):
            return self.error("The file extension must be .fa")
        return True

    def check_header(self, fasta: str):
        lines = fasta.splitlines()

        if not lines[0].startswith(">"):
            return self.error("The header must start with the `>` character.")

        match = re.search(r"^>\s+[\w\d]+$", lines[0])
        if match:
            return self.error("There must be no whitespaces after the `>` character.")

        return True

    def check_multiline(self, fasta: str):
        # skip the first line
        lines = fasta.splitlines()[1:]
        if len(lines) > 1:
            return self.error("The entire sequence must be in one line.")
        return True

    def check_empty_line(self, fasta: str):
        lines = fasta.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                return self.error("There must be no empty lines.")
        return True

    def check_last_character(self, fasta: str):
        if fasta[-1] != "\n":
            return self.error("The sequence must end with a newline character.")
        return True

    def run_all_tests(self, path_fasta) -> int:

        self.error_count = 0

        fasta = self.load_fasta(path_fasta)

        print(fasta)

        self.check_filename(path_fasta)

        self.check_header(fasta)

        self.check_multiline(fasta)

        self.check_empty_line(fasta)

        self.check_last_character(fasta)

        return self.error_count


def main(path_fasta):

    cf = CheckFasta()
    errs = cf.run_all_tests(path_fasta)

    if errs == 0:
        print("PASSED!")
        exit(0)
    else:
        print("FAILED!")
        exit(1)


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fasta",
        action="store",
        dest="path_fasta",
        help="path to fasta file",
        required=True,
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    main(params.path_fasta)
