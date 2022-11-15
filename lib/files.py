import os
import traceback
from os import walk
from lib.comms import Message

#import tqdm
# Instead of storing files on disk,
# we'll save them in memory for simplicity
filestore = {}

def encrypt(data):
    # Encrypt the file so that
    # the user you send it to could  read
    return data


def verify_file(f):
    # Verify the file was sent by the user
    # TODO: NO NEED TO WORRY FOR ASSIGNEMNT 1
    # Naive verification by ensuring the first line has the "passkey"
    lines = f.split(bytes("\n", "ascii"), 1)
    first_line = lines[0]
    if first_line == bytes("Caesar", "ascii"):
        return True
    return False

def process_file(fn, f):
    if verify_file(f):
        # encrypt and store the file
        filestore[fn] = f
        print("Stored the received file as %s" % fn)
    else:
        print("WARNING: The file cannot be verified...")


def recv_file(sconn):
    # Download the file from the other bot
    fn = str(sconn.recv(), "ascii")
    f = sconn.recv()
    print("Receiving %s" % fn)
    process_file(fn, f)
    fd = open("downloaded_file_%s" %fn, "wb")
    fd.write(f)
    fd.close()

###

def send_file(sconn):
     # for simplicity we'll keep the files
    #  in the "files" directoru
    files = {}
    for (dirpath, dirnames, filenames) in\
        walk("./files"):
        for i, f in enumerate(filenames):
            files[i]=f
    print("*** Available Files ***")
    for k, v in files.items():
        print(str(k)+") "+v)

    while True:
        f = input("Please choose which file [0 - "+
                    str(len(files)-1)+
                    "] to send:")
        try:
            fn = files[int(f)]
            break;
        except:
            print("Incorrect file index, please try again""")
            traceback.print_exc()
            continue
    print("Sending file")
    f = open(os.path.join("files", fn), "rb").read()
    sconn.send(Message.FILE_TRANSFER)
    sconn.send(bytes(fn,"ascii"))
    sconn.send(f)
    # Grab the file and send it to another user
    #if fn not in filestore:
    #    print("That file doesn't exist in the botnet's filestore")
    #    return
    #print("Sending %s via P2P" % fn)
    #sconn.send(fn)
    #sconn.send(filestore[fn])
