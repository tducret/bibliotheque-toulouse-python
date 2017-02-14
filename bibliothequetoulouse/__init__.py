# -*- coding: utf-8 -*-
r"""Les bibliothèques de Toulouse <http://www.bibliotheque.toulouse.fr/> proposent un très vaste choix de livres, DVD et autres créations.
:mod:`bibliotheque-toulouse` facilite la récupération des informations du catalogue (exemplaires disponibles, emplacement...).
Recherche des exemplaires disponibles du roman Le meilleur des mondes, d'Aldous Huxley ::
    >>> import bibliotheque-toulouse as bib
    >>> exemplaires_trouves = bib.rechercher("Le meilleur des mondes", "Aldous Huxley")
"""

__version__ = '0.1.7'

from bibliothequetoulouse.client import Client
import json

# Permet à Sphinx de récupérer ces éléments pour la documentation
__all__ = ['Client']

class Liste_resultats(object):
    """ Classe regroupant un liste de résultats d'une recherche dans le catalogue """
    def __init__(self, liste_resultats):
        self.liste_resultats = liste_resultats
    
    def __len__(self): # Méthode pour demander le nombre de résultats (ex : len(liste_resultats))
        return len(self.liste_resultats)
        
    def __getitem__(self, key): # Méthode pour interroger l'objet comme une liste (ex : liste_resultats[1])
        return Resultat(self.liste_resultats[key])
    
    def __repr__(self): # Méthode d'affichage de l'objet (ici, une sortie JSON indentée)
        return _pretty_print_json(self.liste_resultats)

class Resultat(object):
    """ Classe représentant un résultat de recherche dans le catalogue """
    def __init__(self, resultat):
        self.resultat = resultat
    
    def __getattr__(self, key): # Méthode pour récupérer la valeur d'un attribut (ex : resultat.titre)
        return self.resultat.get(key)
    
    def __getitem__(self, key): # Méthode pour récupérer la valeur d'un attribut comme un dictionnaire (ex : resultat["titre"])
        return self.resultat.get(key)
        
    def __repr__(self): # Méthode d'affichage de l'objet (ici, une sortie JSON indentée)
        return _pretty_print_json(self.resultat)

def _pretty_print_json(python_object):
    """ Renvoie une chaine JSON indentée """
    return json.dumps(python_object, ensure_ascii=False, indent=4, sort_keys=True).encode('utf-8').strip()
    
def rechercher(titre="", auteur="", pertinence_minimum=0.7, bibli_souhaitees=[], dispo_uniquement=False, sauf_braille=True):
    bib = Client()
    liste_resultats = bib.rechercher(titre, auteur)
    
    # Filtres
    liste_resultats_filtree = filter(lambda x: x['pertinence'] > pertinence_minimum, liste_resultats)
    if len(bibli_souhaitees) > 0: # On ne filtre pas sur les bibliothèques si aucune n'est spécifiée
        liste_resultats_filtree = filter(lambda x: x['bibliotheque'] in bibli_souhaitees, liste_resultats_filtree)
    if dispo_uniquement:
        liste_resultats_filtree = filter(lambda x: x['dispo'] == True, liste_resultats_filtree)
    if sauf_braille:
        liste_resultats_filtree = filter(lambda x: u'braille' not in x['materiel'].lower(), liste_resultats_filtree)
    
    return Liste_resultats(liste_resultats_filtree)