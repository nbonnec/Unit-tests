#!/usr/bin/env python

import os
import re
import sys
import unicodedata
import tempfile

def remove_score(s):
    return re.sub('-', '_', s)

def remove_c_ext(s):
    return re.sub("\.c", '', s)

# Remove all accents from the string
def clean_string(s):
    if isinstance(s, str):
        s = unicode(s, "utf8", "replace")
    s = unicodedata.normalize('NFD', s)
    return s.encode('ascii', 'ignore')


##############################
##         Script           ##
##############################

if len(sys.argv) < 2:
    print("You must specify a file to test...")
    print(" Ex: " + sys.argv[0] + " foo.c")
    print("Stop.")
    sys.exit(1)

# cleaning the file_name
module = remove_c_ext(sys.argv[1])

source_module = module + ".c"

# create a temporary file
f_temp = tempfile.TemporaryFile()

try:
    f_module = open(source_module, 'a+')
except IOError:
    print("Error with the file" + source_module + ".\nStop.")
    sys.exit(1)

# backup the file
f_module.seek(0)
f_temp.write(f_module.read())

# add inclusion of unit tests
f_module.write("\n#include \"cu-" + source_module + "\"\n")
f_module.close()

try:
    f_main = open("main.c", 'w')
except IOError:
    print("Error with the file main.c.\nStop.")
    sys.exit(1)

header_module = module + ".h"

# Filling the main program.
f_main.write("/*\n * This file has been generated.\n */")
f_main.write("\n\n#include \"cu-" + header_module + "\"\n\n")

# cleaning the file_name
module = remove_score(clean_string(module))

f_main.write("int main(void)\n{")
f_main.write("\n    cu_" + module.lower() + "_tests();\n")
f_main.write("\n    return 0;")
f_main.write("\n}\n")
f_main.close()

# Make process
os.system("make FILE=" + source_module)

try:
    f_module = open(source_module, 'w')
except IOError:
    print("Error with the file" + source_module + ".\nStop.")
    sys.exit(1)

# rewind the temporary file
f_temp.seek(0)
f_module.write(f_temp.read())

f_temp.close()
f_module.close()

# Run unit tests
os.system("./tests.exe")

