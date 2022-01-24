import tkinter as tk
from tkinter import ttk
import pyperclip as pc
import os
import time
import threading
from functools import partial
import webbrowser
from tkinter import filedialog
from tkinter import Listbox
from tkinter import messagebox
from tkinter import *
import concurrent.futures

from adlt_sele_ddler import urls_ddl
from models import fetchall_toddl_from_db, add_to_downloading_db, fetchall_ddled_from_db, remove_from_donwloading, fetch_folder_lst, add_folder_lst

#TODO Ajouter page pour profil (username, password)
#TODO Transformer le tout en fichier exe
#TODO Ajouter progressbar

root = tk.Tk()
root.title('Adult Video Downloader v0.1')

menubar = Menu(root)

def dosomething():
    pass

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Report", command=dosomething)
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

profilemenu = Menu(menubar, tearoff=0)
profilemenu.add_command(label="Add profile", command=dosomething)
profilemenu.add_command(label="View profile", command=quit)
menubar.add_cascade(label="Profile", menu=profilemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Check for update", command=dosomething)
helpmenu.add_command(label="Contact us", command=dosomething)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

#top_text = tk.Label(text='Liens à télécharger')
top_text = tk.Label(text='Links to download')
text_frame = tk.Frame()
scroll_bar = tk.Scrollbar(text_frame, jump=1)
text_field = tk.Text(text_frame, yscrollcommand = scroll_bar.set)
mylist = Listbox(root, yscrollcommand = scroll_bar.set ) 

top_text.grid(row=1)
text_frame.grid()
scroll_bar.grid(column=2, row=1, sticky='NSW')
text_field.grid(column=1, row=1, padx=(10,0), pady=5)

scroll_bar.config(command = text_field.yview )

#Commencer a faire le monitoring du clipboard
def updateClipboard():
    try:
        url = root.clipboard_get()
        text_field.insert(tk.END, url + '\n') 
        #print('Tried to print something...')
        root.clipboard_clear()
    except tk.TclError:
        pass
    print('Waited 2 sec')
    #Arreter le processus de monitoring du clipboard
    def stopClipboard(event):
        if True:
            text_field.after_cancel(id_after)
            print('Clipboard update stopped')
    #Lier le clic du bouton "stop" a l'arret du monitoring
    copy_s.bind("<Button-1>", stopClipboard)
    print('Avant ID after')
    id_after = text_field.after(ms=1000, func=updateClipboard)
    return id_after

#Quitter l'appli
def quitApp():
    root.destroy()
    return True

#Obtenir la liste des liens copies dans la fenetre de l'appli
def ddlLinks():
    global select
    global x
    rad_val = x.get()
    print(rad_val)
    urls = text_field.get('1.0', tk.END)
    cleaned_urls = urls.split('\n')
    new_urls = [url for url in cleaned_urls if url != '']
    if new_urls:
        # ok_msg(ok_msg='Links are downloading...')
        select = pass_dir()
        print(select)
        if select:
            success_dl = []
            fail_dl = []
            #Rendre le nombre de max workers ou dl simultane dynamique
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_to_url = {executor.submit(urls_ddl, url, select, rad_val): url for url in new_urls}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as e:
                        print(f'{url} generated an exception: {e}')
                        fail_dl.append(url)
                    else:
                        print(f'Return statement from selenium funct#######{data}')
                        success_dl.append(url)

            num_success = len(success_dl)
            num_fail = len(fail_dl)
            # for url in new_urls:
                # while url !='':
                # if threading.active_count() <= 2:     
                #     print(threading.active_count())
                #     print(threading.enumerate())
                #     threading.Thread(target= urls_ddl, args=(url, select)).start()

                # while threading.active_count() >= 3:
                #     print('Waiting')
                #     wait_thread = threading.current_thread()
                #     print(type(wait_thread))
                #     wait_thread.join()
                #     print('############################')
                    # else:
                    #     wait_thread = threading.current_thread()
                    #     wait_thread.join()

        # else:
        #     for url in new_urls:
        #         if threading.active_count() <= 2:
        #             threading.Thread(target= urls_ddl, args=(url,)).start()
        #         else:
        #             wait_thread = threading.current_thread()
        #             wait_thread.join()
                    
        # if threading.active_count() >= 1: 
        #     ok_msg(ok_msg='Links are downloading...')

        #ddl_result_lst(lst_ddled_urls)

        #Transformer le msg en pop-up + ajouter stats a database
        completion_msg = f"{num_success} successful downloads, {num_fail} failed downloads. {round(float((num_success/len(new_urls))*100), 2)}% completion rate {'/n'.join(fail_dl) if len(fail_dl) >= 1 else ''}"
        
        messagebox.showinfo("Download summary", completion_msg)
        ok_msg(completion_msg)
        
        return True 
    
    else:
        msg = 'No links to download'
        error_msg(msg)
        return True

#Sauvegarder les liens vers la base donnees
def saveLinksDb():
    urls = text_field.get('1.0', tk.END)
    cleaned_urls = urls.split('\n')
    #TODO Ajouter une condition a la comprehension de liste pour n'ajouter que les lien se terminat par .com ou .net
    com = '.com'
    add_urls = [url for url in cleaned_urls if url != '' and com in url]
    if add_urls:
        add_to_downloading_db(add_urls)
        ok_msg(ok_msg='Links added to the database')
        return True
    else:
        msg = 'No links to add to the database'
        error_msg(msg)
        return True

#Obtenir les liens a telecharger dans la BD et les affiches dans la zone texte
def getLinksToDdlFromDb():
    deleteText()

    links = fetchall_toddl_from_db()
    if links:
        for link in links:
            text_field.insert(tk.END, link[0] + '\n') 
            remove_from_donwloading(link)
        return True
    else:
        msg = 'No links to download in the databse'
        error_msg(msg)
        return True

#Obtenir les liens a telecharger dans la BD et les affiches dans la zone texte
def getLinksDdledFromDb():
    deleteText()

    links = fetchall_ddled_from_db()
    if links:
        for link in links:
            text_field.insert(tk.END, link[0] + '\n') 
        return links
    else:
        msg = 'No downloaded links in the database'
        error_msg(msg)
        return True

#Supprimer le texte de la zone texte
def deleteText():

    text_field.delete('1.0', tk.END)
    return True
    
#Message d'erreur
def error_msg(error_msg='There was a problem'):

    deleteText()
    text_field.insert(tk.END, error_msg)
    return True

#Message de succes
def ok_msg(ok_msg = 'Everything worked ok'):
    
    deleteText()
    text_field.insert(tk.END, ok_msg)
    return True

#Afficher les telechargements a succes a la fin
def ddl_result_lst(result):

    deleteText()
    for lsts in result:
        if lsts:
            for url in lsts:
                text_field.insert(tk.END, url + '... Completed successfully' +'\n')

        else:
            if not lsts[0]:
                text_field.insert(tk.END, url + '... Download unsuccessful' +'\n')
            elif not lsts[1]:
                text_field.insert(tk.END, url + '... All downloads successful' +'\n')
    return True

dir_list = []

#Fonction pour choisir un dossier de telechargement
def choose_dir():
    dir_input = filedialog.askdirectory(title='Choose download directory')
    dir_list.append(dir_input)
    # select = folders_menu.set(dir_input)
    if dir_input != '':
        folders_menu.set(dir_input)
    select = folders_menu.get()
    print(type(select))
    print(select)
    add_folder_lst(select)
    return select

#Fonction pour selectionner une option dans le menu
def select_dir(event):
    select = folders_menu.get()
    folders_menu.current()
    return select

def pass_dir():
    dir_name = folders_menu.get()
    new_dir = dir_name.replace('/', '\\')
    return new_dir

#Fonction pour definir la taille du menu et les elements a afficher
def check_for_dir():
    dir_lst_from_db = fetch_folder_lst()
    print(dir_lst_from_db)
    print('#########################################')
    
    if dir_lst_from_db:
        menu_lst = [i for i in list(set(dir_lst_from_db[-6:]))]
        print(len(menu_lst))
        # some_list = [folders_menu.set(i) for i in menu_lst]
        folders_menu.configure(values=menu_lst)
        # # print(some_list)
        # folders_menu.current()

    # if len(dir_list) > 5:
    #     new_menu = folders_menu.configure(values=dir_list[-5:])
    #     folders_menu.current()
    #     return new_menu
    # else:
    #     new_menu = folders_menu.configure(values=dir_list)
    #     folders_menu.current()
    #     return new_menu
    else:
        pass

# Section Boutons et Options Debut ################################        
folder_frame = tk.Frame()
labelframe = LabelFrame(folder_frame, text="View the download window")
folders_menu = ttk.Combobox(folder_frame,postcommand=check_for_dir)
folders_menu.bind('<<ComboboxSelected>>', select_dir) 
dir_button = tk.Button(folder_frame, text='Choose download directory', command=choose_dir)
copy_b = tk.Button(folder_frame, text='Start copying links', command=updateClipboard)
copy_s = tk.Button(folder_frame, text='Stop copying links')
start_b = tk.Button(folder_frame, text='Download links', command=ddlLinks)
save_to_db = tk.Button(folder_frame, text='Save links to DB', command=saveLinksDb)
get_from_db = tk.Button(folder_frame, text='Get links to DDL from DB', command=getLinksToDdlFromDb)
get_from_db_to = tk.Button(folder_frame, text='Get DDLed links from DB', command=getLinksDdledFromDb)
clear_b = tk.Button(folder_frame, text='Clear text', command=deleteText)
quit_b = tk.Button(folder_frame, text='Quit', command=quitApp)

x = BooleanVar()
# y = IntVar(root)

def radio_choice():
    rad_val = x.get()
    print(rad_val)

    return rad_val

R1 = Radiobutton(labelframe, text="Yes", value=False, variable=x, command=radio_choice)
R2 = Radiobutton(labelframe, text="No", value=True, variable=x, command=radio_choice)

# def radio_choice(event):

    # print(event)
    # rad_val = x.get()
    # # new_val = x.set(rad_val)
    # print(rad_val)
    # # print('radio_choice step 2')
    # # print(new_val)
    # if rad_val == 1:
    #     print('Yes selected, false')
    # elif rad_val == 2:
    #     print('No selected, true')

# R1.bind("<Button>", radio_choice)
# R2.bind("<Button>", radio_choice)

sites_text = tk.Label(folder_frame, text='Available sites to download from')
urls_lst = ['https://www.eporner.com/', 'https://freehdinterracialporn.in', 'https://hqporner.com/', 'https://fr.spankbang.com/', 'https://sxyprn.com/', 'https://www.xvideos.com/', 'https://www.xnxx.com/', 'https://www.xozilla.com/']

Lb1 = Listbox(folder_frame, font=('Helvetica', '13', 'underline'))

# Lb1_font = font.Font('Times', '16', underline=1)
Lb1.insert(END, *urls_lst)

def internet(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print(data)
        webbrowser.open(data)

        # label.configure(text=data)
    else:
        # label.configure(text="")
        pass

Lb1.bind("<<ListboxSelect>>", internet)

scroll_bar_lst = tk.Scrollbar(folder_frame)
scroll_bar_lst.grid(column=2, row=4, rowspan=7, sticky='NEWS')
scroll_bar_lst.config(command = Lb1.yview)
Lb1.config(yscrollcommand = scroll_bar_lst.set)

folder_frame.grid()
folders_menu.grid(column=1, row=1, padx=5, pady=5, sticky='EW')
dir_button.grid(column=4, row=1, padx=5, pady=5, sticky='NEWS')
labelframe.grid(column=1, row=2, padx=3, pady=1, sticky='NEWS')
R1.grid(column=1, row=3,padx=(95, 100), sticky='NEWS')
R2.grid(column=2, row=3,padx=(100, 95), sticky='NEWS')
sites_text.grid(column=1, row=3, padx=2, pady=(5, 1))
Lb1.grid(column=1, row=4, rowspan=8, padx=(5,0), pady=(1, 15), sticky='NEWS')

copy_b.grid(column=4, row=2,padx=5, pady=5, sticky='EW')
copy_s.grid(column=4, row=3,padx=5, pady=5, sticky='EW')
start_b.grid(column=4, row=4,padx=5, pady=5, sticky='EW')
save_to_db.grid(column=4, row=5,padx=5, pady=5, sticky='EW')
get_from_db.grid(column=4, row=6,padx=5, pady=5, sticky='EW')
get_from_db_to.grid(column=4, row=7,padx=5, pady=5, sticky='EW')
clear_b.grid(column=4, row=8,padx=5, pady=5, sticky='EW')
quit_b.grid(column=4, row=9,padx=5, pady=5, sticky='EW')
# Section Boutons et Options Fin ################################

root.resizable(True, True) 
root.mainloop()
