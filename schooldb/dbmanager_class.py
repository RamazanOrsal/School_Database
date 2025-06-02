import mysql.connector
import connection
import pandas as pd
from dbmanager_teacher import tchDbManager
from Class import Class
import random

class classDbmanager:

    def __init__(self):
        self.connection=connection.mydb
        self.cursor=self.connection.cursor()

    def getallClass(self):

        self.addhomeroomTeacher()
        sql="select c.id, CONCAT(c.Grade, ' ', c.Section) as Class , CONCAT(t.name, ' ', t.surname) as HomeroomTeacher from class as c left join teacher as t on c.teacherid=t.id"
        self.cursor.execute(sql)
        try:
            obj=pd.DataFrame(self.cursor.fetchall(),columns=[i[0] for i in self.cursor.description])
            obj.set_index('id', inplace=True)
            obj.index.name = None
            print(obj)
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')


    def addhomeroomTeacher(self):
        sql="select * from class"
        self.cursor.execute(sql)
        obj=pd.DataFrame(self.cursor.fetchall(), columns=[i[0] for i in self.cursor.description])
        
        if obj['teacherid'].isnull().any():

            teacher=tchDbManager.getallteacher(self)
            teacheridlist=teacher['id'].tolist()
            usedidlist=obj['teacherid'].tolist()

            different_idlist=list(set(teacheridlist)-set(usedidlist))

            nan_indices = obj[obj['teacherid'].isna()].index
            for i in nan_indices:
                if different_idlist:
                    chosen_id = random.choice(different_idlist)
                    obj.at[i, 'teacherid'] = chosen_id
                    different_idlist.remove(chosen_id)
                else:
                    print('Not enough teachers are available to be homeroom teachers.')


            tuples = [(Grade, Section, teacherid, id) for id, Grade, Section, teacherid in obj.itertuples(index=False, name=None)]
            self.cursor.executemany("UPDATE class SET Grade=%s, Section=%s, teacherid=%s WHERE id=%s", tuples)
            
            try:        
                self.connection.commit()
            except mysql.connector.Error as err:
                print(f'Error: {err}')
        
        else:
            return


    def getclassbyId(self, id):
        sql="select * from class where id=%s"
        values=(id,)
        self.cursor.execute(sql, values)
        try:
            obj=self.cursor.fetchone()
            print(obj)
            return Class(obj[0],obj[1],obj[2])
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')


    def classdataEntry(self):
        list=[]
        tchDbManager.getallteacher(self)
        while True:
            id=None
            name=input('Enter class name:')
            x=input('Enter teacher id:')
            if x.strip()!='':
                teacherid=int(x)
            list.append((id, name, teacherid))

            kontrol=input('Do you want to add another entry? (y/n)')

            if kontrol == 'n':
                if len(list) == 1:
                    newclass=Class(id, name, teacherid)
                    self.addClass(newclass)
                else:
                    self.addClasses(list)
                break



    def addClass(self, newclass:Class):
        sql= "INSERT INTO class (id, name, teacherid) VALUES (%s, %s, %s)"
        value= (newclass.id, newclass.name, newclass.teacherid)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'{newclass.name} has been added to the database.')
    
        except mysql.connector.Error as err:
            print('Error:', err)

    def addClasses(self, classes):
        sql= "INSERT INTO class (id, name, teacherid) VALUES (%s, %s, %s)"
        values= classes
        self.cursor.executemany(sql,values)

        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} class have been added to the database.')
            print('Added class:')
            print(pd.DataFrame(classes))
        except mysql.connector.Error as err:
            print('Error:', err)


    def newdataUpdating(self, newclass:Class):
        tchDbManager.getallteacher(self)
        c = input("Enter class's teacherid :")
        if c.strip() != '':
            newclass.teacherid =int(c)

        self.editClass(newclass)

    def editClass(self, newclass:Class):
        sql='update class set name=%s, teacherid=%s where id=%s'
        values=(newclass.name, newclass.teacherid, newclass.id)
        self.cursor.execute(sql, values)

        try:
            self.connection.commit()
            print(f'The homeroom teacher for class {newclass.name} has been successfully changed.')
        except mysql.connector.Error as err:
            print('Error:', err)


    def deleteClass(self, id):
        sql= "delete from class where id=%s"
        value= (id,)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'The class with ID {id} has been deleted from the database.')
    
        except mysql.connector.Error as err:
            print('Error:', err)


    def close(self):
        self.cursor.close()
        self.connection.close()
        print('Database connection has been closed.')

        
