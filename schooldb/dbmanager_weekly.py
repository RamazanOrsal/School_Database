from datetime import datetime
import connection
import pandas as pd
from weekly_schedule import WeeklySchedule

 

class WeeklyScheduleManager:

    

    def __init__(self):
        self.connection=connection.mydb
        self.cursor=self.connection.cursor()



        sql_lesson='Select * From lesson'
        self.cursor.execute(sql_lesson)
        self.lesson_map = { row[1] : row[0] for row in self.cursor.fetchall() }


        sql_tch='Select t.id, l.name as lesson From teacher as t right join lesson as l on t.branch=l.id'
        self.cursor.execute(sql_tch)
        self.teacher_map = {row[1]: row[0] for row in self.cursor.fetchall()}
        

        sql_klasse='Select * from class'
        self.cursor.execute(sql_klasse)
        self.class_map= { (row[1], row[2]): row[0] for row in self.cursor.fetchall() }
        

        self.tch_clss_match={'9':(1, 'Matematik'), '10': (14, 'Matematik')}

        self.weeklyProgram = pd.DataFrame()




    def newweeklyplanMade(self):
        while True:
            try:
                weeklyProgram=WeeklySchedule()
                teacher_Kontrollist, schoolProgram = weeklyProgram.stundenplanErstellenFürKlassen()   
                break                 
            except Exception as e:
                print(e)
                print("❌ Hata oluştu. Program yeniden başlatılıyor...\n")
        
        print(schoolProgram)
        self.weeklyProgram=self.widetolongConvert(schoolProgram)
        print(self.weeklyProgram.head(30))

    def widetolongConvert(self,df):
        days_map = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
        df_long=df.melt(id_vars=["Stunde", "Klass"], var_name="Day", value_name="Subject"  )
        df_long['Day'] = df_long['Day'].map(days_map)
        df_long['Klass_level'] = df_long['Klass'].apply(lambda x: str(x[0])) 
        df_long['Klass']=df_long['Klass'].map(self.class_map)
        df_long['Teacher']=df_long['Subject'].map(self.teacher_map)
        for level, (teacher_id, subject) in self.tch_clss_match.items():
            df_long.loc[(df_long['Subject'] == subject) & (df_long['Klass_level'] == level), 'Teacher'] = teacher_id
        
        df_long['Subject']=df_long['Subject'].map(self.lesson_map)
        df_long = df_long.drop('Klass_level', axis=1)
        return df_long
    
    
    def saveProgram(self):
        self.cursor.execute("DELETE FROM weekly_schedule")
        liste=[]
        for row in self.weeklyProgram.itertuples(index=False):
            liste.append(tuple(row))
        
        sql= "INSERT INTO weekly_schedule (hour, classId, day, lessonid, teacherid) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.executemany(sql,liste)

        try:
            self.connection.commit()
            print(f'The program has been added to the database.')
    
        except self.connector.Error as err:
            print('Error:', err)

    def showWeeklyprogram(self):
        sql = """
                SELECT 
                    CONCAT(c.Grade, " " ,c.Section) AS Class,
                    ws.day,
                    ws.hour,
                    l.name AS lesson_name,
                    CONCAT(t.name, " " ,t.surname) AS teacher
                FROM 
                    weekly_schedule as ws
                LEFT JOIN 
                    class as c ON ws.classId = c.id
                LEFT JOIN 
                    lesson as l ON ws.lessonid = l.id
                LEFT JOIN 
                    teacher as t ON ws.teacherid = t.id
                """
        self.cursor.execute(sql)
        df_program=pd.DataFrame(self.cursor.fetchall(), columns=['Class', 'Day', 'Hour', 'Lesson', 'Teacher'])
        df_program['Lesson_Teacher'] = df_program['Lesson'] +  chr(10) + df_program['Teacher']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for className, group in df_program.groupby('Class'):
            print(className)
            pivot_df = group.pivot(index='Hour', columns='Day', values='Lesson_Teacher')
            pivot_df=pivot_df[days]
            pivot_df.to_excel(f"{className}.xlsx")
            print(pivot_df)
        


    
    
    def whichSelect(self):
        self.newweeklyplanMade()
        while True:
            print('Which action would you like to take?')
            select=input('*****\n- Press 1 to save the Program\n- Press 2 to show the weekly class schedule\n- Press 3 für exit\nChoice:')
            if select=='3':
                break
            else:
                if select=='1':
                    self.saveProgram()
                elif select=='2':
                    self.showWeeklyprogram()
                else:
                    print('You pressed a wrong key. Please try again.')


    

    


    

# a=WeeklyScheduleManager()
# a.newweeklyplanMade()



