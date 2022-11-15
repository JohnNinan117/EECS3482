import os


def decrypt_content(f):
    # HINT: For Part 2, you'll need to decrypt the contents of this file
    # The existing scheme plaintext
    # As such, we just convert it back to ASCII and print it out
    decoded_text = str(f, 'ascii')
    print(decoded_text)


def decrypt(fn):
    f = open(os.path.join("files", fn), "rb").read()
    decrypt_content(f)
