#!/usr/bin/env python3

import argparse
import os
import WorkingWithFiles as rnfunc

import dataset_csv_generator.about as about


def normalize_formats(format_list):
    """
    Normalize input formats:
    - ensure leading dot
    - convert to lowercase
    - remove duplicates
    - set default if empty
    """
    if not format_list:
        return {".png", ".jpg", ".jpeg"}

    normalized = set()

    for fmt in format_list:
        fmt = fmt.lower().strip()
        if not fmt.startswith("."):
            fmt = "." + fmt
        normalized.add(fmt)

    return normalized


def main():

    prog_name = about.__program_csv_gen__

    parser = argparse.ArgumentParser(
        description=(
            "Generate a CSV file for image classification datasets based on "
            "a directory structure.\n\n"
            "Each row in the CSV will contain:\n"
            "  1. File path\n"
            "  2. Label (derived from directory structure)"
        ),
        epilog=(
            "Examples:\n\n"
            f"  {prog_name} --input-base-dir data\n\n"
            f"  {prog_name} --input-base-dir data --input-format jpg --input-format png\n\n"
            f"  {prog_name} --input-base-dir data --label-first --header filepath class\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--output-csv-file",
        default="dataset.csv",
        help="Output CSV file name (default: dataset.csv)"
    )

    parser.add_argument(
        "--input-base-dir",
        required=True,
        help=(
            "Base directory containing images organized in subdirectories.\n"
            "The folder structure determines the labels."
        )
    )

    parser.add_argument(
        "--input-format",
        action="append",
        help=(
            "Image file extensions to include (can be used multiple times).\n"
            "Examples: --input-format .png --input-format jpg\n"
            "Default: .png, .jpg, .jpeg"
        )
    )

    # ✅ Header configurável
    parser.add_argument(
        "--header",
        nargs=2,
        metavar=("COLUMN1", "COLUMN2"),
        default=["filename", "label"],
        help=(
            "CSV header (2 columns).\n"
            "Default: filename label"
        )
    )

    # Label selection
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--label-first",
        action="store_true",
        help=(
            "Use the first-level directory (closest to base dir) as label.\n"
            "Example: base/class1/subdir/image.png → label = class1"
        )
    )

    group.add_argument(
        "--label-last",
        action="store_true",
        help=(
            "Use the last directory (closest to file) as label (default).\n"
            "Example: base/class1/subdir/image.png → label = subdir"
        )
    )

    args = parser.parse_args()

    # Verifica se o diretório existe
    if not os.path.exists(args.input_base_dir):
        parser.error(f"Base directory does not exist: {args.input_base_dir}")

    # Normaliza formatos
    format_set = normalize_formats(args.input_format)

    # Define comportamento do label
    label_first = True if args.label_first else False

    print("\nConfiguration:")
    print("  csv_file    :", args.output_csv_file)
    print("  base_dir    :", args.input_base_dir)
    print("  formats     :", format_set)
    print("  header      :", args.header)
    print("  label_first :", label_first)
    print()

    res, Count = rnfunc.generate_csv_file_from_dir_structure(
        args.input_base_dir,
        list(format_set),
        args.output_csv_file,
        header=args.header,
        label_first=label_first
    )

    # Save JSON summary
    with open(args.output_csv_file + ".json", "w") as f:
        json.dump(Count, f, indent=4)

if __name__ == "__main__":
    main()

