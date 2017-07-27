#!/usr/bin/env 

# Script that build a sqlite db with information of the website http://cmireb.be

import urllib.request
import re
import sqlite3
import datetime
import hashlib
import os
import wikipedia
import csv
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

composerManager = []
OeuvreManager = []
ActivitiesManager = []
universal_ID = 8765
directory_raw_info = "raw_data"
issue = ""
def get_a_id():
    global universal_ID
    universal_ID += 1;
    return universal_ID;

def get_composer(url):
    if not os.path.exists(directory_raw_info):
        os.makedirs(directory_raw_info)
    if not os.path.exists(directory_raw_info+"/c"):
        os.makedirs(directory_raw_info+"/c")
    return get_data(url,"c/")

def get_oeuvre(url):
    if not os.path.exists(directory_raw_info):
        os.makedirs(directory_raw_info)
    if not os.path.exists(directory_raw_info+"/o"):
        os.makedirs(directory_raw_info+"/o")
    return get_data(url,"o/")
    
    
def get_data(url,o_dir):    
    file_name = hashlib.sha224(url.encode('utf-8')).hexdigest()
    if os.path.isfile(directory_raw_info+"/"+o_dir+file_name):
        F = open(directory_raw_info+"/"+o_dir+file_name,"r")
        return F.read()
    else:
        opener = urllib.request.FancyURLopener({})       
        f = opener.open(url)
        content = f.read()
        F = open(directory_raw_info+"/"+o_dir+file_name,"wb")
        F.write(content)
        return content


def replace_letter(strg):
    global issue
    a = strg.strip()
    if a == "PremiÃ¨re Ã©preuve"   : a = "Première épreuve"
    if a == "Michael Ponti"        : a = "Michaël Ponti"
    if a == "Lukas Vondracek"      : a = "Lukáš Vondráček"
    if a == "Pierre Volondat"      : a = "Pierre-Alain Volondat"
    if a == "Mikhail Faerman"      : a = "Mikhaïl Faerman"
    if a == "Eketarina Novitzkaya" : a = "Ekaterina Novitskaya"
    if a == "Concert de lauréats"  : a = "Concert de lauréats"
    if a == "Récital du prix Musiq'3"  : a = "Récital du prix Musiq3"
    if a == "Zbigniew Tursky"      : a = "Zbigniew Turski"
    if a == "Emil Guilels"          : a = "Emil Gilels"
    
    a = a.replace("Ã©","é").replace("Ã¨","è").replace('”','').replace('“','').replace('Ã¿','ÿ').replace("Ã§","ç").replace("Ã¢","â").replace("Ã«","ë").replace('Ã¶','ö').replace('Ã³','ó').replace('Ã±','ñ').replace('Ã¯','ï').replace(' - récital','')
    if re.search('[^0-9a-zA-Zû\ \.éèêë\-aáà\:uù\,óůü\/\(\)\?ôçö&\!üïÜÖîœääìÿòřáěčÈòÁıöŞł…ÔřáířáÉ\'ñﬂý°\[\]¿\%ßFånämöŒøâme∆ÈÏ’ÄúlÀ\–Ž«»`ňáąCançãoGarõaŠirokérukáširt’s ‘igaroyžmná’!Dzieciątkomójmaleńki]+', a) is not None:
        print("\n\n->",a,"\n\n")
        issue+= "\n"+a
    return a;

class Activities : 
    def __init__(self,musicien_nom,oeuvre_link,annee,classement):
        self.id = get_a_id()
        self.oeuvre = oeuvre_link
        self.annee = annee
        self.nom_musicien =replace_letter(musicien_nom)
        self. classement = replace_letter(classement)
        
    def __str__(self):
        return  str("+++id "             + str(self.id)   +"\n"+
                "+++self.oeuvre.id"  + str(self.oeuvre.id)+"\n"+
                "+++self.annee"      + str(self.annee)    +"\n"+
                "+++self.classement" +str(self.classement)+"\n")

class Composer : 
    
    def __init__(self,name,composer_link,f):
        self.id = get_a_id()
        self.url = composer_link
        self.name = replace_letter(name)
        self.oeuvres = [f]
        self.birth = ""
        self.death = ""   
        self.wikipedia_url = ""
        self.content = get_composer(self.url)
        try:
            self.content= self.content.decode("utf-8")
        except AttributeError:
            pass    
        m = re.search('°(?P<b>\d+) \- †(?P<d>\d+)', self.content)   
        try :       
            self.birth = m.group("b")
            self.death = m.group("d")
        except AttributeError:
            try : 
                m = re.search('<div>°(?P<b>\d+)', self.content)   
                self.birth = m.group("b")
                self.death = ""            
#               print(self.birth, self.death, ':',self.name,self.url)
            except AttributeError:
                try : #Isaac Manuel Francisco Albéniz y Pascual (Spanish pronunciation: [iˈsaːk alˈβeniθ]; 29 May 1860 – 18 May 1909)
                    d = wikipedia.summary(self.name+ " classical", 2)
                    m = re.search('\d\d? .* (?P<birth>\d+) – \d\d? .* (?P<death>\d+)\)', d)
                    self.birth = m.group("birth")
                    self.death = m.group("death")    
                except Exception:
                    try :
                        m = re.findall('1\d\d\d', d)
                        print(self.name,m, d)
                        if(len(m) == 0) :     
                            print("NOT FOUND")
                        else :
                            self.birth = m[0]
                            if(len(m) > 1) : self.death = m[1]               
                    except Exception as e:                         
                        print("exeption line 131  ",self.name,"  ", e)
        self.oeuvres = [f]

    
    def __str__(self):
        return str( "++name :"     + str(self.name)+"\n" +
                    "++birth :"   + str(self.birth)+"\n"+
                    "++death :"   + str(self.death)+"\n"+
                    "++url   :"   + str(self.url)+ "\n"+  
                    "++oeuvres :" + str(self.oeuvres)+"\n")
  
    
    def addOeuvre(self,f):
        self.oeuvres.append(f)
    
class CREOeuvre :     
    def __init__(self,page_number):
        self.id = get_a_id();
        self.page_number = page_number
        self.url_oeuvre  = "http://cmireb.be/cgi?lg=fr&pag=1942&tab=227&rec="+str(page_number)+"&frm=0&par=secorig1656"
        #print(self.url_oeuvre)
        self.content = get_oeuvre(self.url_oeuvre)
       # print(self.content)
        self.parsed_html = BeautifulSoup(self.content,"html.parser")        
        self.oeuvre_name = replace_letter(self.getOeuvreName())
        self.composer_name = replace_letter(self.getcomposer())
        self.instruments = self.getInstruments()
        self.composer_link = self.getcomposerLink()
        self.activities = self.getActivities()  
      
        if self.composer_link != None :
            f =  [elem for elem in composerManager if elem.name == self.composer_name]
            assert(len(f) <= 1)

            if len(f) == 0 :
                self.composer_object = Composer(self.composer_name,self.composer_link,self)
                composerManager.append(self.composer_object);
            else :
                self.composer_object = f[0]
                f[0].addOeuvre(self);
            
        

    def __str__(self):
        return str( "page_number :"     + str(self.page_number)+"\n" +
                    "oeuvre_name :"     + str(self.oeuvre_name)+"\n" +
                    "composer  :"     + str(self.composer_name)+"\n" +
                    "instruments :"     + str(self.instruments)+"\n" +
                    "oeuvre_url  :"     + str(self.url_oeuvre)+"\n" +
                    "composer_link :" + str(self.composer_link)+"\n" +
                    "activities :"      + str(self.activities)+"\n" +
                    "composer : \n"    + str(self.composer_object)+"\n" )
#http://cmireb.be/cgi?lg=fr&pag=1698&tab=102&rec=1013&frm=0
#http://cmireb.be/cgi?lg=fr&pag=1942&tab=227&rec=417&frm=0&par=secorig1656
 #   def getCREOeuvre(self):
#        opener = urllib.request.FancyURLopener({})       
#        f = opener.open(self.url_oeuvre)
#        content = f.read()
#        return content

    def getOeuvreTitle(self):
        return self.parsed_html.body.find('div',{"class":"exotique TitrePage"}).text.replace('<div class="exotique TitrePage">','').replace('</div>','')

    def getOeuvreName(self):
        return self.getOeuvreTitle().split(':',1)[1].strip().replace('"',"").replace("'","")
    
    def getcomposer(self):
        return self.getOeuvreTitle().split(':',1)[0].strip()
     
        
    
    def getInstruments(self):
        table = self.parsed_html.body.find('table',{"class":"listeInstruments"})
        row_data = []
        try :
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                if len(cols) == 1 : continue;
                row_data.append(cols)
        except Exception:
            return row_data
        return row_data
    
    def getcomposerLink(self):
        table = self.parsed_html.body.find('table',{"class":"listeFonctions"})
        if table == None : return None

        #<a href="/cgi?lg=fr&amp;pag=1698&amp;tab=102&amp;rec=1316&amp;frm=0">Maurice Ravel</a></td> <td class="col2">Compositeur</td>
        #a = str(table.find("a")).split('"')[1].replace ("&amp;","&")       
        for tr in table.find_all('tr')[2:]:
            tds = tr.find_all('td')
            for i in range(0,len(tds)) :
                if tds[i].text == "Compositeur" :
                    url = tds[0].a.get('href')
                    return "http://cmireb.be"+url
        for tr in table.find_all('tr')[2:]:
            tds = tr.find_all('td')
            for i in range(0,len(tds)) :
                if tds[i].text == "Auteur" :
                    url = tds[0].a.get('href')
                    return "http://cmireb.be"+url
                
        a = str(table.find("a")).split('"')[1].replace ("&amp;","&") 
        return "http://cmireb.be/"+a
            
    #listeActivites
    def getActivities(self):  
        global issue
        table = self.parsed_html.body.find('table',{"class":"listeActivites"})
        row_data = []
        if table == None : 
        #    print ("TABLE NULLE->", self.url_oeuvre)
            return row_data
        for row in table.find_all("a"):
            try :
                #print(row.text)
                m = re.search('(?P<cla>.+) (?P<date>\d\d\d\d) : (?P<pl>.+)', row.text)
                if m != None :
                    a = Activities(m.group("pl"),self,m.group("date"),m.group("cla"))
                    row_data.append(a)
                    ActivitiesManager.append(a)
    #             print("->",row_data)
                else :
                    m = re.search('(?P<cla>.+)(?P<date>\d\d\d\d)', row.text)
                    a = Activities("",self,m.group("date"),m.group("cla"))
                    row_data.append(a)
                    ActivitiesManager.append(a)
            except AttributeError as err:                
                print(row.text)
                issue += "AttributeError : LINE(192) " + row.text
                continue
        return row_data


if __name__ == "__main__":
    print(str(datetime.datetime.today()))
    conn = sqlite3.connect('CRE.db')
    c = conn.cursor()

    
    c.execute("CREATE table winners (annee ,first,second,third,fourth,fifth,categorie)") # use your column names here

    with open('Winners.csv') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.reader(fin) # comma is default delimiter
        for r in dr : 
            e = 'INSERT INTO winners VALUES ("'+'","'.join([x.strip() for x in r])+'")'
            c.execute(e)

            
    c.execute("CREATE table categories (annee ,name)") # use your column names here
    with open('Categories.csv') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.reader(fin) # comma is default delimiter
        for r in dr : 
            e = 'INSERT INTO categories VALUES ("'+'","'.join([x.strip() for x in r])+'")'
            c.execute(e)

            
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS oeuvres(id,page_number,oeuvre_name,composer_name, composer_id,oeuvre_link)''')
    c.execute('''CREATE TABLE IF NOT EXISTS instruments(id,oeuvre_id,instrument,role,type)''')
    c.execute('''CREATE TABLE IF NOT EXISTS activities(id,oeuvre_id,annee,nom_musicien,classement)''')
    c.execute('''CREATE TABLE IF NOT EXISTS composers(id,name,birth,death,url,wikipediaUrl)''')
    c.execute('''CREATE TABLE IF NOT EXISTS linktableOC(composer_id,oeuvres_id)''')
    
    for i in range (1,9000):
            o = CREOeuvre(i);
            if o.oeuvre_name.strip() != "" and o.composer_link != None:
                OeuvreManager.append(o)
            
    for e in OeuvreManager:
        if e == None : 
            print("oeuvre None")
            continue
        c.execute('INSERT INTO oeuvres VALUES ("' + '","'.join([str(e.id),str(e.page_number),e.oeuvre_name,e.composer_name,str(e.composer_object.id),str(e.url_oeuvre)])+ '")')
        
        c.execute("INSERT INTO linktableOC Values ("'"'  + '","'.join([str(e.composer_object.id),str(e.id)])   +'")')
        
        for i in e.instruments:
            if i == None : continue
            c.execute('INSERT INTO instruments Values("' + '","'.join([str(get_a_id()),str(e.id),i[0],i[1],i[2]])+ '")')
        
    
    for e  in composerManager:
        if e == None : continue
        c.execute( 'INSERT INTO composers VALUES ("' + '","'.join([str(e.id),e.name,str(e.birth),str(e.death),e.url,e.wikipedia_url])+'")')

    for e  in ActivitiesManager:
        if e == None : continue
        c.execute( 'INSERT INTO activities VALUES ("' + '","'.join([str(e.id),str(e.oeuvre.id),str(e.annee),str(e.nom_musicien),e.classement])+'")')

    c.execute ('''create view global_stat as select "nombre de compositeurs",count(*) from composers
union
select "nombre d'oeuvres",count(*) from oeuvres
union
select "nombre de compositeurs (birth != null)",count(*) from composers where birth != ""
union
select "nombre de compositeurs Piano ",count(*) from composers where  id 
in (select composer_id from instruments, oeuvres, composers where instruments.oeuvre_id = oeuvres.id and composers.id = oeuvres.composer_id  and instrument = "piano")
union
select "nombre de compositeurs Piano (birth != null)",count(*) from composers where birth != "" and id 
in (select composer_id from instruments, oeuvres, composers where instruments.oeuvre_id = oeuvres.id and composers.id = oeuvres.composer_id and birth != ""  and instrument = "piano")
union
select "nombres de sonates (Piano)", count(*) from oeuvres where oeuvres.id in 
(select oeuvre_id from instruments, oeuvres, composers where instruments.oeuvre_id = oeuvres.id and composers.id = oeuvres.composer_id and birth != ""  and instrument = "piano" and oeuvre_name like "%sonate%")
union
select "nombres de concerto (Piano)", count(*) from oeuvres where oeuvres.id in 
(select oeuvre_id from instruments, oeuvres, composers where instruments.oeuvre_id = oeuvres.id and composers.id = oeuvres.composer_id and birth != ""  and instrument = "piano" and oeuvre_name like "%concerto%")''')
    
    c.execute('''create view W2 as select * from activities where nom_musicien in( select first from winners) and classement = "Finale"''')
    
    c.execute('''create view winnerOeuvre  as select * from activities,oeuvres where nom_musicien in( select first from winners) and  oeuvre_id = oeuvres.id and annee in (select annee from categories where  name = "Piano") and classement = "Finale" order by  cast (annee as INT)
''')
    
    c.execute('''create view  stat_composer_winner as select composer_name, count(*) as c from winnerOeuvre group by composer_name order by c desc ''')
    c.execute('''create view  stat_composer_Final as select composer_name,count (*)  as c from activities, oeuvres where oeuvres.id = activities.oeuvre_id  and classement in ("Finale") group by composer_name order by c desc''')
    c.execute('''create view  stat_composer_Demi_Final as select composer_name,count (*)  as c from activities, oeuvres where oeuvres.id = activities.oeuvre_id  and classement in ("Demi-finale") group by composer_name order by c desc''')
    c.execute('''create view  stat_composer_Premiere_ep as select composer_name,count (*)  as c from activities, oeuvres where oeuvres.id = activities.oeuvre_id  and classement in ("Première épreuve") group by composer_name order by c desc''')

    c.execute('''create view winnerConcerto as   select * from activities,oeuvres where nom_musicien in( select first from winners) and  oeuvre_id = oeuvres.id and annee in (select annee from categories where  name = "Piano") and classement = "Finale" and oeuvre_name like "%Concerto%" ''')
    conn.commit()
    conn.close()
    print(issue)
    print(str(datetime.datetime.today()))

    
    
    