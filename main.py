"""Entry program for make.fun news-image-20261121.

Writes the front-page image summarising Saturday 21 November 2026's
world news to /output/entry.png.

The image is rendered by generate.py (Pillow, run locally at build time)
and committed as entry.png; this program only copies it, so the run is
deterministic, needs no network, and uses only the standard library.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
