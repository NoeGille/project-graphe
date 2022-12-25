from enum import Enum

class Couleur(Enum):
    '''Enumération des couleurs qui représente l'état d'exploration d'un sommet pour
    le parcours en profondeur'''
    BLANC = 0
    GRIS = 1
    NOIR = 2
