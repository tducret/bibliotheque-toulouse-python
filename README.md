bibliothequetoulouse
====================================

## Description

Ce package permet d'interroger très simplement le catalogue des [bibliothèques de Toulouse](http://bibliotheque.toulouse.fr).
 
## Pré-requis

 - Python 2.7

## Installation

    $ pip install -U bibliothequetoulouse

## Utilisation

Cet exemple permet de récupérer les informations sur les exemplaires d'un livre dans les bibliothèques de Toulouse, et de les afficher au format JSON :

```python
import bibliothequetoulouse as bib
import json

liste_resultats = bib.rechercher(titre=u"le meilleur des mondes", auteur=u"aldous huxley")
print json.dumps(liste_resultats, ensure_ascii=False, indent=4, sort_keys=True)
print "%d resultat(s)" % len(liste_resultats)
```