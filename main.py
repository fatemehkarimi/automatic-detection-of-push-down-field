import argparse
import sys
from core.pushdown_field_detector import PushDownFieldDetector


def main(arguments):
    detector = PushDownFieldDetector(arguments.path)
    detector.extract_project_classes()
    detector.extract_field_usage()
    detector.detect_project_push_down_positions()
    detector.print_report()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Automatic detection of push-down field refactoring in Java programs')

    parser.add_argument(
        '--path',
        help='the directory in which program source code is located')
    args = parser.parse_args()
    if not args.path:
        parser.print_help()
        sys.exit(1)
    main(args)
