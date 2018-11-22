#! /bin/bash
python3 myscript.py --status | sed -n '/^Files wi/,/^--/p' > difftemp
# sed -n '/^Files wi/,/^--/p' difftemp
echo hello
echo $diff_files