#! /usr/bin/env python
# This script takes html files as arguments and rewrites the files
# with its contents properly indented

from bs4 import BeautifulSoup
import os, sys

def makeitpretty(fname):
    """ saves html file f with prettified contents """
    print("Prettifying %s"%fname)
    f = open(fname, "r")
    html = f.read()
    f.close()
    f = open(fname, "w")
    soup = BeautifulSoup(html)
    f.write(soup.prettify("utf-8"))
    f.close()
    print("Done on %s"%fname)

requireconfirmation = True
for f in sys.argv[1:]:
    _, ext = os.path.splitext(f)
    if ext != ".html":
        print "WARNING: %s is not an html file. Ignored"%f
        continue
    if requireconfirmation:
        confirmed = False
        print "Contents of file %s will be overwriten."%f
        print "\t Please select: 'C'ontinue, 'I'gnore this file, 'A'll, 'E'xit"
        answ = raw_input().lower()

        if answ == 'c':
            confirmed = True
        elif answ == 'a':
            confirmed = True
            requireconfirmation = False
        elif answ == 'E':
            break
        else:    # ignore this file
            continue
    makeitpretty(f)
