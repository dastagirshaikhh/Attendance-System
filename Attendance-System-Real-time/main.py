from datetime import datetime
from time import time, sleep
import numpy as np
import os
import pickle
import cv2
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "", "storageBucket": ""}) #enter url

bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # Use index 0 for default camera
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

# importing mode Images used for the cam
imgBg = cv2.imread("Resources/background.png")
folderModePath = "Resources/Modes"
ModePathList = os.listdir(folderModePath)
imgModeList = []
for path in ModePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

print("Loading Encode file...")
file = open("EncodeFile.p", "rb")
encodeListKnownIds = pickle.load(file)
file.close()
encodeListKnown, studentsId = encodeListKnownIds
# print(studentsId)
print("Encode file loaded")

modeType = 0
counter = 0
id = -1
ImgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBg[172 : 172 + 480, 25 : 25 + 640] = img

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBg = cvzone.cornerRect(imgBg, bbox, rt=0)
                id = studentsId[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBg, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBg)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

                # Add condition to update attendance only once per face detection
                if counter == 1:
                    # Reset studentsInfo to clear previous student's information
                    studentsInfo = {}

                    studentsInfo = db.reference(f"students/{id}").get()
                    print(studentsInfo)

                    # Update data of the attendance
                    datetimeObj = datetime.strptime(
                        studentsInfo["last_attendance_time"], "%Y-%m-%d %H:%M:%S"
                    )
                    secondsElapsed = (datetime.now() - datetimeObj).total_seconds()

                    if secondsElapsed > 30:
                        ref = db.reference(f"students/{id}")
                        studentsInfo["total_attendance"] += 1
                        ref.child("total_attendance").set(
                            studentsInfo["total_attendance"]
                        )
                        ref.child("last_attendance_time").set(
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                    else:
                        modeType = 3
                        counter = 0

        if counter != 0:
            if counter == 1:
                studentsInfo = db.reference(f"students/{id}").get()
                print(studentsInfo)

            if modeType != 3:
                if 10 < counter <= 20:
                    modeType = 2
                    imgBg[172 : 172 + 480, 25 : 25 + 640] = img[modeType]

                if counter <= 10:
                    font = cv2.FONT_HERSHEY_COMPLEX
                    font_scale = 1
                    font_thickness = 1
                    font_color = (255, 255, 255)  # White color

                    # Define text positions
                    positions = {
                        "name": (808, 405),  # Adjusted y-coordinate from 415 to 405
                        "id": (808, 443),  # Adjusted y-coordinate from 463 to 443
                        "major": (808, 501),  # Adjusted y-coordinate from 511 to 501
                        "standing": (808, 549),  # Adjusted y-coordinate from 559 to 549
                        "year": (808, 597),  # Adjusted y-coordinate from 607 to 597
                        "starting_year": (
                            808,
                            645,
                        ),  # Adjusted y-coordinate from 655 to 645
                    }

                    imgBgCopy = imgBg.copy()
                    # Write text onto the image
                    for key, value in studentsInfo.items():
                        if key in positions:
                            text = f"{key.capitalize()}: {value}"  # Format the text
                            cv2.putText(
                                imgBgCopy,
                                text,
                                positions[key],
                                font,
                                font_scale,
                                font_color,
                                font_thickness,
                            )

                    # Display the image with text
                    cv2.imshow("Face Attendance", imgBgCopy)
                    cv2.waitKey(1)  # Wait for a short time to display the image

                    # Add a delay to remove the displayed student information after 3 seconds
                sleep(5)

                # Clear the displayed student information by creating a new copy of imgBg without the text
                imgBgCopy = imgBg.copy()

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentsInfo = {}
                    ImgStudent = 0

        cv2.imshow("Face Attendance", imgBg)
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
            break
    else:
        modeType = 0
        counter = 0


cap.release()
cv2.destroyAllWindows()
