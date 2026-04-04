from pilefile import Pile, File
from graphelib import Graphe
l="(0,0)"
ll=[[1,2],[3,4],[5,6]]
print(ll[int(l[1])][int(l[3])])

laby = [[0, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 0]]


class Labyrinte:
    def __init__(self,lab,depart, arrivee):
        self.lab = lab
        self.depart = depart
        self.arrivee = arrivee
        self.objet=Graphe()
        lignes = len(self.lab)
        colonnes = len(self.lab[0])
# ajout les voisin
        for x in range(lignes):
            for y in range(colonnes):

                if self.lab[x][y] == 0:
                    point = (x, y)

                    directions = [(x - 1, y),  (x + 1, y), (x, y - 1),  (x, y + 1)]
                    for nx, ny in directions:

                        if 0 <= nx < lignes and 0 <= ny < colonnes:
                            if self.lab[nx][ny] == 0:
                                voisin = (nx, ny)
                                self.objet.ajouteArete(point, voisin)
                                




    #dfs

    def parcours_profondeur_laby(self, G,depart,arrivee):
        '''Parcours d'un graphe en profondeur Ã  partir du sommet dÃ©part'''

        marque = set()# ensemble des sommets deja visitÃ©s
        if depart==arrivee:
            print(marque)

        def parcours_aux(G, som):

            marque.add(som)

            for voisin in som.listeVoisins():
                if voisin not in marque:
                    parcours_aux(G, voisin)

        parcours_aux(G, depart)

    #bfs
    def parcours_largeur_laby(self, G, depart, arrivee):
        '''Parcours d'un graphe en largeur Ã  partir du sommet dÃ©part'''
        marque = set()
        f = File()
        f.enfile(depart)
        while not f.estvide():
            s = f.defile()
            if s not in marque:
                marque.add(s)
                traite_sommet(s)
                for s2 in s.listeVoisins():
                    if s2 not in marque:
                        f.enfile(s2)

    def solutiondfst(self):
        return self.parcours_profondeur_laby(self.objet,self.depart,self.arrivee)



c=Labyrinte(laby,'(0,0)', "(4,4)")
print(c.solutiondfst())


