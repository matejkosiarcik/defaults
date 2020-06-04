from typing import List
import sys
import os
import pathlib
import shutil
import argparse


def main(argv: List[str]):
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--cwd', type=str, help='Path to project')
    parser.add_argument('--defaults', type=str, help='Path to defaults')
    parser.add_argument('--dry-run', action='store_true', default=False, help='Dry run')
    parser.add_argument('--init', action='store_true', default=False, help='Dry run')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Dry run')
    args = parser.parse_args(argv)

    # get source/target directories
    cwd = args.cwd or '.'
    defaults_dir = args.defaults or os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
    dry_run = args.dry_run or False
    init = args.init or False
    verbose = args.verbose or False

    files = [
        '.editorconfig',
        '.markdownlint.json',
        '.remarkrc',
        '.swiftlint.yml',
        '.yamllint.yml',
    ]

    def copy(source: str, target: str):
        if dry_run or verbose:
            print(f'Replace {os.path.basename(filepath)}')
        if not dry_run:
            shutil.copyfile(defaults_filepath, filepath)

    # check all files
    for filename in files:
        filepath = os.path.join(cwd, filename)
        defaults_filepath = os.path.join(defaults_dir, filename)
        assert os.path.isfile(defaults_filepath)

        # if file exists, replace it
        if os.path.isfile(filepath):
            if not init:
                with open(filepath) as file:
                    file_str = file.read()
                with open(defaults_filepath) as default_file:
                    default_str = default_file.read()
                if file_str != default_str:
                    copy(defaults_filepath, filepath)
                elif verbose:
                    print(f'Skip {filename}')
            else:
                copy(defaults_filepath, filepath)


if __name__ == "__main__":
    main(sys.argv[1:])
