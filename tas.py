import matplotlib.pyplot as plt

class Tas():
    '''Classe représentant un tas.
    Le tas est représenté par une liste de tuples (indice, valeur, priorité).'''

    # CONSTRUCTEUR

    def __init__(self):
        self.valeur = []
        self.priorite = []

    # COMMANDES

    def supprimer(self) -> tuple:
        '''Supprime la racine du tas et réorganise le tas en conséquences
        Renvoie la racine supprimée sous forme d'un tuple (valeur, priorité)'''
        #TODO
        pass
    
    def inserer(self, v, p) -> tuple:
        '''Insére l'élément de valeur v et de prorité p dans le tas
        à sa bonne place'''
        #TODO
        pass
    
    # OUTILS

    def __echange(self, i: int, j: int):
        '''Echange les éléments d'indice i et j dans le tas'''
        temp = self.valeur[i]
        self.valeur[i] = self.valeur[j]
        self.valeur[j] = temp
        temp = self.priorite[i]
        self.priorite[i] = self.priorite[j]
        self.priorite[j] = temp
    
    def __vers_le_bas(self, i: int):
        '''Réorganise le tas en descendant l'élément d'indice i vers le bas'''
        fils = 2 * i
        if self.priorite(2 * i) > self.priorite(2 * i + 1):
            fils = 2 * i + 1
        # fils contient le fils de i de priorité le plus faible
        if len(self.priorite) < fils:
            self.__echange(i, fils)
            self.__vers_le_bas(fils)
        
    def __vers_le_haut(self, i: int):
        '''Réorganise le tas en remontant l'élément d'indice i vers le haut'''
        if i > 1:
            if self.priorite(i // 2) > self.priorite(i):
                self.__echange(i, i // 2)
                self.__vers_le_haut
    
    # AFFICHAGE

    def __str__(self):
        '''Affiche le tas'''
        return str(self.valeur) + str(self.priorite)