from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests 
import shutil 
import os

save_path = "C:/Users/Ohlone/Desktop/images crypto/" # là ou tu vas save tes images

if not os.path.exists(save_path):
    os.makedirs(save_path) # on crée le dossier si il est pas déjà créé

options = Options()
options.add_argument("-private")
# options.add_argument("-headless")
driver = webdriver.Firefox(options=options) # initialisation du webdriver

pages_compteur = 1

while pages_compteur < 90: # 89 pages à traiter

    driver.get("https://coinmarketcap.com/fr/?page="+str(pages_compteur)) # load la page souhaitée
    driver.maximize_window()

    liste_coins = WebDriverWait(driver, 10).until( # on attends 10 secondes que ça charge
        EC.presence_of_all_elements_located((By.TAG_NAME, "tbody")) # récupération de la balise principale tbody
    )

    compteur = 0

    #refresh page pour avoir les 100 cryptos chargées
    while compteur < 99:
        for index_tb, current_coin in enumerate(liste_coins):
            try:
                bon_tr = WebDriverWait(current_coin, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "tr")) # récup élément tr = une ligne de crypto
                )
                for current_tr in bon_tr: # loop dans les tr soit les lignes
                    current_monnaie = current_tr.find_elements(By.TAG_NAME,"td") # récupération des éléments composant la ligne (dans l'ordre : image, nom, nom réduit)
                    if len(current_monnaie) > 2:
                        infos = current_monnaie[2] # récupération nom réduit : BTC
                        driver.execute_script("arguments[0].scrollIntoView();", infos) # on scroll à chaque fois à la ligne pour faire charger
                        compteur = compteur + 1
                        print(compteur)
            except:
                liste_coins = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "tbody")) # quand il arrive plus à charger, on re récupère le tbody et on repart pour un tour
                )
                current_coin = liste_coins[index_tb]
                compteur = 0

    # une fois que les 100 lignes ont étés chargées on refait pareil en gros
    #récup infos 100 cryptos
    for index_tb, current_coin in enumerate(liste_coins):
        try:
            bon_tr = WebDriverWait(current_coin, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
            )
            for current_tr in bon_tr:
                current_monnaie = current_tr.find_elements(By.TAG_NAME,"td")
                if len(current_monnaie) > 2:
                    infos = current_monnaie[2]
                    driver.execute_script("arguments[0].scrollIntoView();", infos)

                    infos = current_tr.find_elements(By.TAG_NAME,"td")[2]

                    nom_crypto_liste = WebDriverWait(infos, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
                    )
                    nom_crypto = nom_crypto_liste[1].text if len(nom_crypto_liste) > 1 else infos.text # on récup le nom de la crypto, mais des fois ça trouve pas donc on prends le nom complet

                    img = infos.find_element(By.CLASS_NAME, "coin-logo") # récup balise image
                    src = img.get_attribute('src') # récup URL image
                    print(nom_crypto, src)

                    response = requests.get(src, stream=True) # téléchargement de l'image
                    with open(f'{save_path}{nom_crypto}.png', 'wb') as file: # on save l'image à la path donnée au début + nom de la crypto.png
                        shutil.copyfileobj(response.raw, file) 
                    del response
        except:
            liste_coins = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "tbody"))
            )
            current_coin = liste_coins[index_tb]
    pages_compteur = pages_compteur + 1 # ça permet d'incrémenter l'URL au début donc de passer à la prochaine page 
    print("prochaine page : " + str(pages_compteur))


print("fin du scrapping")
print("killian a une petite bite")
driver.quit()