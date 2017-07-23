#!/usr/bin/env 

# Script that build a sqlite db with information of the website http://cmireb.be

import urllib.request
import re
import sqlite3
import datetime
import hashlib
import os

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

CompositorManager = []
OeuvreManager = []
ActivitiesManager = []
universal_ID = 8765
directory_raw_info = "raw_data"
issue = ""
def get_a_id():
    global universal_ID
    universal_ID += 1;
    return universal_ID;

def get_data(url):
    if not os.path.exists(directory_raw_info):
        os.makedirs(directory_raw_info)
    file_name = hashlib.sha224(url.encode('utf-8')).hexdigest()
    if os.path.isfile(directory_raw_info+"/"+file_name):
        F = open(directory_raw_info+"/"+file_name,"r")
        return F.read()
    else:
        print("download")
        opener = urllib.request.FancyURLopener({})       
        f = opener.open(url)
        content = f.read()
        F = open(directory_raw_info+"/"+file_name,"wb")
        F.write(content)
        return content


def replace_letter(strg):
    global issue
    a = strg.strip()
    if a == "PremiÃ¨re Ã©preuve" : a = "Première épreuve"
    if a == "Michael Ponti"      : a = "Michaël Ponti"
    if a == "Lukas Vondracek"    : a = "Lukáš Vondráček"
    if a == "Pierre Volondat"    : a = "Pierre-Alain Volondat"
    if a == "Mikhail Faerman"    : a = "Mikhaïl Faerman"
    if a == "Eketarina Novitzkaya" : a = "Ekaterina Novitskaya"
    
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

class Compositor : 
    
    def __init__(self,name,compositor_link,f):
        self.id = get_a_id()
        self.url = compositor_link
        self.name = replace_letter(name)
        self.oeuvres = [f]
        self.birth = ""
        self.death = ""        
        self.content = get_data(self.url)
        try:
            self.content= self.content.decode("utf-8")
        except AttributeError:
            pass
            #
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
                self.oeuvres = [f]
            except AttributeError:
                self.birth = ""
                self.death = ""            
                self.oeuvres = [f]
                
#    def getCRECompositor(self):
#        opener = urllib.request.FancyURLopener({})       
#        f = opener.open(self.url)
#        content = f.read()
#        return content
    
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
        
        print(self.url_oeuvre)
        self.content = get_data(self.url_oeuvre)
       # print(self.content)
        self.parsed_html = BeautifulSoup(self.content,"html.parser")        
        self.oeuvre_name = replace_letter(self.getOeuvreName())
        self.compositor_name = replace_letter(self.getCompositor())
        self.instruments = self.getInstruments()
        self.compositor_link = self.getCompositorLink()
        self.activities = self.getActivities()  
      
        if self.compositor_link != None :
            f =  [elem for elem in CompositorManager if elem.name == self.compositor_name]
            assert(len(f) <= 1)

            if len(f) == 0 :
                self.compositor_object = Compositor(self.compositor_name,self.compositor_link,self)
                CompositorManager.append(self.compositor_object);
            else :
                self.compositor_object = f[0]
                f[0].addOeuvre(self);
            
        

    def __str__(self):
        return str( "page_number :"     + str(self.page_number)+"\n" +
                    "oeuvre_name :"     + str(self.oeuvre_name)+"\n" +
                    "compositor  :"     + str(self.compositor_name)+"\n" +
                    "instruments :"     + str(self.instruments)+"\n" +
                    "oeuvre_url  :"     + str(self.url_oeuvre)+"\n" +
                    "compositor_link :" + str(self.compositor_link)+"\n" +
                    "activities :"      + str(self.activities)+"\n" +
                    "compositor : \n"    + str(self.compositor_object)+"\n" )
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
    
    def getCompositor(self):
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
    
    def getCompositorLink(self):
            table = self.parsed_html.body.find('table',{"class":"listeFonctions"})
            if table == None : return None
            a = str(table.find("a")).split('"')[1].replace ("&amp;","&")       
            assert(a != None)
            return "http://cmireb.be"+a
            
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

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS oeuvres(id,page_number,oeuvre_name,compositor_name, compositor_id,oeuvre_link)''')
    c.execute('''CREATE TABLE IF NOT EXISTS instruments(id,oeuvre_id,instrument,role,type)''')
    c.execute('''CREATE TABLE IF NOT EXISTS activities(id,oeuvre_id,annee,nom_musicien,classement)''')
    c.execute('''CREATE TABLE IF NOT EXISTS compositors(id,name,birth,death,url)''')
    c.execute('''CREATE TABLE IF NOT EXISTS linktableOC(compositor_id,oeuvres_id)''')
    
    count = 0
    for i in range (1,9000):
            o = CREOeuvre(i);
            if o.oeuvre_name.strip() != "" and o.compositor_link != None:
                OeuvreManager.append(o)
            else :
                count += 1
    print (count,"/",9000)
            
    for e in OeuvreManager:
        if e == None : 
            print("oeuvre None")
            continue
        c.execute('INSERT INTO oeuvres VALUES ("' + '","'.join([str(e.id),str(e.page_number),e.oeuvre_name,e.compositor_name,str(e.compositor_object.id),str(e.url_oeuvre)])+ '")')
        
        c.execute("INSERT INTO linktableOC Values ("'"'  + '","'.join([str(e.compositor_object.id),str(e.id)])   +'")')
        
        for i in e.instruments:
            if i == None : continue
            c.execute('INSERT INTO instruments Values("' + '","'.join([str(get_a_id()),str(e.id),i[0],i[1],i[2]])+ '")')
        
    
    for e  in CompositorManager:
        if e == None : continue
        c.execute( 'INSERT INTO compositors VALUES ("' + '","'.join([str(e.id),e.name,str(e.birth),str(e.death),e.url])+'")')

    for e  in ActivitiesManager:
        if e == None : continue
        c.execute( 'INSERT INTO activities VALUES ("' + '","'.join([str(e.id),str(e.oeuvre.id),str(e.annee),str(e.nom_musicien),e.classement])+'")')

    conn.commit()

    conn.close()
    print(issue)
    print(str(datetime.datetime.today()))

    
    
    