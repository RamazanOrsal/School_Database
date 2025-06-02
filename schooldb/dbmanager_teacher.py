
import connection
import pandas as pd
from Teacher import Teacher
from dbmanager_lesson import lessonDbmanager

lesson_db=lessonDbmanager()



class tchDbManager:

    def __init__(self):
        self.connection=connection.mydb
        self.cursor=self.connection.cursor()

    def getallteacher(self):
        sql="select id, name, surname, branch from teacher"
        self.cursor.execute(sql)
        try:
            obj=pd.DataFrame(self.cursor.fetchall(),columns=[i[0] for i in self.cursor.description])
            return obj
            
        except self.connector.Error as err:
            print(f'Error: {err}')


    def getteacherbyId(self, Id):
        sql="select * from teacher where id=%s"
        values=(Id,)
        self.cursor.execute(sql, values)
        try:
            obj=self.cursor.fetchone()
            print(obj)
            return Teacher(obj[0],obj[1],obj[2],obj[3],obj[4],obj[5])
        
        except self.connector.Error as err:
            print(f'Error: {err}')

    def getClasses(self):
        sql="select id, class from class"
        self.cursor.execute(sql)

        try:
            obj=pd.DataFrame(self.cursor.fetchall(),columns=[i[0] for i in self.cursor.description])
            obj.set_index('id', inplace=True)
            obj.index.name = None
            return print(obj)
        
        except self.connector.Error as err:
            print(f'Error: {err}')


    def teacherdataEntry(self):

        list=[]
        lesson_db.getallLesson()

        while True:
            id=None
            Branch=input('Enter teacher branchid:')
            Name=input('Enter teacher name:').capitalize()
            Surname=input('Enter teacher surname:').capitalize()
            while True:
                try:
                    date_str = input("Enter teacher birthdate(gg.aa.yyyy): ")
                    if date_str.strip() != '':
                        Birthday = connection.geburtsdatumÜberprüft(date_str)
                    break
                except ValueError as e:
                    print(f"Fehler: {e}")
            Gender=input('Enter teacher gender(M/F):').upper()

            list.append((id, Name , Surname, Birthday, Gender,  Branch))

            kontrol=input('Do you want to add another entry? (y/n)')

            if kontrol == 'n':
                if len(list) == 1:
                    teacher=Teacher(id, Name, Surname, Birthday, Gender, Branch)
                    self.addTeacher(teacher)
                else:
                    self.addTeachers(list)
                break



    def addTeacher(self, teacher:Teacher):
        sql= "INSERT INTO teacher (Branch, Name, Surname, Birthday, Gender) VALUES (%s, %s, %s, %s, %s)"
        value= (teacher.branch, teacher.name, teacher.surname, teacher.birthday, teacher.gender)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'{teacher.name} {teacher.surname} has been added to the database.')
    
        except self.connector.Error as err:
            print('Error:', err)

    def addTeachers(self, teachers):
        sql= "INSERT INTO teacher (id, Name, Surname, Birthday, Gender, Branch) VALUES (%s, %s, %s, %s, %s,%s)"
        values= teachers
        self.cursor.executemany(sql,values)

        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} people have been added to the database.')
            print('Added people:')
            print(pd.DataFrame(teachers))
        except self.connector.Error as err:
            print('Error:', err)


    def newdataUpdating(self, teacher:Teacher):
        print('Enter the data you want to change, leave blank for those you do not want to change.')
        lesson_db.getallLesson()
        a = input('Enter teacher branch:')
        if a.strip() != '':
            teacher.branch= int(a)
        
        b = input('Enter teacher name:')
        if b.strip() != '':
            teacher.name= b

        c = input('Enter teacher surname:')
        if c.strip() != '':
            teacher.surname = c

        while True:
            try:
                d = input("Enter teacher birthdate (gg.aa.yyyy): ")
                if d.strip() != '':
                    teacher.birthday = connection.geburtsdatumÜberprüft(d)
                break
            except ValueError as e:
                print(f"Fehler: {e}")
            
        e = input('Enter teacher gender (M/F):').upper()
        if e.strip() != '':
            teacher.gender = e

        self.editTeacher(teacher)

    def editTeacher(self, teacher:Teacher):

        sql='update teacher set branch=%s, name=%s, surname=%s, birthday=%s, gender=%s where id=%s'
        values=(teacher.branch, teacher.name, teacher.surname, teacher.birthday, teacher.gender, teacher.id)
        self.cursor.execute(sql, values)

        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} teacher is updated.')
        except self.connector.Error as err:
            print('Error:', err)


    def teacherInfo(self):
        values=None
        temp = input('Which information do you want to see?\n- Press 1 to see all teacher\n- Press 2 to see female teachers only\n- Press 3 to see male teachers only\n- Press 4 to see teacher by branch\nYour choice: ')
        if temp=='1':
            sql='Select t.id, t.name, t.surname, l.name as Branch from teacher as t left join lesson as l on t.branch=l.id '
        elif temp=='2':
            sql='Select id, Name, Surname, Branch from teacher where gender="K"'
        elif temp=='3':
            sql='Select id, Name, Surname, Branch from teacher where gender="E"'
        elif temp=='4':
            branch=input("Which subject's teachers would you like to see?")
            sql="select * from teacher where branch=%s"
            values=(branch,)
        
        try:
            if values:
                self.cursor.execute(sql,values)
            else:
                self.cursor.execute(sql)
            obj=pd.DataFrame(self.cursor.fetchall(), columns=[i[0] for i in self.cursor.description])
            obj.set_index('id', inplace=True)
            obj.index.name = None
            print(obj)
            #Ich wollte keine for-Schleife verwenden, weil es mit Pandas einfacher ist, die Daten als DataFrame zu sehen.

        except self.connector.Error as er:
            print('Fehler:', er)

    def deleteTeacher(self, id):
        sql= "delete from teacher where id=%s"
        value= (id,)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'Teacher {id} has been deleted from the database.')
    
        except self.connector.Error as err:
            print('Error:', err)

    def close(self):
        self.cursor.close()
        self.connection.close()
        print('Database connection has been closed.')


        
