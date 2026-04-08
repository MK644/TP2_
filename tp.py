from pilefile import Pile, File
from graphelib import Graphe

import turtle



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

        def coord(s):
            s = s.strip().strip("()") # enleve les espaces + parenthese
            parties = s.split(",")
            if len(parties) != 2:
                raise ValueError("Format invalide")
            try:
                return (int(parties[0].strip()), int(parties[1].strip()))
            except ValueError:
                raise ValueError("coordonner non entiere")

        self.depart = coord(depart)
        self.arrivee = coord(arrivee)

        self.lab = lab
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
        arrivee=G.sommet(arrivee)
        marque = set()# ensemble des sommets deja visité
        chemin=[]
        def parcours_aux(G, som):
            chemin.append(som)

            if som._nom == arrivee._nom:

                return True
            marque.add(som)
            for voisin in som.listeVoisins():

                if voisin not in marque:
                    if parcours_aux(G, voisin):
                        return True
            chemin.pop() #si la fonction recule, elle enleve le point qu'elle avait parcourue
            return False

        if parcours_aux(G, G.sommet(depart)):
            print("Sommets visités :", [str(s._nom) for s in chemin])
            return chemin
        else:
            print('Aucun chemin.')
            return None

    #bfs
    def parcours_largeur_laby(self, G, depart, arrivee):
        '''Parcours d'un graphe en largeur Ã  partir du sommet dÃ©part'''
        marque = set()
        chemin=[]
        parent={}
        parent[depart] = None
        depart=G.sommet(depart)
        arrivee=G.sommet(arrivee)
        f = File()
        f.enfile(depart)
        while not f.estvide():
            s = f.defile()
            if s._nom == arrivee._nom:

                break

            if s not in marque:
                marque.add(s)

                for voisin in s.listeVoisins():
                    if voisin not in marque and voisin not in parent:
                        f.enfile(voisin)
                        parent[voisin] = s

        courant = arrivee
        while courant is not None:
            chemin.append(courant)
            courant = parent.get(courant)
        chemin.reverse()
        print("Sommets visités :", [str(s._nom) for s in chemin])
        return chemin



    def solutiondfst(self):
        return self.parcours_profondeur_laby(self.objet,self.depart,self.arrivee)
    def solutionbfs(self):
        return self.parcours_largeur_laby(self.objet,self.depart,self.arrivee)

    def visualiser(self, chemin, titre="Solution Labyrinthe", couleur_chemin="blue"):
        """
        chemin : la liste des objets Sommet renvoyée par tes fonctions de solution
        """
        # On calcule la distance directement ici au lieu de la demander aux algos
        # La distance est le nombre de cases du chemin - 1 (les arêtes)
        distance = len(chemin) - 1 if chemin else 0

        # On récupère les dimensions depuis self.lab (puisque self.nb_lignes n'est pas défini dans le __init__)
        nb_lignes = len(self.lab)
        nb_cols = len(self.lab[0])
        TAILLE = 30

        ecran = turtle.Screen()
        ecran.setup(width=600, height=600)
        ecran.title(f"{titre} - Distance: {distance} arêtes")
        ecran.tracer(0)

        t = turtle.Turtle()
        t.hideturtle()

        # Calcul pour centrer parfaitement
        ox = -nb_cols * TAILLE / 2
        oy = nb_lignes * TAILLE / 2

        # Dessin de la grille
        for x in range(nb_lignes):
            for y in range(nb_cols):
                px, py = ox + y * TAILLE, oy - x * TAILLE

                # Choix de la couleur
                if self.lab[x][y] == 1:
                    color = "black"
                elif (x, y) == self.depart:
                    color = "green"
                elif (x, y) == self.arrivee:
                    color = "red"
                else:
                    color = "white"

                t.penup()
                t.goto(px, py)
                t.pendown()
                t.fillcolor(color)
                t.begin_fill()
                for _ in range(4):
                    t.forward(TAILLE)
                    t.right(90)
                t.end_fill()

        ecran.update()

        # Dessin du chemin
        if chemin:
            ecran.tracer(1)
            t.penup()
            t.pensize(3)
            t.pencolor(couleur_chemin)

            for i, etape in enumerate(chemin):
                # Tes algos retournent des objets "Sommet" de graphelib.
                # L'attribut _nom contient déjà le tuple de coordonnées (x, y) ! Pas besoin de eval().
                coord_tuple = etape._nom

                # Aller au centre de la case
                cx = ox + coord_tuple[1] * TAILLE + TAILLE / 2
                cy = oy - coord_tuple[0] * TAILLE - TAILLE / 2
                t.goto(cx, cy)
                t.pendown()
                if i == 0:
                    t.dot(10, "green")

            t.dot(10, "red")

        print(f"Visualisation terminée. Distance : {distance}")
        turtle.done()



c = Labyrinte(laby, '(0,0)', '(7,4)')
c.solutionbfs()
c.solutiondfst()
# On récupère juste le chemin
chemin_bfs = c.solutionbfs()

# On passe ce chemin directement à la visualisation
c.visualiser(chemin_bfs, titre="Solution DFS", couleur_chemin="blue")
