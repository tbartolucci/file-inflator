#!/usr/bin/python

import os, argparse, shutil


def convert_size(size):
    # Convert a string to bytes
    # Supports [Number][K|M|G]
    # Returns size in bytes
    magnitude = size[-1:]
    if magnitude == 'K':
        multiplier = 1000
    elif magnitude == 'M':
        multiplier = 1000000
    elif magnitude == 'G':
        multiplier = 1000000000
    else:
        raise Exception("Unknown size magnitude")

    number = int(size[0:-1])
    return number * multiplier


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-file', required=True)
    parser.add_argument('--desired-size', required=False)
    parser.add_argument('--out-file', required=False)
    args = parser.parse_args()

    # Set default target file size
    if args.desired_size is None:
        desired_size = "100M"
    else:
        desired_size = args.desired_size

    # Convert file size to bytes
    desired_size_in_bytes = convert_size(desired_size)

    # Set default output file name
    if args.out_file is None:
        out_file = desired_size + "_" + args.in_file
    else:
        out_file = args.out_file

    print("Reading contents of source file: " + args.in_file)
    fh = open(args.in_file, 'r')
    lines = fh.readlines()
    fh.close()

    print("Copying data to inflate file to " + desired_size)
    shutil.copyfile(args.in_file, out_file)
    wh = open(out_file, 'a')
    current_size = os.stat(out_file).st_size

    while current_size < desired_size_in_bytes:
        wh.writelines(lines)
        current_size = os.stat(out_file).st_size

    exit(0)
