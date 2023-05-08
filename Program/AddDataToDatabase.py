import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pickle
import json
import numpy as np

cred = credentials.Certificate('Program/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://facerecognitionattendanc-ff2b5-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
ref = db.reference("Employee")

data1 = {
    "189387523798": {
        "Nama" : "Elon Musk", 
    },
    "194728469583" : {
        "Nama" : "Muh. Fauzan Azima"
    },
    "185928395628" : {
        "Nama" : "Ricky Gosal"
    }
}

for key, value in data1.items():
    ref.child(key).set(value)


