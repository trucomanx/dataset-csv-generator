#!/usr/bin/python3

#!/usr/bin/python

import sys
import os
import signal
import argparse

import dataset_csv_generator.about as about
from dataset_csv_generator.modules.split import generate_train_test_csv


def parse_args():
    prog_name=about.__program_csv_split__
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""
Split a CSV dataset into train and test files using stratified sampling.

This tool preserves the distribution of a categorical column
(e.g. labels) between train and test datasets.
        """,
        epilog=f"""
Examples:

  Basic usage:
    {prog_name} -i data.csv

  Specify output directory:
    {prog_name} -i data.csv -o ./output

  Custom train/test filenames:
    {prog_name} -i data.csv --train-file my_train.csv --test-file my_test.csv

  Define test size (percentage):
    {prog_name} -i data.csv -t 30

  Use specific column for stratification:
    {prog_name} -i data.csv -c label

  Full example:
    {prog_name} -i data.csv -o out -t 25 -c category
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # -------- Input --------
    parser.add_argument(
        "-i", "--input",
        required=True,
        metavar="FILE",
        help="Path to input CSV file"
    )

    # -------- Output --------
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        metavar="DIR",
        help="Directory where output files will be saved (default: current directory)"
    )

    parser.add_argument(
        "--train-file",
        default="train.csv",
        metavar="NAME",
        help="Filename for the train dataset (default: train.csv)"
    )

    parser.add_argument(
        "--test-file",
        default="test.csv",
        metavar="NAME",
        help="Filename for the test dataset (default: test.csv)"
    )

    # -------- Parameters --------
    parser.add_argument(
        "-t", "--test-size",
        type=float,
        default=16.66,
        metavar="PERCENT",
        help="Percentage of dataset to use as test set (0–100, default: 16.66)"
    )

    parser.add_argument(
        "-c", "--column",
        default="",
        metavar="COLUMN",
        help="""
Column name used for stratification.

If not provided, the last column of the CSV will be used.
Must be a categorical column (e.g. class labels).
"""
    )


    args = parser.parse_args()

    # -------- Validation --------
    if not (0 < args.test_size < 100):
        parser.error("--test-size must be between 0 and 100")

    return args


def main():
    args = parse_args()

    csv_train_file = os.path.join(args.output_dir, args.train_file)
    csv_test_file  = os.path.join(args.output_dir, args.test_file)

    try:
        generate_train_test_csv(
            input_csv=args.input,
            csv_train_file=csv_train_file,
            csv_test_file=csv_test_file,
            test_factor=args.test_size,
            column_name=args.column
        )

        print("✅ Work completed successfully")
        print(f"Train: {csv_train_file}")
        print(f"Test : {csv_test_file}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
