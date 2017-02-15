bibliothequetoulouse
=======

[![Build Status](https://travis-ci.org/thibdct/bibliotheque-toulouse-python.svg?branch=master)](https://travis-ci.org/thibdct/bibliotheque-toulouse-python)
[![Coverage Status](https://coveralls.io/repos/github/thibdct/bibliotheque-toulouse-python/badge.svg)](https://coveralls.io/github/thibdct/bibliotheque-toulouse-python)
![License](https://img.shields.io/badge/license-MIT-lightgray.svg) 

Description
=======

Ce package permet d'interroger très simplement le catalogue des [bibliothèques de Toulouse](http://bibliotheque.toulouse.fr).
 
Pré-requis
=======

 - Python 2.7 ou 3.6

Installation
=======

    $ pip install -U bibliothequetoulouse

Utilisation
=======

* Pour récupérer les informations sur les exemplaires **disponibles** d'un livre dans toutes les bibliothèques de Toulouse, et de les afficher au format JSON

```python
# -*- coding: utf-8 -*-
import bibliothequetoulouse as bib

resultats = bib.rechercher(titre=u"le meilleur des mondes",
                           auteur=u"aldous huxley",
                           dispo_uniquement=True)

print("%d resultat(s)" % len(resultats))
print(resultats)
```

Ce qui renverra ce type de résultats :

```
[
    {
        "auteur": "Aldous Huxley", 
        "bibliotheque": "Ancely", 
        "cote": "TE F HUX", 
        "dispo": true, 
        "isbn": "", 
        "localisation": "Textes enregistrés", 
        "materiel": "Texte imprimé pour tout public", 
        "pertinence": 1.0, 
        "retour_attendu": "", 
        "titre": "Le meilleur des mondes", 
        "url_permanent": "http://catalogues.toulouse.fr/web2/tramp2.exe/do_keyword_search/log_in?setting_key=BMT1&servers=1home&query=ELC2608081&screen=hitlist.html"
    }, 
    {
        "auteur": "Aldous Huxley", 
        "bibliotheque": "Médiathèque José Cabanis", 
        "cote": "F HUXL", 
        "dispo": true, 
        "isbn": "", 
        "localisation": "Etage 2 - Littératures : Textes enregistrés", 
        "materiel": "Texte imprimé pour tout public", 
        "pertinence": 1.0, 
        "retour_attendu": "", 
        "titre": "Le meilleur des mondes", 
        "url_permanent": "http://catalogues.toulouse.fr/web2/tramp2.exe/do_keyword_search/log_in?setting_key=BMT1&servers=1home&query=ELC2608081&screen=hitlist.html"
    }
]
```

* Pour récupérer les informations sur tous les exemplaires du même livre à la **Médiathèque José Cabanis** (disponibles à l'emprunt ou non) :

```python
# -*- coding: utf-8 -*-
import bibliothequetoulouse as bib

resultats = bib.rechercher(titre=u"le meilleur des mondes",
                           auteur=u"aldous huxley",
                           bibli_souhaitees=[u'Médiathèque José Cabanis'])

for res in resultats:
    print("Cote : %s / Localisation : %s" % (res.cote, res.localisation))
```

Ce qui renverra par exemple :

```
Cote : F HUXL / Localisation : Etage 2 - Littératures : Textes enregistrés
Cote : TE HUXL / Localisation : Prêté
Cote : F HUXL / Localisation : Réserve pôle Littérature
Cote : F HUXL / Localisation : Prêté
Cote : RTF HUXL / Localisation : Prêté
```