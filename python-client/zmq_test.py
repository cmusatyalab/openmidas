#!/usr/bin/env python3

import cv2
import numpy as np
import zmq
import time
import random
import os

def send_array(socket, A, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(
        dtype = str(A.dtype),
        shape = A.shape
    )
    socket.send_json(md, flags|zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)



context = zmq.Context()

#  Socket to talk to server
print("Publishing images from current working directory on port 5555...")
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')

for entry in os.scandir("./"):
    if entry.is_file():
        if (entry.path.endswith(".jpg") or entry.path.endswith(".png")):
            img = cv2.imread(entry.path)
            print(f"Sending request with {entry.path}...")
            send_array(socket, img)
            time.sleep(random.random())