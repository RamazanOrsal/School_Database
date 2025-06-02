import mysql.connector
import connection
import pandas as pd
from Student import Student





class stdDbManager:

    def __init__(self):
        self.connection=connection.mydb
        self.cursor=self.connection.cursor()

    ###### For Student ######
    def getStudentbyNummer(self, nummer):
        sql="select * from student where studentnummer=%s"
        values=(nummer,)
        self.cursor.execute(sql, values)
        try:
            obj=self.cursor.fetchone()
            print(obj)
            return Student(obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6])
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    def getClasses(self):
        sql="select c.id, c.class, t.name , t.surname, t.branch from class as c left join teacher as t on c.teacherid=t.id "
        self.cursor.execute(sql)

        try:
            obj=pd.DataFrame(self.cursor.fetchall(),columns=[i[0] for i in self.cursor.description])
            obj.set_index('id', inplace=True)
            obj.index.name = None
            return print(obj)
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')


    def studentdataEntry(self):

        list=[]
        while True:
            self.getClasses()
            id=None
            classid=int(input('Which classes do you want to add new student:'))
            StudentNummer=int(input('Enter student number:'))
            Name=input('Enter student name:').capitalize()
            Surname=input('Enter student surname:').capitalize()
            while True:
                try:
                    date_str = input("Enter student birthdate(gg.aa.yyyy): ")
                    if date_str.strip() != '':
                        Birthday = connection.geburtsdatumÜberprüft(date_str)
                    break
                except ValueError as e:
                    print(f"Fehler: {e}")
            Gender=input('Enter student gender(M/F):').upper()

            list.append((id, StudentNummer,Name, Surname, Birthday, Gender, classid))

            kontrol=input('Do you want to add another entry? (y/n)')

            if kontrol == 'n':
                if len(list) == 1:
                    student=Student(id, StudentNummer, Name, Surname, Birthday,Gender, classid)
                    self.addStudent(student)
                else:
                    self.addStudents(list)
                break



    def addStudent(self, student:Student):
        sql= "INSERT INTO student (StudentNummer, Name, Surname, Birthday, Gender, Classid) VALUES (%s, %s, %s, %s, %s, %s)"
        value= (student.studentNummer, student.name, student.surname, student.birthday, student.gender, student.classid)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'{student.name} {student.surname} has been added to the database.')
    
        except mysql.connector.Error as err:
            print('Error:', err)

    def addStudents(self, students):
        sql= "INSERT INTO student (StudentNummer, Name, Surname, Birthday, Gender, Classid) VALUES (%s, %s, %s, %s,%s, %s)"
        values= students
        self.cursor.executemany(sql,values)

        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} people have been added to the database.')
            print('Added people:')
            print(pd.DataFrame(students))
        except mysql.connector.Error as err:
            print('Error:', err)


    def newdataUpdating(self, student:Student):
        print('Enter the data you want to change, leave blank for those you do not want to change.')
     
        b = input('Enter student name:')
        if b.strip() != '':
            student.name= b

        c = input('Enter student surname:')
        if c.strip() != '':
            student.surname = c


        while True:
            try:
                d = input("Enter student birthdate (gg.aa.yyyy): ")
                if d.strip() != '':
                    student.birthday = connection.geburtsdatumÜberprüft(d)
                break
            except ValueError as e:
                print(f"Fehler: {e}")
            
        e = input('Enter student gender (M/F):').upper()
        if e.strip() != '':
            student.gender = e

        a = input('Enter student classid:')
        if a.strip()  != '':
            student.classid = int(a)

        self.editStudent(student)

    def editStudent(self, student:Student):

        sql='update student set name=%s, surname=%s, birthday=%s, gender=%s, classid=%s where studentNummer=%s'
        values=(student.name, student.surname, student.birthday, student.gender, student.classid, student.studentNummer)
        self.cursor.execute(sql, values)

        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} student is updated.')
        except mysql.connector.Error as err:
            print('Error:', err)


    def studentInfo(self):
        values=None
        temp = input('Which information do you want to see?\n- Press 1 to see all students\n- Press 2 to see girls only\n- Press 3 to see boys only\n- Press 4 to see students by class\nYour choice: ')
        if temp=='1':
            sql='Select * from student'
        elif temp=='2':
            sql='Select Studentnummer, Name, Surname from student where gender="K"'
        elif temp=='3':
            sql='Select Studentnummer, Name, Surname from student where gender="E"'
        elif temp=='4':
            classid=input('Which class do you want to view the list for?\nFor 10-A enter 1\n For 10-B enter 2\nFor 10-C enter 3\nYour choice:')
            sql="select * from student where classid=%s"
            values=(classid,)
        
        try:
            if values:
                self.cursor.execute(sql,values)
            else:
                self.cursor.execute(sql)
            print(pd.DataFrame(self.cursor.fetchall(), columns=[i[0] for i in self.cursor.description]))
            #Ich wollte keine for-Schleife verwenden, weil es mit Pandas einfacher ist, die Daten als DataFrame zu sehen.

        except mysql.connector.Error as er:
            print('Fehler:', er)

    def deleteStudent(self, studentnummer):
        sql= "delete from student where studentnummer=%s"
        value= (studentnummer,)
        self.cursor.execute(sql,value)

        try:
            self.connection.commit()
            print(f'Student {studentnummer} has been deleted from the database.')
    
        except mysql.connector.Error as err:
            print('Error:', err)

    def close(self):
        self.cursor.close()
        self.connection.close()
        print('Database connection has been closed.')







        
