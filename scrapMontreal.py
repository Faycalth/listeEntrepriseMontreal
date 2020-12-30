#à partir du tuto suivant : https://blog.lesjeudis.com/web-scraping-avec-python

#libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
import time

start_time = time.time()

#données tirées du site https://www.toutmontreal.com/eetp/eetp.html
page_name = ["Consultant internet", "Ingénieurs conseils"]
url_page = ["https://www.toutmontreal.com/ieti/internet/consultantsinter.html", "https://www.toutmontreal.com/eetp/ingenieurs.html"]

#plusieurs catégories à l'adresse suivante
page_cat = urllib.request.urlopen("https://www.toutmontreal.com/ieti/consultantsinfo/consultantsinfo.html")
soup_url = BeautifulSoup(page_cat, 'html.parser')
categorie = soup_url.find('ul')
resultats_categorie = categorie.find_all('li')

for resultat_cat in resultats_categorie:
    nom_cat = resultat_cat.find("a").getText()
    url_cat = resultat_cat.find("a").get("href")
    page_name.append(nom_cat)
    url_page.append(url_cat)

#creation table 
lignes = [] 
lignes.append(["Nom","Domaine","Adresse","Site","URL Fiche","Contact"])

#pour chaque url  
i = 0 
j = 0
k = 0
for url in url_page:
    #renvoie l'html de la page dans "page"
    page = urllib.request.urlopen(url)
    #utilise beautiful soup pour parser l'html recueilli 
    soup = BeautifulSoup(page, 'html.parser')

    #recherche dans la liste
    colonne = soup.find('ol')
    resultats = colonne.find_all('li')
    
    #tri des résultats non-nuls 
    for resultat in resultats:
        try:
            nom = resultat.find("a").getText()
        except:
            nom = ""
        try:
            adresse = resultat.find("div", attrs={"class":"petit"}).getText().replace("Adresse: ", "")
        except:
            adresse = "inconnue"
        try:
            site = resultat.find("a").get("href")
        except:
            site = ""
        try:
            url_fiche = resultat.find("span", attrs={"class":"petit"}).find("a").get("href")
        except:
            url_fiche = ""
        
        domaine = page_name[i]

        try:
            contact = ""
            page_contact = urllib.request.urlopen(url_fiche)
            soup_contact = BeautifulSoup(page_contact, "html.parser")
            colonne_contact = soup_contact.find("div")
            resultats_contact = colonne_contact.find_all("li")
            for r in resultats_contact:
                if str(r).find("@")>0:
                    contact = r.find("a").get("href").replace("mailto:", "")
                    k+=1
            resultats_contact.clear()
        except:
            contact = ""

        ligne = [nom,domaine,adresse,site,url_fiche,contact]


        #ajout des données dans lignes
        lignes.append(ligne)
        print(j, " entreprises traitées", end="\r")
        j+=1

    resultats.clear()
    i += 1


#création du csv
with open('listeEntrepriseMontreal.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(lignes)

print("Nombre d'entreprises traitées = " + str(j) )
print("Nombre de contacts trouvés = " + str(k) )
print("Temps d'execution = " + str(time.time() - start_time) + " secondes")
