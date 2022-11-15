import os


def sign_file(f):
    # TODO: For Part 2, you'll use public key crypto here
    # The existing scheme just ensures the updates start with the line 'EECS3482'
    # This is naive -- replace it with something better!
    return bytes("EECS3482\n", "ascii") + f


def save_signed_filed(fn):
    f = open(os.path.join("files", fn), "rb").read()
    signed_f = sign_file(f)
    signed_fn = os.path.join("files", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    #print("Signed file written to", signed_fn)
