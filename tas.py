class Tas():
    '''Classe représentant un tas.
    Le tas est représenté par une liste de tuples (indice, valeur, priorité).'''

    # CONSTRUCTEUR

    def __init__(self):
        self.valeur = []
        self.priorite = []

    # REQUETES

    def racine(self) -> tuple:
        '''Renvoie la racine du tas sous forme d'un tuple (valeur, priorité)'''
        return (self.valeur[0], self.priorite[0])
    
    def taille(self) -> int:
        '''Renvoie la taille du tas'''
        return len(self.valeur)

    # COMMANDES

    def supprimer(self) -> tuple:
        '''Supprime la racine du tas et réorganise le tas en conséquences
        Renvoie la racine supprimée sous forme d'un tuple (valeur, priorité)'''
        self.__echange(0, len(self.valeur) - 1)
        self.valeur.pop()
        self.priorite.pop()
        self.__vers_le_bas(1)
    
    def inserer(self, v, p) -> tuple:
        '''Insére l'élément de valeur v et de prorité p dans le tas
        à sa bonne place'''
        self.valeur.append(v)
        self.priorite.append(p)
        self.__vers_le_haut(len(self.valeur))
    
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
        if 2 * i + 1 < len(self.priorite):
            if self.priorite[2 * i - 1] > self.priorite[2 * i]:
                fils = 2 * i + 1
        # fils contient le fils de i de priorité le plus faible
        if fils < len(self.priorite) and self.priorite[fils - 1] < self.priorite[i - 1]:
            self.__echange(i - 1, fils - 1)
            self.__vers_le_bas(fils)
        
    def __vers_le_haut(self, i: int):
        '''Réorganise le tas en remontant l'élément d'indice i vers le haut'''
        if i > 1:
            if self.priorite[(i // 2) - 1] > self.priorite[i - 1]:
                self.__echange(i - 1, i // 2 - 1)
                self.__vers_le_haut(i // 2)
    
    # AFFICHAGE

    def __str__(self):
        '''Affiche le tas'''
        return str(self.valeur) + str(self.priorite)
