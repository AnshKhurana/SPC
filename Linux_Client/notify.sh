#! /bin/bash
export DISPLAY=:0.0
python3 /home/aman/Desktop/SPC_Post_Eval/Linux_Client/myscript.py --status | sed -n '/^Files wi/,/^--/p' > /home/aman/Desktop/SPC_Post_Eval/Linux_Client/difftemp
DISPLAY=:0.0 /usr/bin/notify-send  "You Not Been on Cloud it Seems!" "`cat /home/aman/Desktop/SPC_Post_Eval/Linux_Client/difftemp`"