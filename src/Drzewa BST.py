import random
import math
import matplotlib.pyplot as plt



def losuj(lista):										#Fisher-Yates shuffle
    for i in range(len(lista) - 1, 0, -1):				#iteracja po "liscie" od ostatniego elementu
        j = random.randint(0, i)						#losowanie j z przedzialu 0,i włącznie
        lista[i], lista[j] = lista[j], lista[i]			#zamiana miejsc i z j

class Node:
    def __init__(self, v):
        self.value = v                                  # przechowanie wartości
        self.left = None                                # wskaźnik lewego potomka
        self.right = None                               # wskaźnik prawego potomka

class BST:
    def __init__(self):
        self.root = None								#korzeń drzewa is null, pusty

    def dodaj(self, v):									#dodawanie nowej wartosci do drzewa
        if self.root is None:							#jesli jest puste
            self.root = Node(v)							#nowy korzen
        else:
            self._dodaj(self.root, v)					# a jesli nie, wywoalnie rekurencyjnego wstawiania

    def _dodaj(self, node, v):							# rekurencyjne wstawianie
        if v < node.value:								# jesli wartosc mniejsza, idziemy w lewo
            if node.left is None:
                node.left = Node(v)
            else:
                self._dodaj(node.left, v)               # Jeśli znajdziemy wolne miejsce, tworzymy nowy węzeł
        elif v > node.value:							# jesli wieksza, to w prawo
            if node.right is None:
                node.right = Node(v)
            else:
                self._dodaj(node.right, v)              # # Jeśli znajdziemy wolne miejsce, tworzymy nowy węzeł

    def wysokosc(self):									# obliczanie wysokosci drzewa
        def f(n):										
            if n is None:
                return -1                               # jesli napotkamy puste drzewo, zwraca -1
            return 1 + max(f(n.left), f(n.right))       # sprawdzamy wys. lewej i prawej galęzi, zwraca większą z nich +1
        return f(self.root)

    def liscie(self):									# liczenie liczby liści
        def f(n):										# lisc to węzeł  bez dzieci
            if n is None:
                return 0
            if n.left is None and n.right is None:      # jeśli oba "dzieci" puste - zwraca 1
                return 1
            return f(n.left) + f(n.right)               # w przeciwnym razie, sumujemy liście z prawej i lewej
        return f(self.root)

    def srednia_glebokosc(self):						# srednia glebokosc wezłow
        def f(n, g):									# g - aktualna glebokosc
            if n is None:                               # jesli puste, zwracamy 0
                return (0, 0)							
            l_sum, l_ile = f(n.left, g + 1)             # suma glebokosci, liczba wezlow z lewej
            r_sum, r_ile = f(n.right, g + 1)            # suma glebokosci, liczba wezlow z prawej
            return (l_sum + r_sum + g, l_ile + r_ile + 1) # dodajemy głębokości po przejściu przez lewe i prawe
        suma, ile = f(self.root, 0)
        return suma / ile if ile > 0 else 0             # sumę głębkości dzielimy przez liczbę węzłów

def std(dane):                                          # funkcja obliczająca odchylenie standardowe
    s = sum(dane) / len(dane)                           # średnia z danych
    return math.sqrt(sum((x - s) ** 2 for x in dane) / len(dane))      # wzor na odchylenie za pomocą "import math"

def korelacja(x, y):                                    # funkcja licząca korelacje Pearsona między dwiema listami
    n = len(x)
    sx = sum(x) / n                                     # średnia z X
    sy = sum(y) / n                                     # średnia z Y
    licznik = sum((x[i] - sx)*(y[i] - sy) for i in range(n))    # suma iloczynów odchyleń
    mianownik = math.sqrt(sum((x[i] - sx)**2 for i in range(n)) * sum((y[i] - sy)**2 for i in range(n)))    # pierwiastek z iloczynu sum kwadratów
    return licznik / mianownik if mianownik != 0 else 0     # zwróc wynik lub 0, jeśli mianownik = 0

def iqr(dane):                                          # funkcja licząca odstęp międzykwartylowy
    dane_posortowane = posortowane(dane)                # posortowana lista
    n = len(dane_posortowane)
    q1_index = n // 4                                   # indeks I kwartylu
    q3_index = (3 * n) // 4                             # indeks III kwartylu
    return dane_posortowane[q3_index] - dane_posortowane[q1_index]  # różnica Q3 - Q1

if __name__ == "__main__":                              # Główna część programu, uruchamiana tylko bezpośrednio
    h, l, d = [], [], []                                        # Listy: wysokości, liści, głębkości
    for p in range(300):                                        # 300 prób
        dane = list(range(10000))                               # Lista 0-9999
        losuj(dane)                                           # pomieszanie listy
        drzewo = BST()                                          # tworzymy nowe drzewo BST
        for x in dane:                                          # dodajemy wszystkie wartości do drzewa
            drzewo.dodaj(x)                                     # dodajemy dane do drzewa
        h.append(drzewo.wysokosc())                             # zapisanie wysokości
        l.append(drzewo.liscie())                               # zapisanie liczby liści
        d.append(drzewo.srednia_glebokosc())                    # zapisanie średniej głębokości


    # Zapis wyników do pliku tekstowego
    with open("wyniki_bst.txt", "w") as f:                      # tworzy .txt w trybie zapisu "write"
        for i in range(len(h)):                                 # iteruje po wszystkich zebranych wynikach
            f.write(f"Próba {i+1}: Wysokość = {h[i]}, Liście = {l[i]}, Średnia głębokość = {round(d[i], 3)}\n")
            # zapisuje jedna linie z wynikami; wysokość, liście, średnia gł.


    print("\nKorelacje:")
    print("wysokosc vs liscie:", round(korelacja(h, l), 3))         # korelacja między wysokością a liczbą liści
    print("wysokosc vs glebokosc:", round(korelacja(h, d), 3))      # korelacja między wysokością a głebokościa
    print("liscie vs glebokosc:", round(korelacja(l, d), 3))        # korelacja między liści a głębokością

    print("\nOdchylenie standardowe wysokosci:", round(std(h), 3))  # odchylenie st. wysokości drzewa
    print("Rozstęp międzykwartylowy wysokości:", iqr(h))            # rozstęp międzykwartylowy wysokości

    
# Tworzenie i zapisywanie wykresów histogramów
def zapisz_wykresy(heights, leaves, depths):  # Funkcja przyjmuje 3 listy z wynikami

    # Wysokość drzewa
    plt.figure()  # Tworzy nową figurę (okno wykresu)
    plt.hist(heights, bins=20, color='skyblue', edgecolor='black')  # Rysuje histogram z 20 przedziałami
    plt.title("Histogram wysokości drzewa")  # Tytuł wykresu
    plt.xlabel("Wysokość")  # Opis osi X
    plt.ylabel("Liczba przypadków")  # Opis osi Y
    plt.show()  # Wyświetlenie wykresu

    # Liczba liści
    plt.figure()
    plt.hist(leaves, bins=20, color='lightgreen', edgecolor='black')
    plt.title("Histogram liczby liści")
    plt.xlabel("Liście")
    plt.ylabel("Liczba przypadków")
    plt.show()

    # Średnia głębokość
    plt.figure()
    plt.hist(depths, bins=20, color='salmon', edgecolor='black')
    plt.title("Histogram średniej głębokości")
    plt.xlabel("Średnia głębokość")
    plt.ylabel("Liczba przypadków")
    plt.show()


# Wywołanie funkcji zapisującej wykresy
zapisz_wykresy(h, l, d)

        