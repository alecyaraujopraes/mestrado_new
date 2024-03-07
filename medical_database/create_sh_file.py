import csv
import pandas as pd
from io import BytesIO
from minio import Minio
from minio.error import S3Error
import pandas as pd


client = Minio("192.168.0.12:9000/", 
               "redda",  
               "SnowinRio", 
                secure=False)

print("Connected to Minio")

objects = client.list_objects("mestrado", prefix="papers/")

for obj in objects:
    response = client.get_object("mestrado", f"{obj.object_name}")

    texts = response.data.decode("utf-8")
    # .split("\r\n\r\n")

    # for text in texts:
    sentences_used = []
    if texts not in sentences_used:
        t0 = texts.replace("\r\n", " ")
        t1 = t0.replace("\n", " ")
        t = t1.replace("\r", " ")

        str_line = f"""python3 medical_database/SpacyParse.py -s "{t}" """

        with open("medical_database/run_spacy.sh", "a") as my_file:
            my_file.write(str_line)
            my_file.write("\n")
        
        sentences_used.append(texts)