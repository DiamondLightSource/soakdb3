import json
from argparse import ArgumentParser

from soakdb3_lib.version import meta, version


def get_parser():
    parser = ArgumentParser(
        description="Command line accompanying the soakdb3 library."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version(),
        help="Print version string.",
    )
    parser.add_argument(
        "--version-json",
        action="store_true",
        help="Print version stack in json.",
    )
    return parser


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.version_json:
        print(json.dumps(meta(), indent=4))


if __name__ == "__main__":
    main()
