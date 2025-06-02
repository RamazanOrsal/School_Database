import mysql.connector
from datetime import datetime
import connection
import pandas as pd


class Lesson:

    mydb=connection.mydb
    mycursor=mydb.cursor()

    def __init__(self, id, name):
        if id is None:
            self.id=0
        else:
            self.id=id
        self.name=name

