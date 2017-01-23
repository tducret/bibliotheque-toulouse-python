# -*- coding: utf-8 -*-
r"""Les bibliothèques de Toulouse <http://www.bibliotheque.toulouse.fr/> proposent un très vaste choix de livres, DVD et autres créations.
:mod:`bibliotheque-toulouse` facilite la récupération des informations du catalogue (exemplaires disponibles, emplacement...).
Recherche des exemplaires disponibles du roman Le meilleur des mondes, d'Aldous Huxley ::
    >>> import bibliotheque-toulouse as bib
    >>> exemplaires_trouves = bib.rechercher("Le meilleur des mondes", "Aldous Huxley")
"""

__version__ = '0.1.1'

from bibliothequetoulouse.client import Client

# Permet à Sphinx de récupérer ces éléments pour la documentation
__all__ = ['Client']

def rechercher(titre="", auteur=""):
    bib = Client()
    liste_resultats = bib.rechercher(titre, auteur)
    return liste_resultats