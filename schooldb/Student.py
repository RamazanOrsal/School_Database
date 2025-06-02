import mysql.connector
from datetime import datetime
import connection
import pandas as pd


class Student:
    def __init__(self, id, studentNummer, name, surname, birthday, gender, classid,):
        if id is None:
            self.id=0
        else:
            self.id=id
        self.studentNummer=studentNummer
        self.name=name
        self.surname=surname
        self.birthday=birthday
        self.gender=gender
        self.classid=classid





