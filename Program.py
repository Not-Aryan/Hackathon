import face_recognition
import cv2
import numpy as np
import os
import sys


i = 0
known_face_encodings = []
known_face_names = []
cwd = os.getcwd()
for filename in os.listdir("images/"):
    if filename.endswith(".jpg"):
        i = i+1
        n = face_recognition.load_image_file("images/"+filename)
        m = face_recognition.face_encodings(n)[0]
        known_face_encodings.append(m)
        known_face_names.append(str(filename.split(".jpg")[0]))


video_capture = cv2.VideoCapture(1)
z = i
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
present = []
x = False
print("You've activated the attendence system.")
h = 0
while True:        
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                if name not in present:
                    print(str(name)+" is here")
                    present.append(name)
                    if i == 1:
                        print("All Students Are Here!")
                        sys.exit()
                    else:
                        i = i-1
                        print(str(i) + " students haven't arrvied, their names are:")
                        for val in known_face_names:
                            h = h+1
                            if val not in present:
                              print(val)
                              if h == z:
                                  print("----------")
        

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
##
##    if cv2.waitKey(1) & 0xFF == ord('e'):
##        for val in known_face_names:
##            if val in present:
##                print(val + " is here")
##            else:
##                print(val +" absent")
##    elif cv2.waitKey(1) & 0xFF == ord('t'):
##        for val in known_face_names:
##            if val in present:
##                print(val + " is here")
##            else:
##                print(val+ " is absent")

video_capture.release()
cv2.destroyAllWindows()
