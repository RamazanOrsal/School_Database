import mysql.connector
from datetime import datetime
import connection
import pandas as pd


 

class Teacher:

    mydb=connection.mydb
    mycursor=mydb.cursor()

    def __init__(self, id=None, name='', surname='', birthday='', gender='', branch=''):
        if id is None:
            self.id=0
        else:
            self.id=id
        self.branch=branch
        self.name=name
        self.surname=surname
        self.birthday=birthday
        self.gender=gender
