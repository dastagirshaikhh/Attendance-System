import cv2, pickle, face_recognition, os, firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "", "storageBucket": ""}  # enter url
)

folderPath = "Images"
ImgPathList = os.listdir(folderPath)
imgList = []
studentsId = []
for path in ImgPathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentsId.append(os.path.splitext(path)[0])

    filename = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    # blob.upload_from_file(filename)
    with open(filename, "rb") as file:
        blob.upload_from_file(file)


# print(studentsId)


def findEncodings(imagelist):
    encodeList = []
    for img in imagelist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print("Starting Encoding....")
encodeListKnown = findEncodings(imgList)
encodeListKnownIds = [encodeListKnown, studentsId]
print("Encoding Complete")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownIds, file)
file.close()
print("Encode file created")
