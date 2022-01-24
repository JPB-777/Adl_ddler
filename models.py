#import sqlite3

def add_to_downloading_db(urls_to_db):
    import sqlite3
    import datetime
    from datetime import date 
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()

    #Creer table dans base de donnees si elle n<existe pas deja
    c.execute("CREATE TABLE IF NOT EXISTS todownload(link TEXT UNIQUE, date timestamp)")

    #Inserer plusieurs infos a la fois dans base de donnees
    try:
        lst_wdate = []
        #Obtenir une liste de tuple avec la date du jour
        for link in urls_to_db:
            a, b = link, date.today()
            new_tup = a, b
            lst_wdate.append(new_tup)

        c.executemany("INSERT INTO todownload (link, date) VALUES(?,?);",lst_wdate)
    except Exception as e:
        print(e)

    conn.commit()
    conn.close()
    return True

def add_to_downloaded_db(url):
    import sqlite3
    import datetime
    from datetime import date
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()

    #Creer table dans base de donnees si elle n<existe pas deja
    c.execute("CREATE TABLE IF NOT EXISTS downloaded(link TEXT UNIQUE, date timestamp)")

    try:
        #Inserer lien dans base de donnees
        c.execute("INSERT INTO downloaded (link, date) VALUES(?,?);", (url, date.today()))

    except Exception as e:
        print(e)

    conn.commit()
    conn.close()
    return True

def fetchall_toddl_from_db():
    import sqlite3
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()

    #Creer table dans base de donnees si elle n<existe pas deja
    c.execute("CREATE TABLE IF NOT EXISTS todownload(link TEXT UNIQUE, date timestamp)")
    
    #Collecter les liens de la base de donnees
    rows = c.execute("SELECT link FROM todownload").fetchall()
    
    conn.commit()
    conn.close()
    return rows

def fetchall_ddled_from_db():
    import sqlite3
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()
    
    #Creer table dans base de donnees si elle n<existe pas deja
    c.execute("CREATE TABLE IF NOT EXISTS downloaded(link TEXT UNIQUE, date timestamp)")

    #Collecter les liens de la base de donnees
    rows_ddled = c.execute("SELECT link,date FROM downloaded").fetchall()

    conn.commit()
    conn.close()
    return rows_ddled

def remove_from_donwloading(link):
    import sqlite3
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()

    #Creer table dans base de donnees si elle n<existe pas deja
    c.execute('DELETE FROM todownload WHERE link=?', (link[0],))

    conn.commit()
    conn.close()
    return True

def add_folder_lst(folder_name):

    import sqlite3
    # import datetime
    # from datetime import date
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()

    #Creer table dans base de donnees si elle n<existe pas deja
    c.execute("CREATE TABLE IF NOT EXISTS folders_lst(path TEXT)")

    try:
        #Inserer lien dans base de donnees
        c.execute("INSERT INTO folders_lst (path) VALUES(?);", (folder_name,))

    except Exception as e:
        print(e)

    conn.commit()
    conn.close()
    return True

def fetch_folder_lst():
    import sqlite3
    import os

    #Definir l'emplacement de la DB
    os.chdir('C:\\Users\\Ginette\\Documents\\Python Scripts\\Web_scrapers\\AFT\\Adult_ddler')

    #Creer(la 1ere fois) et se connecter a la base de donnees
    conn = sqlite3.connect('testagain.db')

    #Creer un curseur
    c = conn.cursor()

    #Creer table dans base de donnees si elle n<existe pas deja
    # c.execute("CREATE TABLE IF NOT EXISTS todownload(link TEXT UNIQUE, date timestamp)")
    
    #Collecter les liens de la base de donnees
    rows = c.execute("SELECT path FROM folders_lst").fetchall()
    # print(rows)
    # print(rows)
    paths_lst = [row[0] for row in rows]

    conn.commit()
    conn.close()
    return paths_lst

import os

# dir = os.getcwd()

# add_folder_lst(dir)

# fetch_folder_lst()