import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "" # enter url
})

ref = db.reference("students")

data = {
    "911": {
        "name": "Ryan Reynolds",
        "major": "BSC CS",
        "starting_year": 2022,
        "total_attendance": 2,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2023-2-21 00:29:43"
    }, "990": {
        "name": "Tom Cruise",
        "major": "BSC IT",
        "starting_year": 2021,
        "total_attendance": 6,
        "standing": "B",
        "year": 3,
        "last_attendance_time": "2023-2-21 00:29:59"
    }, "991": {
        "name": "Ryan Gosling",
        "major": "BSC IT",
        "starting_year": 2023,
        "total_attendance": 8,
        "standing": "G",
        "year": 1,
        "last_attendance_time": "2023-2-21 00:30:43"
    }, "992": {
        "name": "Elon Musk",
        "major": "BSC IT",
        "starting_year": 2020,
        "total_attendance": 5,
        "standing": "A",
        "year": 4,
        "last_attendance_time": "2023-2-21 00:31:43"
    }, "993": {
        "name": "Sebastian Vettel",
        "major": "BSC CS",
        "starting_year": 2023,
        "total_attendance": 7,
        "standing": "B",
        "year": 3,
        "last_attendance_time": "2023-2-21 00:32:11"
    }, "997": {
        "name": "Bill Gates",
        "major": "MSC CS",
        "starting_year": 2023,
        "total_attendance": 5,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2023-2-21 00:33:15"
    }, "999": {
        "name": "Dastagir Shaikh",
        "major": "BSC CS",
        "starting_year": 2022,
        "total_attendance": 2,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2023-2-21 00:34:00"
    }
}

ref.update(data)
