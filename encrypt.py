#!/usr/bin/env python3

import os, sys
from cryptography.fernet import Fernet

# If not input is given, then set current directory as the root
# directory from where you need to encrypt all the files.

if len(sys.argv) > 1:
    root_dir = sys.argv[1]
else:
    root_dir = 'test_dir'

all_files = []

def list_files(base_dir):
    global all_files
    for entry in os.listdir(base_dir):

        # sys.argv[0] is the name of current file.
        # Be sure to not encrypt important files like the key or the
        # encryption and decryption scripts. As long as the `root_dir' is
        # different from the current directory, this should not be an issue.
        if entry == sys.argv[0] or entry == "key.key" or entry == "decrypt.py":
            continue

        if os.path.isdir(os.path.join(base_dir, entry)):
            list_files(os.path.join(base_dir, entry))

        elif os.path.isfile(os.path.join(base_dir, entry)):
            all_files.append(os.path.join(base_dir, entry))

key = Fernet.generate_key()

list_files(root_dir)

# Save the key for now so that we can also decrypt all the encrypted
# files using the same key.

# Open file in 'wb' so that we can write binary to it.
with open("key.key", "wb") as keyfile:
    keyfile.write(key)

for file in all_files:
    with open(file, "rb") as raw_file:
        contents = raw_file.read()
    enc_contents = Fernet(key).encrypt(contents)
    with open(file, "wb") as raw_file:
        raw_file.write(enc_contents)

print("Files that have been encrypted are:")
for names in all_files:
    print("{}".format(names))
