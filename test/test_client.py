# -*- coding: utf-8 -*-
import bibliothequetoulouse as bib

def test_recherche_classique():
    resultats = bib.rechercher(titre=u"le meilleur des mondes",
                               auteur=u"aldous huxley",
                               bibli_souhaitees=[u'Médiathèque José Cabanis'])
    assert len(resultats) > 0
