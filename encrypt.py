#!/usr/bin/env python3

import os, sys
from cryptography.fernet import Fernet

# Set this as the root directory from where you need to encrypt all the files.
root_dir = "test_dir"

all_files = []

#  for file in os.listdir():
for file in os.listdir(root_dir):

    # sys.argv[0] is the name of current file.
    # Be sure to not encrypt important files like the key or the
    # encryption and decryption scripts. As long as the `root_dir' is
    # different from the current directory, this should not be an issue.
    if file == sys.argv[0] or file == "key.key" or file == "decrypt.py":
        continue

    # Since test directory is different from the current file
    # location, we need to give the absolute path for the file to
    # check if it's a file or a directory.
    if os.path.isfile(os.path.join(root_dir, file)):
        all_files.append(os.path.join(root_dir, file))

# print("Files: ", all_files)

key = Fernet.generate_key()

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
