import pandas as pd
import connection
import random


class WeeklySchedule:

    def __init__(self):
        self.connection=connection.mydb
        self.cursor=self.connection.cursor()
        self.unterricht_stunde = {
                "Matematik": 7,
                "Fizik": 5,
                "Kimya": 4,
                "Biyoloji": 4,
                "Tarih": 3,
                "Cografya": 2,
                "Edebiyat": 3,
                "Türkce": 2
            }
        

        sql_tch='Select t.id, CONCAT(t.name, " " ,t.surname) as teacher, l.name as lesson From teacher as t right join lesson as l on t.branch=l.id'
        self.cursor.execute(sql_tch)
        tch_df=pd.DataFrame(self.cursor.fetchall())
        tch_dict = { (row[0], row[2]) : row[1] for row in tch_df.itertuples(index=False) }
        self.tchList=tch_dict
        #burda ögretmenleri id ve branslarina göre sözlükte tutuyorum


        sql_klasse='Select * from class'
        self.cursor.execute(sql_klasse)
        klasse_df=pd.DataFrame(self.cursor.fetchall())
        klasselist = { (row[1], row[2]) for row in klasse_df.itertuples(index=False) }
        self.klasseList=klasselist # Burada sinif ve subeleri ayarladim.

        satirlar = []

        for klass in self.klasseList:
            for stunde in range(6):
                satir = {
                    'Stunde': stunde+1,
                    1: pd.NA,
                    2: pd.NA,
                    3: pd.NA,
                    4: pd.NA,
                    5: pd.NA,
                    'Klass': klass
                }
                satirlar.append(satir)
        self.klass_kont_df = pd.DataFrame(satirlar)


        self.tch_clss_match={'9':(1, 'Matematik'), '10': (14, 'Matematik')} 
        #Bunu manuel olarak atadim cünkü elimizde zaten 2 tane mateamtikci var ve digerleri her sinifa girecek bunu bu sekilde manuel atabiliriz.


        tch_kont_dict={}
        for teacherid in self.tchList:
            tch_kont_dict[teacherid] =[(h, g) for h in range(1, 7) for g in range(1, 6)]
        self.tch_kontrol_df=pd.DataFrame(tch_kont_dict, index=None)
        #ögretmenlerin bosluklarini kontrol etmek amaci ile yapildi. her ders eklemesinde listeden eleman silinecek ve kontrol daha kolay olacak



        
    
    def stundenplanErstellenFürKlassen(self):
        
        for i in range(2):
            if i==0:
                for klass in self.klasseList:
                    einzelUnterricht, doppelstundeUnterricht = self.unterrichsPlan()
                    lehrkraftKontrollist=self.lehrerChecklist(klass[0])
                    self.eintragenEinzelstunden(einzelUnterricht, lehrkraftKontrollist, klass)

            else:
                einzelUnterricht, doppelstundeUnterricht = self.unterrichsPlan()
                for i in range(len(doppelstundeUnterricht)):
                    unterricht, stunde= doppelstundeUnterricht[i]

                    for klass in self.klasseList:
                        lehrkraftKontrollist=self.lehrerchecklistNachunterricht(unterricht, klass)
                        self.eintragenDoppelstundenProFach(unterricht, stunde, lehrkraftKontrollist, klass)
                        

        return self.tch_kontrol_df, self.klass_kont_df
 




    def lehrerchecklistNachunterricht(self, unterricht, klass):

        spezifischer_lehrer = self.tch_clss_match[klass[0]]

        if spezifischer_lehrer[1] == unterricht:
            return self.tch_kontrol_df[spezifischer_lehrer]
        
        passende_lehrer = [lehrkraft for lehrkraft in self.tchList if lehrkraft[1] == unterricht]
        
        return self.tch_kontrol_df[passende_lehrer[0]]



    def lehrerChecklist(self, klass):
        andre_klass='10'
        if klass == '9':
            unerwunschter_Lehrkraft=self.tch_clss_match[andre_klass]
        elif klass =='10':
            andre_klass='9'
            unerwunschter_Lehrkraft=self.tch_clss_match[andre_klass]
        
        lehrerkontrollist=self.tch_kontrol_df.drop(unerwunschter_Lehrkraft,axis=1)
        lehrerkontrollist.columns = [col[1] for col in lehrerkontrollist.columns]

        return lehrerkontrollist



    def unterrichsPlan(self):
        einzel_unterricht=[]
        doppelstunde_unterricht=[]
        for unterricht, stunde in self.unterricht_stunde.items():
            if stunde%2==0:
                doppelstunde_unterricht.append((unterricht,stunde))
            else:
                einzel_unterricht.append(unterricht)
                stunde-=1
                doppelstunde_unterricht.append((unterricht, stunde))
        return einzel_unterricht, doppelstunde_unterricht
     


    def eintragenEinzelstunden(self, einzelUnterricht, lehrkraftKontrollist, klass):
  
        random.shuffle(einzelUnterricht)
        for i in range(len(einzelUnterricht)//2):
            while True:
                passend_tag_lehrer1=random.choice(lehrkraftKontrollist[einzelUnterricht[0]][lehrkraftKontrollist[einzelUnterricht[0]].notna()].tolist())
                stunde1, tag1 = passend_tag_lehrer1

                if stunde1%2==0:
                    passend_tag_lehrer2 = lehrkraftKontrollist[einzelUnterricht[1]][lehrkraftKontrollist[einzelUnterricht[1]].apply(lambda x: x == (stunde1-1, tag1) if pd.notna(x) else False)]

                else:
                    passend_tag_lehrer2 = lehrkraftKontrollist[einzelUnterricht[1]][lehrkraftKontrollist[einzelUnterricht[1]].apply(lambda x: x == (stunde1+1, tag1) if pd.notna(x) else False)]

            
                ist_leer=self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde1), tag1].isna().values[0]

                if not passend_tag_lehrer2.empty and ist_leer:
                    stunde2, tag2 = passend_tag_lehrer2.iloc[0]
                    break
                else:
                    continue

                
            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde1), tag1] = einzelUnterricht[0]
            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde2), tag2] = einzelUnterricht[1]
           
            
            lehrkraftKontrollist.loc[lehrkraftKontrollist[einzelUnterricht[0]] == (stunde1, tag1), einzelUnterricht[0]] = pd.NA
            lehrkraftKontrollist.loc[lehrkraftKontrollist[einzelUnterricht[1]] == (stunde2, tag2), einzelUnterricht[1]] = pd.NA

            del einzelUnterricht[:2]
                
        self.vollzelleLöschenvonTchlistfürEinzel(lehrkraftKontrollist,klass[0])


    def eintragenDoppelstundenProFach(self, unterricht, stunde, lehrkraftKontrollist, klass):

        tages=[1,2,3,4,5]

        sayac=stunde//2
   
        passend_tag=self.geeigneteTageFürKlasseUndLehrkraft(tages, sayac, unterricht, klass, lehrkraftKontrollist)
        passend_leer_zeele=[]

        versucht=0
        maxversucht=20


        while versucht<=maxversucht:

            for g in passend_tag:

                passend_tag_lehrer=lehrkraftKontrollist[lehrkraftKontrollist.notna()].tolist()
                
                passend=[h for h in passend_tag_lehrer
                        if h[1] == g and self.klass_kont_df.loc[
                            (self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == h[0]), g].isna().values[0]
                ]
                

                random.shuffle(passend)

                for stunde, tag in passend:
                    if stunde % 2 == 0:
                        if (any(x == (stunde - 1, tag) for x in passend_tag_lehrer) and
                            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde), tag].isna().values[0] and
                            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde - 1), tag].isna().values[0]):
                            passend_leer_zeele.append((stunde, tag))
                            passend_leer_zeele.append((stunde - 1, tag))
                            break
                    else:
                        if (any(x == (stunde + 1, tag) for x in passend_tag_lehrer) and
                            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde), tag].isna().values[0] and
                            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == stunde + 1), tag].isna().values[0]):
                            passend_leer_zeele.append((stunde, tag))
                            passend_leer_zeele.append((stunde + 1, tag))
                            break
                else:
                    continue

            if  len(passend_leer_zeele)>=sayac*2:
                break        
            else:
                passend_leer_zeele.clear()
                versucht+=1
                passend_tag=self.geeigneteTageFürKlasseUndLehrkraft(tages, sayac, unterricht, klass, lehrkraftKontrollist)
        
        if versucht > maxversucht:
            raise Exception(f"{klass} için {unterricht} dersi yerleştirilemedi.")
            
        self.vollzelleLöschenvonTchlistfürDoppel(lehrkraftKontrollist, passend_leer_zeele)
        
        
          
            
        for i in passend_leer_zeele:
            self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass) & (self.klass_kont_df['Stunde'] == i[0]), i[1]] = unterricht
  
        tages=self.vollColumns(self.klass_kont_df, tages, klass) 
        
     


    def vollColumns(self, klass_kont_df, tages, klass):

        voll_columns=klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass)]

        passend_tages = [g for g in tages if voll_columns[g].isna().any()]

        return passend_tages
    


    def geeigneteTageFürKlasseUndLehrkraft(self, tages, sayac, unterricht, klass, lehrkraftKontrollist):
        versucht=0
        maxversucht=20
        while versucht<=maxversucht:
            passend_tag=random.sample(tages, sayac)
            for i in passend_tag:
                kontrol=self.klass_kont_df.loc[(self.klass_kont_df['Klass'] == klass), i]
                if kontrol.isin([unterricht]).any():
                    break

                if kontrol.isna().sum() < 2:
                    break

                lehr_stunden = [tup for tup in lehrkraftKontrollist if tup is not None and pd.notna(tup) and tup[1] == i]
                if len(lehr_stunden) < 2:
                    break

            else:
                return passend_tag       
  
            versucht+=1
        raise Exception(f"{klass} için '{unterricht}' için uygun günler bulunamadı.")
    
    
    def vollzelleLöschenvonTchlistfürEinzel(self, lehrerkontrollist, klass):

        if klass=='9':
            ogretmen=self.tch_clss_match[klass]
            self.tch_kontrol_df[ogretmen]=lehrerkontrollist['Matematik']

        elif klass=='10':
            ogretmen=self.tch_clss_match[klass]
            self.tch_kontrol_df[ogretmen]=lehrerkontrollist['Matematik']

        for ders in lehrerkontrollist.columns:
            istenenstun=[xyz for xyz in self.tch_kontrol_df.columns if ders==xyz[1] ]
               
            if ders == 'Matematik':
                pass
            else:
                self.tch_kontrol_df[istenenstun[0]]=lehrerkontrollist[ders]
    

    def vollzelleLöschenvonTchlistfürDoppel(self, lehrkraftKontrollist, passend_leer_zeele):

        
        lehrkraftKontrollist = lehrkraftKontrollist[~lehrkraftKontrollist.isin(passend_leer_zeele)]
        name=lehrkraftKontrollist.name
        self.tch_kontrol_df[name]=lehrkraftKontrollist
   
