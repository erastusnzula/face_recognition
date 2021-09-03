import os
import random
import winsound

import cv2
import face_recognition
import numpy


class SecurityCamera:

    def __init__(self):
        self.images = []
        self.base_names = []
        self.encoded_faces = []
        self.path = 'images'
        print('please wait my dummy program is busy encoding...')
        self.camera = cv2.VideoCapture(0)
        self.known_encoded_faces = []
        self.frame_one = None

    def known_image_folder(self):
        for image in os.listdir(path=self.path):
            if not (image.endswith('.jpeg') or image.endswith('.JPG') or image.endswith('.jpg') or image.endswith(
                    '.png')):
                continue
            img = cv2.imread(f"{self.path}/{image}")
            self.images += [img]
            self.base_names += [os.path.splitext(image)[0]]

    def encode_face(self, images):
        for image in images:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_encoding = face_recognition.face_encodings(image_rgb)[0]
            self.encoded_faces += [face_encoding]
        return self.encoded_faces

    def run(self):
        self.known_image_folder()
        self.known_encoded_faces = self.encode_face(self.images)
        print("Encoding Complete, camera opening...")
        self.open_camera_tasks()

    def open_camera_tasks(self):
        while self.camera.isOpened():
            _, self.frame_one = self.camera.read()
            self.detect_faces()
            cv2.imshow("Press 'c' to capture an image.", self.frame_one)
            key = cv2.cv2.waitKey(1)
            if key == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
            elif key == ord('c'):
                cv2.imwrite(f'Image {random.randint(1, 100)}.png', self.frame_one)

    def detect_faces(self):
        frame_one_rgb = cv2.cvtColor(self.frame_one, cv2.COLOR_BGR2RGB)
        face_location = face_recognition.face_locations(frame_one_rgb)
        face_encoding = face_recognition.face_encodings(frame_one_rgb, face_location)
        for face_encoded, face_located in zip(face_encoding, face_location):
            self.face_comparison(face_encoded, face_located)

    def face_comparison(self, face_encoded, face_located):
        compare_face = face_recognition.compare_faces(self.known_encoded_faces, face_encoded)
        face_distance = face_recognition.face_distance(self.known_encoded_faces, face_encoded)
        distance_index = numpy.argmin(face_distance)
        if compare_face[distance_index]:
            name = self.base_names[int(distance_index)].title()
            x, y, w, h = face_located
            cv2.rectangle(self.frame_one, (h, x), (y, w), (0, 255, 0), 2)
            cv2.rectangle(self.frame_one, (h, x - 40), (y, w), (0, 255, 0), 2)
            cv2.putText(self.frame_one, name, (h + 10, x - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            x, y, w, h = face_located
            cv2.rectangle(self.frame_one, (h, x), (y, w), (0, 255, 0), 2)
            cv2.rectangle(self.frame_one, (h, x - 40), (y, w), (0, 255, 0), 2)
            cv2.putText(self.frame_one, "Unknown", (h + 10, x - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
            print("Intruder in the house.")


SecurityCamera().run()
