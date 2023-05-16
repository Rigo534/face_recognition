from requests import Session
from sqlalchemy import Column, DateTime, Integer, String , BigInteger, ForeignKey, BLOB

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

SQLALCHEMY_DATABASE_URL = ("mysql+pymysql://root@localhost:3306/coba_db")

#create engine
engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
#mapped
Base = declarative_base()
class datasetImage(Base):
    __tablename__ = 'TabelDataset'
    id = Column(Integer,primary_key=True)
    image_name = Column(String(255))
    photo_id = Column(BLOB)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine ,autocommit=False, autoflush=False, )
session = Session()

def add_image(id, image_name, photo_id):
    new_image = datasetImage(id=id, image_name=image_name, photo_id = photo_id)
    
    session.add(new_image)
    session.commit()

def get_image_name_by_id(id):
    image = session.query(datasetImage).filter_by(id=id).first()
    if image:
        return image.image_name
    else:
        return None

path = "Images"
dir = os.listdir(path)
gambar_blob = []
for file_images in dir:
    with open(f'{path}/{file_images}', 'rb') as f:
        gambar = f.read()
    gambar_blob_1 = bytearray(gambar)
    gambar_blob.append(gambar_blob_1)

# datasetImage()

add_image(185928395628, 'Ricky Gosal', gambar_blob[0])
add_image(189387523798, 'Elon Musk', gambar_blob[1])
add_image(194728469583, 'Muh. Fauzan Azima', gambar_blob[2])

#print(get_image_name_by_id(12345678))