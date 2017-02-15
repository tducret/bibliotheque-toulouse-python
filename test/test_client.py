# -*- coding: utf-8 -*-
from __future__ import print_function
import bibliothequetoulouse as bib

def afficher_liste_resultats(liste_resultats):
    print("%d resultat(s)" % len(liste_resultats))
    print(liste_resultats)
    for resultat in liste_resultats:
        afficher_resultat_detaille(resultat)

def afficher_resultat_detaille(resultat):
    print(resultat)
    print(u"Affichage par __getattr__")
    print(u"Titre : %s" % (resultat.titre))
    print(u"Auteur : %s" % (resultat.auteur))
    print(u"ISBN : %s" % (resultat.isbn))
    print(u"Bibliotheque : %s" % (resultat.bibliotheque))
    print(u"Cote : %s" % (resultat.cote))
    print(u"Materiel : %s" % (resultat.materiel))
    print(u"Localisation : %s" % (resultat.localisation))
    print(u"Retour attendu : %s" % (resultat.retour_attendu))
    print(u"URL permanente : %s" % (resultat.url_permanent))
    print(u"Pertinence : %.2f" % (resultat.pertinence))
    print(u"Disponibilité : %s" % (resultat.dispo))
    print()
    print(u"Affichage par __getitem__")
    print(u"Titre : %s" % (resultat['titre']))
    print(u"Auteur : %s" % (resultat['auteur']))
    print(u"ISBN : %s" % (resultat['isbn']))
    print(u"Bibliotheque : %s" % (resultat['bibliotheque']))
    print(u"Cote : %s" % (resultat['cote']))
    print(u"Materiel : %s" % (resultat['materiel']))
    print(u"Localisation : %s" % (resultat['localisation']))
    print(u"Retour attendu : %s" % (resultat['retour_attendu']))
    print(u"URL permanente : %s" % (resultat['url_permanent']))
    print(u"Pertinence : %.2f" % (resultat['pertinence']))
    print(u"Disponibilité : %s" % (resultat['dispo']))
        
def test_recherche_classique():
    resultats = bib.rechercher(titre=u"Les raisins de la colère",
                               auteur=u"John Steinbeck",
                               bibli_souhaitees=[u'Saint-Cyprien'])
    afficher_liste_resultats(resultats)
    assert len(resultats) > 0

def test_recherche_une_seule_page_detaillee():
    resultats = bib.rechercher(titre=u"L'homme sans argent",
                               auteur=u"Mark Boyle")
    print(resultats) # Sortie JSON
    assert len(resultats) > 0

def test_dispo_uniquement():
    resultats = bib.rechercher(titre=u"le meilleur des mondes",
                           auteur=u"aldous huxley",
                           dispo_uniquement=True)
    assert len(resultats) > 0

def test_auteur_seulement():
    resultats = bib.rechercher(auteur=u"cyprien iov")
    assert len(resultats) > 0
    
def test_titre_seulement():
    resultats = bib.rechercher(titre=u"Roger et ses humains")
    assert len(resultats) > 0
    
def test_aucun_resultat():
    resultats = bib.rechercher(titre=u"fdsfkjsdlkfjds",
                               auteur=u"klfjzelkfjelz")
    assert len(resultats) == 0

def test_avec_braille():
    resultats_sans_braille = bib.rechercher(titre=u"le meilleur des mondes",
                               auteur=u"aldous huxley", sauf_braille=True)
    resultats_avec_braille = bib.rechercher(titre=u"le meilleur des mondes",
                               auteur=u"aldous huxley", sauf_braille=False)

    assert len(resultats_sans_braille) < len(resultats_avec_braille)