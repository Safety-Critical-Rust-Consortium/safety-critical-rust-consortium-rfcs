#!/usr/bin/env python3

"""
Generate the mdBook source tree from the RFC repository layout.

This mirrors the rust-lang/rfcs approach: RFCs live under text/, while src/
is generated just before building the book.
"""

import os
import shutil
import subprocess


def main():
    if os.path.exists("src"):
        shutil.rmtree("src")
    os.mkdir("src")

    for path in os.listdir("text"):
        symlink(f"../text/{path}", f"src/{path}")
    symlink("../README.md", "src/introduction.md")
    symlink("../SUBCOMMITTEES.md", "src/subcommittees.md")

    with open("src/SUMMARY.md", "w") as summary:
        summary.write("[Introduction](introduction.md)\n\n")
        summary.write("- [Subcommittees](subcommittees.md)\n")
        collect(summary, "text", 0)

    subprocess.call(["mdbook", "build"])


def collect(summary, path, depth):
    entries = [entry for entry in os.scandir(path) if entry.name.endswith(".md")]
    entries.sort(key=lambda entry: entry.name)
    for entry in entries:
        indent = "    " * depth
        name = entry.name[:-3]
        link_path = entry.path[5:]
        summary.write(f"{indent}- [{name}]({link_path})\n")
        maybe_subdir = os.path.join(path, name)
        if os.path.isdir(maybe_subdir):
            collect(summary, maybe_subdir, depth + 1)


def symlink(src, dst):
    if not os.path.exists(dst):
        os.symlink(src, dst)


if __name__ == "__main__":
    main()
