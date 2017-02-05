bibliothequetoulouse
====================================

[![Build Status](https://travis-ci.org/thibdct/bibliotheque-toulouse-python.svg?branch=master)](https://travis-ci.org/thibdct/bibliotheque-toulouse-python)

## Description

Ce package permet d'interroger très simplement le catalogue des [bibliothèques de Toulouse](http://bibliotheque.toulouse.fr).
 
## Pré-requis

 - Python 2.7

## Installation

    $ pip install -U bibliothequetoulouse

## Utilisation

Cet exemple permet de récupérer les informations sur les exemplaires **disponibles** d'un livre dans toutes les bibliothèques de Toulouse, et de les afficher au format JSON :

```python
# -*- coding: utf-8 -*-
import bibliothequetoulouse as bib

resultats = bib.rechercher(titre=u"le meilleur des mondes",
                           auteur=u"aldous huxley",
                           dispo_uniquement=True)

print("%d resultat(s)" % len(resultats))
print(resultats)
```

Cet exemple permet de récupérer les informations sur tous les exemplaires du même livre de la Médiathèque José Cabanis (disponibles à l'emprunt ou non) :

```python
# -*- coding: utf-8 -*-
import bibliothequetoulouse as bib

resultats = bib.rechercher(titre=u"le meilleur des mondes",
                           auteur=u"aldous huxley",
                           bibli_souhaitees=[u'Médiathèque José Cabanis'])

for res in resultats:
    print("Cote : %s / Localisation : %s" % (res.cote, res.localisation))
```