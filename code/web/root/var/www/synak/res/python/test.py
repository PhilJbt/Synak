#!/usr/bin/python3

import subprocess

cmd = "date"
output = subprocess.run(cmd, stdout=subprocess.PIPE)

print("Content-type: text/html\n")
print(output.stdout.decode('utf-8'))