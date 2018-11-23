#! /bin/bash
export DISPLAY=:0.0
spc --status | sed -n '/^Files wi/,/^--/p' > /usr/bin/difftemp
DISPLAY=:0.0 /usr/bin/notify-send  "You have not been on Cloud it seems!" "`cat /usr/bin/difftemp`"
