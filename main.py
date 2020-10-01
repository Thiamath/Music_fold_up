import argparse as ap

from wrapper.wrapper import parse_files

parser = ap.ArgumentParser(description='Store music files into subfolders.')

parser.add_argument('--destination', '-d',
                    required=False,
                    help='Destination folder.',
                    default='.',
                    type=str)

parser.add_argument('--input', '-i',
                    required=False,
                    help='Input folder, file or files.',
                    default='.',
                    type=str)

parser.add_argument('--recursive', '-r',
                    action='store_true',
                    required=False,
                    help='Input folder, file or files.')

args = parser.parse_args()
print(f'args={args}')
parse_files(args.input, args.destination, recursive=args.recursive)
