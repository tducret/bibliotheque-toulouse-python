# -*- coding: utf-8 -*-
import bibliothequetoulouse as bib

def test_recherche_classique():
    resultats = bib.rechercher(titre=u"le meilleur des mondes",
                               auteur=u"aldous huxley",
                               bibli_souhaitees=[u'Médiathèque José Cabanis'])
    print("%d resultat(s)" % len(resultats))
    print(resultats) # Sortie JSON
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
    resultats = bib.rechercher(auteur=u"aldous huxley")
    assert len(resultats) > 0
    
def test_titre_seulement():
    resultats = bib.rechercher(titre=u"le meilleur des mondes")
    assert len(resultats) > 0
    
# TODO : Ajout de tests pour afficher la liste, obtenir des éléments : resultats[0] res['dispo'], res.dispo 