import connection
import pandas as pd

 

class Class:

    mydb=connection.mydb
    mycursor=mydb.cursor()

    def __init__(self, id, name, teacherid=None):
        if id is None:
            self.id=0
        else:
            self.id=id
        self.name=name
        self.teacherid=teacherid

    