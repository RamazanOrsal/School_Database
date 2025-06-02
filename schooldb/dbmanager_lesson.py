import mysql.connector
import connection
import pandas as pd
from Lesson import Lesson
import random

class lessonDbmanager:

    def __init__(self):
        self.connection=connection.mydb
        self.cursor=self.connection.cursor()


    def getallLesson(self):

        sql="Select * from lesson "
        self.cursor.execute(sql)
        try:
            obj=pd.DataFrame(self.cursor.fetchall(),columns=[i[0] for i in self.cursor.description])
            obj.set_index('id', inplace=True)
            obj.index.name = None
            print(obj)
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')    

    def getallLessonwithTeacher(self):

        sql="Select l.id, l.name, CONCAT(t.name, ' ', t.surname) as Teacher from teacher as t inner join lesson as l on t.branch=l.id "
        self.cursor.execute(sql)
        try:
            obj=pd.DataFrame(self.cursor.fetchall(),columns=[i[0] for i in self.cursor.description])
            obj.set_index('id', inplace=True)
            obj.index.name = None
            print(obj)
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')


    def getlessonbyId(self, id):
        sql="select * from lesson where id=%s"
        values=(id,)
        self.cursor.execute(sql, values)
        try:
            obj=self.cursor.fetchone()
            print(obj)
            return Lesson(obj[0],obj[1])
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')


    def lessondataEntry(self):
        list=[]
        while True:
            id=None
            name=input('Enter lesson name:')
            list.append((id, name))

            kontrol=input('Do you want to add another entry? (y/n)')

            if kontrol == 'n':
                if len(list) == 1:
                    lesson=Lesson(id, name)
                    self.addLesson(lesson)
                else:
                    self.addLessons(list)
                break



    def addLesson(self, lesson:Lesson):
        sql= "INSERT INTO lesson (id, name) VALUES (%s, %s)"
        value= (lesson.id, lesson.name)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'{lesson.name} has been added to the database.')
    
        except mysql.connector.Error as err:
            print('Error:', err)

    def addLessons(self, lessons):
        sql= "INSERT INTO lesson (id, name) VALUES (%s, %s)"
        values= lessons
        self.cursor.executemany(sql,values)

        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} lessons have been added to the database.')
            print('Added lesson:')
            print(pd.DataFrame(lessons))
        except mysql.connector.Error as err:
            print('Error:', err)


    def newdataUpdating(self, lesson:Lesson):
        c = input("Enter lesson's name:")
        if c.strip() != '':
            lesson.name =c
        self.editLesson(lesson)

    def editLesson(self, lesson:Lesson):
        sql='update lesson set name=%s where id=%s'
        values=(lesson.name, lesson.id)
        self.cursor.execute(sql, values)

        try:
            self.connection.commit()
            print(f'{lesson.name} has been successfully corrected.')
        except mysql.connector.Error as err:
            print('Error:', err)


    def close(self):
        self.cursor.close()
        self.connection.close()
        print('Database connection has been closed.')



        
