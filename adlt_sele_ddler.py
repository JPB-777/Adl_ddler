import os
import os.path
import time
import requests
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options

from models import add_to_downloaded_db
#from tkinter_clippy_ddler import error_msg

#Probleme quand erreur de telechargement --corriger en parti
#Ajouter if quand un lien de la liste est inexistant --ok
#Ajouter une facon de verifier si lien est toujours actif
#TODO Ajouter log file

spkbg = 'spankbang.com'
eprnr = 'eporner.com'
hqprnr = 'hqporner.com'
xvd = 'xvideos.com'
xnxx = 'xnxx.com'
prnhd = 'pornhd.com'
xzll = 'xozilla.com'
sxprn = 'sxyprn.com'
frntrrclprn = 'freehdinterracialporn.in'

def eprnr_ddl(driver, wait):
    if driver.find_elements(By.XPATH, "//span[contains(@data-menutype, 'downloaddiv')]"):
        menu_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@data-menutype, 'downloaddiv')]")))
        menu_button.click()

    if driver.find_elements(By.XPATH, "//div[@id='hd-porn-dload']//div[@class='dloaddivcol']//a[contains(text(), '480')]"):
        eprnr_480p = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='hd-porn-dload']//div[@class='dloaddivcol']//a[contains(text(), '480')]")))
        eprnr_480p.click()
        file_format = '480'
        
        
    elif driver.find_elements(By.XPATH, "//div[@id='hd-porn-dload']//div[@class='dloaddivcol']//a[contains(text(), '320')]"):
        eprnr_320p = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='hd-porn-dload']//div[@class='dloaddivcol']//a[contains(text(), '320')]")))
        eprnr_320p.click()
        file_format = '320'
        
        
    elif driver.find_elements(By.XPATH, "//div[@id='hd-porn-dload']//div[@class='dloaddivcol']//a[contains(text(), '240')]"):
        eprnr_240p = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='hd-porn-dload']//div[@class='dloaddivcol']//a[contains(text(), '240')]")))
        eprnr_240p.click()
        file_format = '240'
        
    
    else:
        print('Cannot find desired file format')
        
    return file_format

def spkbng_ddl(driver, wait):
    try:                                                                            
        if driver.find_element(By.XPATH, "//header//ul[@class='top']//li[@class='links']//a[contains(text(),'Connexion')]"):
            login_btn_header = wait.until(EC.element_to_be_clickable((By.XPATH, "//header//ul[@class='top']//li[@class='links']//a[2]")))
            login_btn_header.click()
            the_user = driver.find_element(By.XPATH, "//li//input[@id='log_username']")
            the_user.send_keys('bassman3579')
            the_pass = driver.find_element(By.XPATH, "//li//input[@id='log_password']")
            the_pass.send_keys('Leslie29')
            submit_btn = driver.find_element(By.XPATH, "//p//button[@class='ft-button ft-red sign']")
            submit_btn.click()
            driver.implicitly_wait(2)
            driver.switch_to.default_content()
        else:
            driver.switch_to.default_content()

        if driver.find_element(By.XPATH, "//ul[@class='video_toolbar']//li[7]"):
            wait_25 = WebDriverWait(driver, 25, poll_frequency=1,ignored_exceptions=[NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException])
            dl_link = wait_25.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='video_toolbar']//li[7]")))
            try:
                dl_attempt = 0 
                while dl_attempt < 3:
                    link_click = dl_link.click()
                    driver.execute_script('arguments[0].click()', link_click)
                    time.sleep(1)
                    dl_attempt += 1
                    # print(dl_attempt)
            except StaleElementReferenceException as e:
                time.sleep(4)
                new_dl_link = wait_25.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='video_toolbar']//li[7]")))
                new_dl_link.click()
                print(e)# A transformer ? en log ?

        else:
            # print("False")
            dl_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='video_toolbar']//li[7]")))
            dl_link.click()


        #Cliquer le lien de download
        try:
            # print('Section liens')

            if driver.find_elements(By.XPATH, "//section[@class='download-list']//p[@class='pl b_480p'and contains(@style, 'display')]"):
                dl_480p = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//section[@class='download-list']//p[@class='pl b_480p'and contains(@style, 'display')]")))
                dl_480p.click()
                file_format = '480p'
                print(file_format)                  

            elif driver.find_elements(By.XPATH, "//section[@class='download-list']//p[@class='pl b_320p'and contains(@style, 'display')]"):
                dl_320p = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//section[@class='download-list']//p[@class='pl b_320p'and contains(@style, 'display')]")))
                dl_320p.click()
                file_format = '320p'
                print(file_format)                        

            elif driver.find_elements(By.XPATH, "//section[@class='download-list']//p[@class='pl b_240p'and contains(@style, 'display')]"):
                dl_240p = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//section[@class='download-list']//p[@class='pl b_240p'and contains(@style, 'display')]")))
                dl_240p.click()
                file_format = '240p'
                print(file_format)

            else:
                print('Error finding dl link') 

        except Exception as e:
            print(e)                  

    except Exception as e:
        print(e)
    
    return file_format

def hqprnr_ddl(driver, wait, ddl_path, url):
    time.sleep(2)
    # body = driver.find_element(By.XPATH, "//body")
    # driver.execute_script("arguments[0].setAttribute('class', 'vsc-initialized')")
    # driver.execute_script("arguments[0].setAttribute('class', 'vsc-initialized')", body)
    # print('Etape 0')
    # handles = driver.window_handles
    # print(handles)
    # elem = driver.execute_script("document.getElementsByTagName('iframe')")
    # print(elem)
    elem3 = driver.find_element(By.XPATH,"//div[@class='videoWrapper']//iframe")
    print(elem3)
    ele3_attr = elem3.get_attribute('src')
    print(ele3_attr)
    driver.get(ele3_attr)
    driver.implicitly_wait(2)
    print('Etape 1')
    import requests
    import re
    import os
    # time.sleep(2)
    # os.chdir(ddl_path)
    # name_file = driver.title
    # print(name_file)
    print('Etape 2')
    # video_360 = wait.until(EC.presence_of_element_located((By.XPATH, "//video[@id='flvv']//source[contains(@title, '360')]")))
    video_360 = driver.find_element(By.XPATH, "//video[@id='flvv']//source[contains(@title, '360')]")
    # video_720 = wait.until(EC.presence_of_element_located((By.XPATH, "//video[@id='flvv']//source[contains(@title, '720')]")))
    video_720 = driver.find_element(By.XPATH, "//video[@id='flvv']//source[contains(@title, '720')]")
    print('Etape 3')
    if video_360:
        os.chdir(ddl_path)
        url_split = url.split('/')
        part_strip = re.search("[0-9]+-", url_split[-1])
        # print(type(part_strip.group()))
        title = url_split[-1].strip('.html').strip(part_strip.group())
        name_file = f"Hqporner - {title}.mp4"
        # dl_elem = driver.find_element(By.XPATH, "//video[@id='flvv']//source[contains(@title, '360')]")
        dl_link = video_360.get_attribute('src')
        print('Element video 360 found')
        r = requests.get(dl_link, stream=True)
        with open(name_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    elif video_720:
        dl_link = driver.find_element(By.XPATH, "//video[@id='flvv']//source[contains(@title, '720')]/@src")
        print('Element video 720 found')
        r = requests.get(dl_link, stream=True)
        with open(name_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print('Problem dling from HQprnr')
        pass

    driver.quit()
    # dled_urls.append(url)
    add_to_downloaded_db(url)

    return True

def xvd_ddl(driver, wait):

    if driver.find_element(By.XPATH, "//div[@class='video-page']//a[contains(@data-mode, 'signin')]"):
        login_btn = driver.find_element(By.XPATH, "//div[@class='video-page']//a[contains(@data-mode, 'signin')]")
        login_btn.click()

        the_user = driver.find_element(By.XPATH, "//input[@class='form-control'][@type='email']")
        the_user.send_keys('joel33@zoho.com')
        the_pass = driver.find_element(By.XPATH, "//input[@class='form-control'][@type='password']")
        the_pass.send_keys('WisedLv5arQx') #Recuperer a partir de  sauvegarde bd fait d'une autre page
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'][contains(text(), 'Log in') or contains(text(), 'Connexion')]")
        submit_btn.click()

        driver.implicitly_wait(2)
        driver.switch_to.default_content()
    else:
        pass

    if driver.find_element(By.XPATH, "//ul[@class='tab-buttons']//li[2]/a"):
        wait_25 = WebDriverWait(driver, 25, poll_frequency=1,ignored_exceptions=[NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException])
        dl_tab = wait_25.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='tab-buttons']//li[2]/a")))
        try:
            dl_attempt = 0 
            while dl_attempt < 3:
        #             link_click = dl_link.click()
                dl_tab.click()
        #             driver.execute_script('arguments[0].click()', link_click)
                time.sleep(1)
                dl_attempt += 1
                # print(dl_attempt)
        except StaleElementReferenceException as e:
            time.sleep(4)
            new_dl_tab = wait_25.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='tab-buttons']//li[2]/a")))
            new_dl_tab.click()
            print(e)# A transformer ? en log ? 
        

    if driver.find_element(By.XPATH, "//p//strong[contains(text(), 'MEDIUM')]"):
        dl_link = wait_25.until(EC.element_to_be_clickable((By.XPATH, "//p//strong[contains(text(), 'MEDIUM')]")))
        dl_link.click()
        file_format = 'medium'

    return file_format

def xnxx_ddl(driver, wait):
    dl_btn_wait = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tab-buttons']/a[@title='Télécharger']")))
    if dl_btn_wait:
        ddl_btn = driver.find_element(By.XPATH, "//div[@class='tab-buttons']/a[@title='Télécharger']")
        ddl_btn.click()

        if driver.find_element(By.XPATH, "//div[@id='tabDownload']//a[@class='text-danger']"):
            connex_link = driver.find_element(By.XPATH, "//div[@id='tabDownload']//a[@class='text-danger']")
            connex_link.click()

            username = driver.find_element(By.XPATH, "//form[@id='signin-form']//input[@type='email']")
            username.send_keys('bassman3579@gmail.com')

            password = driver.find_element(By.XPATH, "//form[@id='signin-form']//input[@type='password']")
            password.send_keys('Leslie29')

            lgn_btn = driver.find_element(By.XPATH, "//form[@id='signin-form']//button[@type='submit']")
            lgn_btn.click()

            driver.implicitly_wait(2)
            driver.switch_to.default_content()

            ddl_btn1 = driver.find_element(By.XPATH, "//div[@class='tab-buttons']/a[@title='Download']")
            ddl_btn1.click()

            file_format = driver.find_element(By.XPATH, "//div[@id='tabDownload']//a//strong")
            fileformat = file_format.text
            #print(file_format.text)

            med_btn = driver.find_element(By.XPATH, "//div[@id='tabDownload']//a")
            med_btn.click()

    return fileformat

def prnhd_ddl(driver, wait):
    dl_btn_wait = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='video-player-controls']//button[@aria-controls='videoDownload']")))
    if dl_btn_wait:
        # dl_btn = driver.find_element(By.XPATH, "//div[@class='video-player-controls']//button[@aria-controls='videoDownload']")
        # dl_btn.click()

        menu_btn = driver.find_element(By.XPATH, "//div[@class='dropdown-trigger']/a")
        menu_btn.click()
        # lgn_btn_wait = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-menu']//a[@data-target='modal-login']")))
        lgn_btn_wait = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dropdown-menu']//a[@data-target='modal-login']")))
        # lgn_btn_wait = driver.find_element(By.XPATH, "//div[@class='dropdown-menu']//a[@data-target='modal-login']")
        lgn_btn_wait.click()

        username = driver.find_element(By.XPATH, "//div[@class='field']//input[@name='email']")
        username.send_keys("bassman3579@gmail.com")

        password = driver.find_element(By.XPATH, "//div[@class='field']//input[@name='password']")
        password.send_keys("Leslie29")

        lgn_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//div[@class='buttons']//button[@type='submit']")))
        lgn_btn.click()

        dl_btn_480p_wait = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal is-active']//a[@class='download-video']")))
        if dl_btn_480p_wait:
            dl_btn_480p = driver.find_element(By.XPATH, "//div[@class='modal is-active']//a[@class='download-video']")
            dl_btn_480p.click()

    return True

def xzll_ddl(driver, wait):
    dl_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='info']//div[contains(text(), 'Download')]/a[1]")))
    # dl_btn = driver.find_element(By.XPATH, "//div[@class='info']//div[@class='item'][5]/a[1]")
    print(dl_btn)

    if dl_btn:
        dl_btn.click()

    fileformat = 'smallest'

    return fileformat

def sxprn_ddl(driver, wait, ddl_path):
    # import requests
    print('Sxyprn function start')
    print(ddl_path)
    os.chdir(ddl_path)

    link_src = driver.find_element(By.XPATH, "//video[@id='player_el']")
    dl_link = link_src.get_attribute('src')

    print(dl_link)

    title = driver.title
    forbidden_symbols = '*."/[]:;|,!?\\'
    y = ' ' * len(forbidden_symbols)
    translation = title.maketrans(forbidden_symbols, y)
    trans = title.translate(translation)
    name_file = f'Sxyprn - {trans[:60]}.mp4'
    print(name_file)

    r = requests.get(dl_link, stream=True)
    with open(name_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    driver.quit()
    return True

def frntrrclprn_ddl(driver, wait):
    bt_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-id='download']")))
    # bt_link = driver.find_element(By.XPATH, "//button[@data-id='download']")
    
    x = 1

    if driver.find_element(By.XPATH, "//div[@class='exo_wrapper']"):
        text_tag = driver.find_element(By.XPATH, "//div[@class='exo_close_text']")
        print(text_tag)

        while driver.find_element(By.XPATH, "//div[@class='exo_close_text']").text != 'Close ad' and x < 351:
            driver.implicitly_wait(2)
            print(x)
            print(driver.find_element(By.XPATH, "//div[@class='exo_close_text']").text)
            x += 1  

        if driver.find_element(By.XPATH, "//div[@class='exo_close']"):
            close_link = driver.find_element(By.XPATH, "//div[@class='exo_close']")
            close_link.click()

    if bt_link:
        bt_link.click()

    if driver.find_element(By.XPATH, "//a[contains(text(), '720')]"):
        dl_link_720 = driver.find_element(By.XPATH, "//a[contains(text(), '720')]")
        dl_link_720.click()
        file_format = '720p'

    elif driver.find_element(By.XPATH, "//a[contains(text(), '360')]"):
        dl_link_360 = driver.find_element(By.XPATH, "//a[contains(text(), '360')]")
        dl_link_360.click()
        file_format = '360p'
    else:
        driver.quit()

    return file_format

def file_name(url, host_url, file_format, driver):
    #Attendre et verifier que le fichier est telecharger
    if spkbg in url:

        url_parts = url.split('/')
        new_url_parts = [url_part for url_part in url_parts if url_part != '']
        print(new_url_parts)
        title = new_url_parts[-1]
        print(title)
        if '480' in file_format:
            name_file = f"{host_url}_{title}_{file_format}.mp4"
        elif '320' in file_format:
            name_file = f"{host_url}_{title}_{file_format}.mp4"
        elif '240' in file_format:
            name_file = f"{host_url}_{title}_{file_format}.mp4"
        else:
            print('Cannot find the file to download')

        return name_file
    
    elif eprnr in url:

        title_drvr = driver.title
        print(title_drvr)
        # title_driver = 'Balls Deep Anal - Alexa Flexy - Calibri - EPORNER'
        try:
            new_title = title_drvr.split('-')
            print(new_title)
            if len(new_title) >= 4:
                comp_title = '-'.join(new_title[:2])
            else:
                comp_title = new_title[0].strip()
                print(comp_title + "filename func")
        except:
            # pass
            comp_title = title_drvr

        # name_file = f"{title}.mp4"
        # if name_file:
        #     if f"{title}.mp4.crdownload" != True:

        url_parts = url.split('/')
        new_url_parts = [url_part for url_part in url_parts if url_part != '']
        print(new_url_parts)

        partial_title = new_url_parts[-1]
        title = partial_title.split('-')
        print(title)

        new_title = ' '.join(title)

        partial_code_url = new_url_parts[-2]
        if 'video-' in partial_code_url:
            lowdef_code_url = partial_code_url.replace('video-', '')
        # lowdef_code_url = f"video-{partial_code_url}"
            print(lowdef_code_url)

            name_file = f"EPORNER.COM - [{lowdef_code_url}] {comp_title} ({file_format}).mp4"
            print(name_file)
        else:
            name_file = f"EPORNER.COM - [{partial_code_url}] {comp_title} ({file_format}).mp4"
            print(name_file)

        return name_file

    elif xvd in url or xnxx in url:
        title = driver.title
        print(title)

        file_num = driver.find_element(By.XPATH, "//meta[@property = 'og:image']").get_attribute('content')
        new_file_num = file_num.split('/')
        print(new_file_num[-2])
        filename = new_file_num[-2]

        name_file = f"xvideos.com_{filename}.mp4"

        return name_file, title

    elif xzll in url:
        title = driver.title
        url_split = url.split('/')
        url_parts = [i for i in url_split if i !='']
        namefile = f"{url_parts[-1]}.mp4"

        return namefile, title

    elif frntrrclprn in url:
        new_url = url.split('/')
        full_url = [i for i in new_url if i != '']
        title = full_url[-1]
        namefile = f'{title}-{file_format}.mp4'
        print(namefile)

        return namefile

def check_file_path(url, ddl_path, namefile, dled_urls, driver):

        file_path = os.path.join(ddl_path, namefile)
        print(file_path)
        # file_path = f"{partial_path}.crdownload"
        seconds = 0
        while os.path.isfile(file_path) != True:
            time.sleep(5)
            seconds += 5
            if seconds > 450:
                print('Download failed')
                driver.quit()
                break
        else:
            
            driver.quit()
            dled_urls.append(url)
            add_to_downloaded_db(url)
        
        return file_path

def check_file_exist(url, ddl_path, namefile, dled_urls, driver):
    os.chdir(ddl_path)
    
    if spkbg in url:
        filepath = check_file_path(url, ddl_path, namefile, dled_urls, driver)

    elif eprnr in url:
        filepath = check_file_path(url, ddl_path, namefile, dled_urls, driver)

    elif xvd in url or xnxx in url:
        filepath = check_file_path(url, ddl_path, namefile, dled_urls, driver)
    
    elif xzll in url:
        filepath = check_file_path(url, ddl_path, namefile[0], dled_urls, driver)

    elif frntrrclprn in url:
        filepath = check_file_path(url, ddl_path, namefile, dled_urls, driver)
    # elif hqprnr in url:

    #     file_path = os.path.join(ddl_path, namefile)
    #     print(file_path)
    #     # file_path = f"{partial_path}.crdownload"
    #     seconds = 0
    #     while os.path.isfile(file_path) != True:
    #         time.sleep(5)
    #         seconds += 5
    #         if seconds > 450:
    #             print('Download failed')
    #             break
    #     else:
    #         driver.quit()
    #         dled_urls.append(url)
    #         add_to_downloaded_db(url)

    return filepath

def change_filename(url, host_url, ddl_path, namefile, file_path, title):
    os.chdir(ddl_path)
    print('Change name function  - Step1')
    forbidden_symbols = r'*."/[]:;|,!?\\'
    forbidden_symbols_replace = ' ' * len(forbidden_symbols)
    if xvd in url or xnxx in url:
        print(f"File path: {file_path} - Step2")
        if file_path != '':
            print(f"Name file: {namefile} - Step3")
            clean_namefile = namefile.strip('xvideos.com_').strip('.mp4')
            print(f"Clean Name file: {clean_namefile} - Step4")
            print(os.listdir())
            for i in os.listdir():
                print(f"List of files: - Step5")
                if clean_namefile in i:
                    # print(file_path)
                    print(i)
                    # old_title = driver.title
                    # print(old_title)
                    new_title = title.split('- X')
                    print(new_title)
                    clean_title = new_title[0].strip()
                    trans = clean_title.maketrans(forbidden_symbols, forbidden_symbols_replace)
                    cleaned_title = clean_title.translate(trans)
                    filename = f"xVideos - {cleaned_title}.mp4"
                    print(f'New filename: {filename} - (change filename function)')
                    os.rename(file_path, os.path.join(ddl_path, filename))

    elif xzll in url:
        title_split = title.split('/')
        new_title = title_split[0]

        filename = f"Xozilla - {new_title}.mp4"
        if file_path != '':
            for i in os.listdir():
                if namefile in i:
                    os.rename(file_path, os.path.join(ddl_path, filename))

    return True

def urls_ddl(url, ddl_path='M:\\Videotheque\\Nopro', headless=False):
    
    dled_urls = []
    bad_urls = []
            
    #chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_headless(headless=headless)
    chrome_options.add_argument("--window-size=1200,960")
    #chrome_options.add_argument(f"download.default_directory={ddl_path}")
    prefs = {"download.default_directory": ddl_path,
            #  "download.prompt_for_download": True
                }
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)
    #Definir le parametre wait
    wait = WebDriverWait(driver, 10, poll_frequency=1,ignored_exceptions=[NoSuchElementException,ElementNotVisibleException,
                                                                            ElementNotSelectableException])
    if spkbg in url:
        
        fileformat = spkbng_ddl(driver, wait)
        namefile = file_name(url, spkbg, fileformat, driver)
        check_file_exist(url, ddl_path, namefile, dled_urls, driver)

    elif eprnr in url:
        
        fileformat = eprnr_ddl(driver, wait)
        namefile = file_name(url, eprnr, fileformat, driver)
        check_file_exist(url, ddl_path, namefile, dled_urls, driver)
        # except Exception as e:
        #     bad_urls.append(url)
        #     print(e)

    elif hqprnr in url:
        hqprnr_ddl(driver, wait, ddl_path, url)

    elif xvd in url:
        fileformat = xvd_ddl(driver, wait)
        namefile = file_name(url, xvd, fileformat, driver)
        filepath = check_file_exist(url, ddl_path, namefile[0], dled_urls, driver)
        change_filename(url, xvd, ddl_path, namefile[0], filepath, namefile[1])

    elif xnxx in url:
        fileformat = xnxx_ddl(driver, wait)
        namefile = file_name(url, xnxx, fileformat, driver)
        filepath = check_file_exist(url, ddl_path, namefile[0], dled_urls, driver)
        change_filename(url, xvd, ddl_path, namefile[0], filepath, namefile[1])

    elif prnhd in url:
        prnhd_ddl(driver, wait)

    elif xzll in url:
        fileformat = xzll_ddl(driver, wait)
        namefile = file_name(url, xzll, fileformat, driver)
        filepath = check_file_exist(url, ddl_path, namefile, dled_urls, driver)
        change_filename(url, xvd, ddl_path, namefile[0], filepath, namefile[1])

    elif sxprn in url:
        sxprn_ddl(driver, wait, ddl_path)

    elif frntrrclprn in url:
        fileformat = frntrrclprn_ddl(driver, wait)
        namefile = file_name(url, frntrrclprn, fileformat, driver)
        filepath = check_file_exist(url, ddl_path, namefile, dled_urls, driver)

    else:
        pass
            
    return (url)
