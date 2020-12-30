#à partir du tuto suivant : https://blog.lesjeudis.com/web-scraping-avec-python

#libraries
from bs4 import BeautifulSoup
import urllib.request
import csv

#https://www.toutmontreal.com/eetp/eetp.html
urlpage = "https://www.toutmontreal.com/ieti/internet/consultantsinter.html"


#renvoie l'html de la page dans "page"
page = urllib.request.urlopen(urlpage)
#utilise beautiful soup pour parser l'html recueilli 
soup = BeautifulSoup(page, 'html.parser')

#recherche dans la liste
colonne = soup.find('ol')
resultats = colonne.find_all('li')

#creation table 
rows = [] 
rows.append(["Nom", "Adresse", "Site", "URL Fiche"])

#tri des résultats non-nuls 
i = 0
for resultat in resultats:
    nom = resultat.find("a").getText()
    try:
        adresse = resultat.find("div", attrs={"class":"petit"}).getText().replace("Adresse: ", "")
    except:
        adresse = "inconnue"
    site = resultat.find("a").get("href")
    url_fiche = resultat.find("span", attrs={"class":"petit"}).find("a").get("href")
    rows.append([nom,adresse,site, url_fiche])

# Create csv and write rows to output file
with open('ListeEntrepriseMontreal.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)
