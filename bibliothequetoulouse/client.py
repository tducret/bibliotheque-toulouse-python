# -*- coding: utf-8 -*-
"""
Fonctionnalité permettant de faire les requêtes HTTP vers le serveur du catalogue des bibliothèques de Toulouse <http://catalogues.toulouse.fr>
"""

from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing.dummy import Pool as ThreadPool
import traceback # Analyse traces exception
from time import sleep
import itertools
from difflib import SequenceMatcher

_URL_BASE=u"http://catalogues.toulouse.fr/web2/tramp2.exe/"
_URL_PAGE_ACCUEIL=urljoin(_URL_BASE,u"log_in?setting_key=BMT1")
_URL_RECHERCHE=urljoin(_URL_BASE,u"do_keyword_search/log_in?setting_key=BMT1&servers=1home&screen=hitlist.html&query=")
_TIMEOUT=30
_TITRE_PAGE_UN_RESULTAT=u"Notice détaillée Web2"
_TITRE_PAGE_PLUSIEURS_RESULTATS=u"Résultats de recherche"
_DEFAULT_BEAUTIFULSOUP_PARSER="html.parser"
_TAILLE_THREADPOOL = 5
_NB_TENTATIVES_REQUETES = 30 # Nombre de tentatives de requêtes HTTP pour les pages de résultats (renvoie souvent une erreur CGI en cas de multithreading)
_NB_PAGES_RESULTATS_MAX = 100 # Nombre de pages de résultats maximum (on ne récupère que les _NB_PAGES_RESULTATS_MAX premières pages)
_TEMPS_ATTENTE_ENTRE_TENTATIVES_GETURL = 5

def aplatir_liste(liste):
    """ Transforme une liste de liste en une liste simple [[a,b],c] => [a,b,c]"""
    liste_aplatie = itertools.chain(*liste)
    return list(liste_aplatie)

def similar(a, b):
    """ Renvoie un score de similitude entre 2 chaines, =1 si ce sont les mêmes """
    similarite = SequenceMatcher(None, a, b).ratio()
    return round(similarite, 2)

class Client(object):
    """Fait les requêtes avec le serveur du catalogue des bibliothèques de Toulouse"""
    
    def __init__(self):
        """ Initialisation du client """
        self.session = requests.session()
        
    def _get(self, url):
        headers = {'Origin': 'http://catalogues.toulouse.fr',
                   'Accept-Encoding': 'gzip, deflate',
                   'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        return self.session.get(url, headers=headers).text
    
    def _construire_url_recherche(self):
        requete = ""
        if (self.titre_recherche != ""):
            requete = u"TI '%s'" % (self.titre_recherche)
            if (self.auteur_recherche != "") : requete += u" ET AU '%s'" % (self.auteur_recherche)
        elif (self.auteur_recherche != "") : requete = u"AU '%s'" % (self.auteur_recherche)
        requete=requete.strip()
        return (_URL_RECHERCHE+requete)
    
    def _normaliser_auteur(self, auteur_brut):
        """ A partir d'un auteur du type 'nom, prenom', renvoie une chaine 'prenom nom' """
        auteur=self._normaliser_chaine(auteur_brut)
        if len(auteur.split(',')) == 2 :
            nom, prenom = auteur.split(',')
            auteur = "%s %s" % (prenom.strip(), nom.strip())
        return auteur
    
    def _normaliser_titre(self, titre_brut):
        """ Normalise le titre (ex : 'Le meilleur des mondes /' => 'Le meilleur des mondes'"""
        titre=self._normaliser_chaine(titre_brut)
        if titre[-1] == '/' : titre = titre[:-1] # Les titres finissent souvent par '/', ex : "Le meilleur des mondes /"
        titre = titre.strip()
        return titre
            
    def _calcul_pertinence(self, titre, auteur):
        """ Calcule la pertinence du résultat, en fonction de la similarité entre le résultat et le titre et auteur recherché """
        pertinence = 1
        if self.titre_recherche != "":
            pertinence *= similar(self.titre_recherche.lower(), titre.lower())
        if self.auteur_recherche != "":
            pertinence *= similar(self.auteur_recherche.lower(), auteur.lower())
        return pertinence
    
    def _extraire_infos_page_detaillee(self, url="", soup="", page_html_detaillee=""):
        """ Extrait les infos de la page détaillée d'une oeuvre, via le résultat de beautifulsoup,
        via le code source de la page, ou via l'URL """
        
        try :
            dict_exemplaire = {}
        
            if (soup == ""):
                if (page_html_detaillee == "") :
                    nb_tentatives = 0
                    while True:
                        page_html_detaillee = self._get(url)
                        nb_tentatives += 1
                        if "Erreur CGI" not in page_html_detaillee : break # on refait la requête HTTP si elle renvoie une erreur
                        if nb_tentatives > _NB_TENTATIVES_REQUETES : break
                        sleep(_TEMPS_ATTENTE_ENTRE_TENTATIVES_GETURL)
                    
                    soup = BeautifulSoup(page_html_detaillee, _DEFAULT_BEAUTIFULSOUP_PARSER)
            
            auteur_brut = soup.select('div[id="auteur"] > a')
            if len(auteur_brut) > 0 : auteur_brut=auteur_brut[0].text.strip()
            else : auteur_brut = u""
            auteur = self._normaliser_auteur(auteur_brut)
            
            titre_brut = soup.select('td[width="95%"] > h1')
            if len(titre_brut) > 0 : titre_brut =  titre_brut[0].text.strip()
            else : titre_brut = u""
            titre = self._normaliser_titre(titre_brut)
        
            url_permanent = soup.select('#BW_link > input')
            if len(url_permanent) > 0 : url_permanent=url_permanent[0]["value"].strip()
            else : url_permanent = u""
        
            isbn = soup.select('#isbn_livre')
            if len(isbn) > 0 : isbn=isbn[0].text.strip()
            else : isbn = u""
            
            pertinence = self._calcul_pertinence(titre, auteur)
        
            tableau_exemplaires = soup.select('#exemplaire_table > tr')
            liste_exemplaires = []
            for ligne in tableau_exemplaires:
                cellules = ligne.select('td.holdingslistbab')
                if len(cellules) == 5: # Les lignes intéressantes contiennent 5 cellules
                    dict_exemplaire = { u'titre'         : titre,
                                        u'auteur'        : auteur,
                                        u'isbn'          : isbn,
                                        u'bibliotheque'  : self._normaliser_chaine(cellules[0].text),
                                        u'cote'          : self._normaliser_chaine(cellules[1].text),
                                        u'materiel'      : self._normaliser_chaine(cellules[2].text),
                                        u'localisation'  : self._normaliser_chaine(cellules[3].text),
                                        u'retour_attendu': self._normaliser_chaine(cellules[4].text),
                                        u'url_permanent' : url_permanent,
                                        u'pertinence'    : pertinence
                                     }
                    non_dispo = {u"Prêté", u"Document indisponible, acheminement en cours", u"Réservé", u"En traitement"}

                    if (dict_exemplaire[u'localisation'] in non_dispo) or (dict_exemplaire[u'materiel'] == ""):
                        dict_exemplaire[u'dispo'] = False
                    else : dict_exemplaire[u'dispo'] = True
                
                    liste_exemplaires.append(dict_exemplaire)
        except:
            liste_exemplaires = []
            raise
        
        return liste_exemplaires
    
    def _extraire_infos_page_plusieurs_resultats(self, soup=""):
        """ Extrait les infos de chacune des pages détaillées des résultats,
        via le résultat de beautifulsoup"""
        
        nb_resultats_temp = self._normaliser_chaine(soup.select('td[class="enrichcontentbab"] > h2')[0].text)
        nb_resultats = int(nb_resultats_temp.split(u"a repéré")[1].split(u"titres")[0].strip())
        
        url_premier_resultat = soup.select('td[class="itemlisting"] > h1 > a')[0]['href']
        url_premier_resultat = urljoin(_URL_BASE,url_premier_resultat)
        
        urls = []
        if nb_resultats > _NB_PAGES_RESULTATS_MAX : nb_resultats = _NB_PAGES_RESULTATS_MAX
        for indice_resultat in range(1,nb_resultats+1):
            urls.append(url_premier_resultat.replace(u"item=1", u"item=%d" % (indice_resultat)))
        
        liste_infos = []
        pool = ThreadPool(_TAILLE_THREADPOOL)
        liste_infos = pool.map(self._extraire_infos_page_detaillee, urls)
        pool.close() 
        pool.join()
        liste_infos = aplatir_liste(liste_infos)
        
        return liste_infos
    
    def _normaliser_chaine(self, chaine):
        return chaine.replace('\n',' ').replace('\r','').replace('\t',' ').replace('  ',' ').strip()
    
        
    def rechercher(self, titre="", auteur="", pertinence_minimum = 0.7):
        
        self.titre_recherche = titre
        self.auteur_recherche = auteur
        self.pertinence_minimum = pertinence_minimum
        
        liste_resultats = []
        
        nb_tentatives = 0
        while True:
            page_html_resultats = self._get(self._construire_url_recherche())
            nb_tentatives += 1
            if "Erreur CGI" not in page_html_resultats : break # on refait la requête HTTP si elle renvoie une erreur
            if nb_tentatives > _NB_TENTATIVES_REQUETES : break
            sleep(_TEMPS_ATTENTE_ENTRE_TENTATIVES_GETURL)

        soup = BeautifulSoup(page_html_resultats, _DEFAULT_BEAUTIFULSOUP_PARSER)
        
        if soup.title : # L'objet n'existe pas s'il n'y a pas de balise <TITLE> dans la page HTML
            titre_page = soup.title.string
    
            if titre_page == _TITRE_PAGE_UN_RESULTAT: # S'il n'y a qu'un seul résultat, la page est directement celle détaillée
                liste_resultats = self._extraire_infos_page_detaillee(soup=soup)
        
            elif _TITRE_PAGE_PLUSIEURS_RESULTATS in titre_page:
                liste_resultats = self._extraire_infos_page_plusieurs_resultats(soup=soup)
        
            else :
                raise RuntimeError(u"Page avec titre inconnu", titre_page)
        
        return liste_resultats