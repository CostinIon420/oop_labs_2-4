from abc import ABC, abstractmethod
from random import randint, choice

# Clasa abstractă EntitateEcosistem
class EntitateEcosistem(ABC):
    def __init__(self, nume, energie, pozitie, rataSupravietuire):
        self.nume = nume
        self.energie = energie
        self.pozitie = pozitie  # tuple (x, y)
        self.rataSupravietuire = rataSupravietuire

    @abstractmethod
    def actioneaza(self):
        pass

    @abstractmethod
    def reproduce(self):
        pass


# Clasa Planta
class Planta(EntitateEcosistem):
    def __init__(self, nume, energie, pozitie, rataSupravietuire, resurse):
        super().__init__(nume, energie, pozitie, rataSupravietuire)
        self.resurse = resurse

    def actioneaza(self):
        self.creste()

    def creste(self):
        self.resurse += 1  # Crește resursele în timp

    def reproduce(self):
        if self.resurse > 5:  # Condiție pentru reproducere
            self.resurse -= 5
            return Planta(self.nume, 10, (randint(0, 10), randint(0, 10)), self.rataSupravietuire, 3)
        return None


# Clasa abstractă Animal
class Animal(EntitateEcosistem):
    def __init__(self, nume, energie, pozitie, rataSupravietuire, viteza, tipHrana):
        super().__init__(nume, energie, pozitie, rataSupravietuire)
        self.viteza = viteza
        self.tipHrana = tipHrana

    @abstractmethod
    def mananca(self, hrana):
        pass

    @abstractmethod
    def deplaseaza(self):
        pass
class Erbivor(Animal):
    def __init__(self, nume, energie, pozitie, rataSupravietuire, viteza):
        super().__init__(nume, energie, pozitie, rataSupravietuire, viteza, tipHrana="plante")

    def mananca(self, planta):
        if isinstance(planta, Planta):
            self.energie += planta.resurse
            planta.resurse = 0  # Planta este consumată
        else:
            raise ValueError("Erbivorul poate consuma doar plante.")

    def deplaseaza(self):
        dx = randint(-self.viteza, self.viteza)
        dy = randint(-self.viteza, self.viteza)
        self.pozitie = (self.pozitie[0] + dx, self.pozitie[1] + dy)

    def actioneaza(self):
        self.deplaseaza()
        self.energie -= 1  # Pierde energie în timpul deplasării

    def reproduce(self):
        if self.energie > 20:  # Condiție pentru reproducere
            self.energie -= 10
            return Erbivor(self.nume, 10, self.pozitie, self.rataSupravietuire, self.viteza)
        return None
class Carnivor(Animal):
    def __init__(self, nume, energie, pozitie, rataSupravietuire, viteza):
        super().__init__(nume, energie, pozitie, rataSupravietuire, viteza, tipHrana="animale")

    def mananca(self, prada):
        if isinstance(prada, Animal):
            self.energie += prada.energie
            prada.energie = 0  # Prada este consumată (moartă)
        else:
            raise ValueError("Carnivorul poate consuma doar animale.")

    def deplaseaza(self):
        dx = randint(-self.viteza, self.viteza)
        dy = randint(-self.viteza, self.viteza)
        self.pozitie = (self.pozitie[0] + dx, self.pozitie[1] + dy)

    def actioneaza(self):
        self.deplaseaza()
        self.energie -= 2  # Pierde mai multă energie în timpul deplasării

    def reproduce(self):
        if self.energie > 30:  # Condiție pentru reproducere
            self.energie -= 15
            return Carnivor(self.nume, 15, self.pozitie, self.rataSupravietuire, self.viteza)
        return None
class Omnivor(Animal):
    def __init__(self, nume, energie, pozitie, rataSupravietuire, viteza):
        super().__init__(nume, energie, pozitie, rataSupravietuire, viteza, tipHrana="mixt")

    def mananca(self, hrana):
        if isinstance(hrana, Planta):
            self.energie += hrana.resurse
            hrana.resurse = 0  # Planta este consumată
        elif isinstance(hrana, Animal):
            self.energie += hrana.energie
            hrana.energie = 0  # Animalul este consumat
        else:
            raise ValueError("Omnivorul poate consuma plante sau animale.")

    def deplaseaza(self):
        dx = randint(-self.viteza, self.viteza)
        dy = randint(-self.viteza, self.viteza)
        self.pozitie = (self.pozitie[0] + dx, self.pozitie[1] + dy)

    def actioneaza(self):
        self.deplaseaza()
        self.energie -= 1  # Pierde energie în timpul deplasării

    def reproduce(self):
        if self.energie > 25:  # Condiție pentru reproducere
            self.energie -= 12
            return Omnivor(self.nume, 12, self.pozitie, self.rataSupravietuire, self.viteza)
        return None
class Interactiune:
    def ataca(self, prada):
        pass

    def reproduce(self):
        pass
class Ecosistem:
    def __init__(self, dimensiune):
        self.dimensiune = dimensiune  # Dimensiunea hărții (ex. 10x10)
        self.harta = [[None for _ in range(dimensiune)] for _ in range(dimensiune)]
        self.entitati = []  # Lista tuturor entităților

    def adauga_entitate(self, entitate):
        x, y = entitate.pozitie
        if 0 <= x < self.dimensiune and 0 <= y < self.dimensiune:
            self.harta[x][y] = entitate
            self.entitati.append(entitate)

    def elimina_entitate(self, entitate):
        x, y = entitate.pozitie
        self.harta[x][y] = None
        self.entitati.remove(entitate)

    def simuleaza_pas(self):
        for entitate in list(self.entitati):
            entitate.actioneaza()

            # Eliminare dacă energia este zero
            if entitate.energie <= 0:
                self.elimina_entitate(entitate)

            # Reproducere
            progenitura = entitate.reproduce()
            if progenitura:
                self.adauga_entitate(progenitura)

    def afiseaza_stare(self):
        for i in range(self.dimensiune):
            for j in range(self.dimensiune):
                if self.harta[i][j]:
                    print(f"[{self.harta[i][j].nume[0]}]", end="")
                else:
                    print("[ ]", end="")
            print()
# Exemplu de utilizare
if __name__ == "__main__":
    ecosistem = Ecosistem(dimensiune=10)

    # Adăugăm câteva plante și animale
    planta1 = Planta("Iarba", 10, (2, 3), 0.9, 5)
    erbivor1 = Erbivor("Iepure", 20, (4, 5), 0.8, 2)
    carnivor1 = Carnivor("Lup", 30, (6, 7), 0.7, 3)
    omnivor1 = Omnivor("Urs", 40, (1, 1), 0.85, 2)

    ecosistem.adauga_entitate(planta1)
    ecosistem.adauga_entitate(erbivor1)
    ecosistem.adauga_entitate(carnivor1)
    ecosistem.adauga_entitate(omnivor1)

    # Simulăm 5 pași
    for _ in range(5):
        ecosistem.simuleaza_pas()
        ecosistem.afiseaza_stare()
        print("-" * 20)
class Ecosistem:
    def __init__(self, dimensiune):
        self.dimensiune = dimensiune  # Dimensiunea hărții (ex. 10x10)
        self.harta = [[None for _ in range(dimensiune)] for _ in range(dimensiune)]
        self.entitati = []  # Lista tuturor entităților

    def adauga_entitate(self, entitate):
        x, y = entitate.pozitie
        if 0 <= x < self.dimensiune and 0 <= y < self.dimensiune:
            self.harta[x][y] = entitate
            self.entitati.append(entitate)

    def elimina_entitate(self, entitate):
        x, y = entitate.pozitie
        self.harta[x][y] = None
        self.entitati.remove(entitate)

    def simuleaza_pas(self):
        for entitate in list(self.entitati):
            entitate.actioneaza()

            # Eliminare dacă energia este zero
            if entitate.energie <= 0:
                self.elimina_entitate(entitate)

            # Reproducere
            progenitura = entitate.reproduce()
            if progenitura:
                self.adauga_entitate(progenitura)

    def afiseaza_stare(self):
        # Afișare hartă
        print("Harta ecosistemului:")
        for i in range(self.dimensiune):
            for j in range(self.dimensiune):
                if self.harta[i][j]:
                    entitate = self.harta[i][j]
                    if isinstance(entitate, Planta):
                        simbol = "P"
                    elif isinstance(entitate, Erbivor):
                        simbol = "E"
                    elif isinstance(entitate, Carnivor):
                        simbol = "C"
                    elif isinstance(entitate, Omnivor):
                        simbol = "O"
                    else:
                        simbol = "?"
                    print(f"[{simbol}]", end="")
                else:
                    print("[ ]", end="")
            print()

        # Afișare detalii entități
        print("\nDetalii entități:")
        numar_plante = sum(1 for e in self.entitati if isinstance(e, Planta))
        numar_erbivore = sum(1 for e in self.entitati if isinstance(e, Erbivor))
        numar_carnivore = sum(1 for e in self.entitati if isinstance(e, Carnivor))
        numar_omnivore = sum(1 for e in self.entitati if isinstance(e, Omnivor))

        print(f"Total entități: {len(self.entitati)}")
        print(f"Plante: {numar_plante}, Erbivore: {numar_erbivore}, Carnivore: {numar_carnivore}, Omnivore: {numar_omnivore}\n")

        for entitate in self.entitati:
            print(f"{entitate.nume} (Tip: {type(entitate).__name__}) - Energie: {entitate.energie}, Poziție: {entitate.pozitie}")
def simuleaza_pas(self):
    for entitate in list(self.entitati):
        entitate.actioneaza()

        # Carnivor atacă erbivor
        if isinstance(entitate, Carnivor):
            for alta_entitate in self.entitati:
                if isinstance(alta_entitate, Erbivor) and self._sunt_aproape(entitate.pozitie, alta_entitate.pozitie):
                    entitate.mananca(alta_entitate)
                    self.elimina_entitate(alta_entitate)
                    break

        # Erbivor mănâncă plante
        if isinstance(entitate, Erbivor):
            for alta_entitate in self.entitati:
                if isinstance(alta_entitate, Planta) and self._sunt_aproape(entitate.pozitie, alta_entitate.pozitie):
                    entitate.mananca(alta_entitate)
                    if alta_entitate.energie <= 0:
                        self.elimina_entitate(alta_entitate)
                    break

        # Eliminare dacă energia este zero
        if entitate.energie <= 0:
            self.elimina_entitate(entitate)

        # Reproducere
        progenitura = entitate.reproduce()
        if progenitura:
            self.adauga_entitate(progenitura)

# Verifică dacă două entități sunt aproape una de cealaltă
def _sunt_aproape(self, pozitie1, pozitie2):
    return abs(pozitie1[0] - pozitie2[0]) <= 1 and abs(pozitie1[1] - pozitie2[1]) <= 1
