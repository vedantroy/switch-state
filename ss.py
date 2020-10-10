#! /usr/bin/env python3

import argparse
import shutil
from tempfile import NamedTemporaryFile

parser = argparse.ArgumentParser(
    description="Switch between different variations of a file"
)
parser.add_argument("files", nargs="+", help="The files to process")
parser.add_argument("--comment-string", "-c", dest="c")
parser.add_argument("--state", "-s", dest="state")

args = parser.parse_args()

active_state = args.state
c_str = args.c
# TODO: We default to C style comments. Ideally, we auto-detect
# the comment type on a per-file basis & provide flags to either
# A) override the auto-detected comment string or B) provide a fallback
# if we can't auto-detect the comment string.
if c_str is None:
    c_str = "//"

state_flag = "SEC "
state_end_flag = "ENDSEC"

for fpath in args.files:
    new_lines = []
    with open(fpath) as f:
        in_state = None
        for idx, line in enumerate(f.readlines()):
            without_ws = line.lstrip(" ")
            num_ws = len(line) - len(without_ws)
            if without_ws[: len(c_str)] == c_str:
                comment = without_ws[len(c_str) :]
                if comment.startswith(state_flag):
                    if in_state:
                        raise Exception(
                            f'Line {idx}:\n"{line}"\nstarted new section but old section: "{in_state}" was not finished. Did you forget "{c_str + state_end_flag}"?'
                        )
                    in_state = comment[len(state_flag) :].rstrip(" \n")
                    new_lines.append(line)
                elif comment.startswith(state_end_flag):
                    in_state = None
                    new_lines.append(line)
                elif in_state and in_state == active_state:
                    # uncomment the line & shift back the code by the length of the comment
                    new_lines.append(
                        (" " * (num_ws - len(c_str))) + without_ws[len(c_str) :]
                    )
                else:
                    new_lines.append(line)
            elif in_state and in_state != active_state:
                new_lines.append((" " * num_ws) + c_str + without_ws)
            else:
                new_lines.append(line)

    with NamedTemporaryFile("w") as ftemp:
        ftemp.writelines(new_lines)
        ftemp.flush()
        shutil.copyfile(ftemp.name, fpath)
