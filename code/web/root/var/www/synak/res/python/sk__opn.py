#!/usr/bin/python3


# Open a file, read it, and return its content
def getTemplate(_fileName):
    fp = open(f"../template/{_fileName}.tpl", "r")
    cont = fp.read().replace("\n", "").replace("\r", "")
    fp.close()
    return cont