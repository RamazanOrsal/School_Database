from dbmanager_student import stdDbManager
from dbmanager_teacher import tchDbManager
from dbmanager_class import classDbmanager
from dbmanager_lesson import lessonDbmanager
from dbmanager_weekly import WeeklyScheduleManager

weeklyProgram=WeeklyScheduleManager()
lesson_db=lessonDbmanager()
class_db=classDbmanager()
tch_db=tchDbManager()
std_db=stdDbManager()

def stdApp():      
    while True:
        wahl=input('*****\n1- Add student\n2- Show student Info\n3- Get or edit student\n4- Student delete\n5- Exit\nChoice:')

        if wahl=='5':
            std_db.close()
            break
        else:
            if wahl=='1':
                std_db.studentdataEntry()

            elif wahl=='2':
                std_db.studentInfo()
                
            
            elif wahl=='3':
                obje=input('Which student do you want to see? (Enter number):')
                data=std_db.getStudentbyNummer(obje)
                islem=input("Do you want to change the student's information? (y/n):")
                if islem == 'y':
                    std_db.newdataUpdating(data)

            elif wahl=='4':
                print('Which number student dou you want to delete?')
                temp=input('Enter student number:')
                std_db.deleteStudent(temp)

            else:
                print('You pressed a wrong key. Please try again.')

def tchApp():      
    while True:
        wahl=input('*****\n1- Add teacher\n2- Show teacher Info\n3- Get or Edit teacher\n4- Teacher delete\n5- Exit\nChoice:')

        if wahl=='5':
            tch_db.close()
            break
        else:
            if wahl=='1':
                tch_db.teacherdataEntry()

            elif wahl=='2':
                tch_db.teacherInfo()
                
            
            elif wahl=='3':
                obje=input('Which teacher do you want to see? (Enter id):')
                data=tch_db.getteacherbyId(obje)
                islem=input("Do you want to change the teacher's information? (y/n):")
                if islem == 'y':
                    tch_db.newdataUpdating(data)

            elif wahl=='4':
                print('Which id teacher dou you want to delete?')
                temp=input('Enter teacher id:')
                tch_db.deleteTeacher(temp)

            else:
                print('You pressed a wrong key. Please try again.')

def classApp():      
    while True:
        wahl=input('*****\n1- Add class\n2- Show classes Info\n3- Get or Edit class\n4- Class delete\n5- Exit\nChoice:')

        if wahl=='5':
            class_db.close()
            break
        else:
            if wahl=='1':
                class_db.classdataEntry()

            elif wahl=='2':
                class_db.getallClass()
                
            
            elif wahl=='3':
                obje=input('Which class do you want to see? (Enter id):')
                data=class_db.getclassbyId(obje)
                islem=input("Do you want to change the class's homeroom teacher? (y/n):")
                if islem == 'y':
                    class_db.newdataUpdating(data)

            elif wahl=='4':
                print('Which class dou you want to delete?')
                temp=input('Enter class id:')
                class_db.deleteClass(temp)

            else:
                print('You pressed a wrong key. Please try again.')

def lessonsApp():   

    while True:
        wahl=input('*****\n1- Add lesson\n2- Show lesson Info\n3- Get or Edit lesson\n4- Create a weekly class schedule\n5- Create a weekly class schedule\n6- Exit\nChoice:')

        if wahl=='6':
            lesson_db.close()
            break
        else:
            if wahl=='1':
                lesson_db.lessondataEntry()

            elif wahl=='2':
                lesson_db.getallLessonwithTeacher()
                
            elif wahl=='3':
                obje=input('Which class do you want to see? (Enter id):')
                data=lesson_db.getlessonbyId(obje)
                islem=input("Do you want to change the class's homeroom teacher? (y/n):")
                if islem == 'y':
                    lesson_db.newdataUpdating(data)

            elif wahl=='4':
                print('A new weekly class schedule is being created')
                weeklyProgram.whichSelect()   
            
            elif wahl=='5':
                print('Show the weekly class schedule')
                weeklyProgram.showWeeklyprogram() 

            else:
                print('You pressed a wrong key. Please try again.')


while True:
    print('Which action would you like to take?')
    select=input('*****\n1-For teacher\n2-For student\n3-For class\n4-For lessons\n5- Exit\nChoice:')
    if select=='5':
        break
    else:
        if select=='1':
            tchApp()

        elif select=='2':
            stdApp()
        
        elif select=='3':
            classApp()
        
        elif select=='4':
            lessonsApp()

        else:
            print('You pressed a wrong key. Please try again.')


