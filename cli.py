"""
CLI interface for the app
"""

import argparse

def load_cli():
    """
    loads the cli
    """
    parser = argparse.ArgumentParser(
        prog="Emotion Recognition App",
        description="Face and Emotion Recogition App with Simple Statistics"
    )

    parser.add_argument("-l", "--list", action="store_true", help="list history")
    parser.add_argument("-s", "--stats", type=int, metavar="TIME_WINDOW")

    args = parser.parse_args()

    return args
