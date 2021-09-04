##### **Security Camera - face recognition**

**Description**

It detects faces in a live camera feed, compares them against
images directory. If the image exist in the images directory
it attaches the image name tag. If the image does not exist 
it plays an alert sound and attaches 'Unknown' as the name tag.

**Packages**

```
import os
import winsound

import cv2
import face_recognition
import numpy
```
**Running the program**

You must have python installed in your system.
Click the main.py file in a directory with an image folder.

**How it works**
- It detects faces and draws a rectangle box around the face with a name tag.
- If face encodings don't match any of the image directory encodings it attaches `unknown` name tag.
- To capture an image press `space bar` or `c`, the image is saved in the Security Camera Images directory.
- The program automatically saves the video feed in the Security Camera Video directory.
- To exit press `q` or `esc` key.