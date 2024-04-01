import math
path ="car.txt"

# Klasa węzła drzewa decyzyjnego
class Wezel:
    def __init__(self):
        # Domyślnie węzeł jest 'pusty' żęby porpawnie stworzyć korzeń drzewa
        self.index = None
        self.value = None
        self.decision = None
        self.counter = 0
        self.next = []

    def __str__(self):
        # Wykorzystuje wbudowaną funkcje __str__ żeby nie printować w funkcji tree, next to kolejne węzły, pierwszy jest pusty
        next = ""
        for i in self.next:
            next += "\n" + "    " * self.counter
            next += f"{i}"
        if self.index is not None:
            node = f" Atrybut{self.index + 1}:"
        else:
            node = f"Decyzja: {self.decision}"
        if self.value is not None:
            value =f" Wartość atrybutu: {self.value} ->" 
        else:
            value = f" Pierwszy podział ->"

        return f"─ Węzeł {self.counter}:{value}{node}{next}"

def lista_list(path:str) -> list: 
    data = []
    with open(path, 'r') as plik:
        data_raw = plik.readlines()
    # Stworzenie listy z każdego wiersza w pliku txt
    for i in data_raw:
        row = i.replace("\n", "").split(',')
        data.append(row)
    return data


# Funkcja tworząca listę list, w której każda przedstawia wartości dla wybranej cechy
def transpose_list(lista:list) -> list:
    num_rows = len(lista)
    num_cols = len(lista[0])

    transposed_list = []
    for i in range(num_cols):
        new_row = []
        for j in range(num_rows):
            new_row.append(lista[j][i])
        transposed_list.append(new_row)

    return transposed_list

#Funkcja licząca entropię 
def entropia(kolumna) -> float:
    #lista prawdopodobieństwa wystąpienia wartości cechy
    I = []
    entropia = 0
    for element in set(kolumna):
        I.append(kolumna.count(element)/len(kolumna))
    for i in I:
        entropia += i* math.log2(i)
    return entropia*(-1)

def get_distinct_values_for_column(data):
    columns = transpose_list(data)
    distinct_values = []
    for column in  columns[:-1]:
        distinct_values.append(list(set(column)))
    return distinct_values

#Funkcja licząca funkcje informacji dla zestawu danych
def f_info(kolumna, decyzja):
    f_info_v = 0
    licznik = len(decyzja)
    wartosci = set(kolumna)
    for wartosc in wartosci:
        indeksy = []
        for i in range(len(kolumna)):
            if wartosc == kolumna[i]:
                indeksy.append(i)
        decyzja_new = [decyzja[i] for i in indeksy]
        f_info_v += (kolumna.count(wartosc)/licznik)*entropia(decyzja_new)
    return f_info_v

def f_info_list(kolumny, decyzja):
    f_info_list =[]
    for kolumna in kolumny[:-1]:
        info =f_info(kolumna, decyzja)
        f_info_list.append(info)
    return f_info_list


def gain_list(kolumny, decyzja):
    gains = []
    entropia_all = entropia(decyzja)
    for kolumna in kolumny[:-1]:
        gain = entropia_all - f_info(kolumna, decyzja)
        gains.append(gain)
    return gains

def split_info_list(kolumny):
    s_info_list = []
    for kolumna in kolumny[:-1]:
        s_info = entropia(kolumna)
        s_info_list.append(s_info)
    return s_info_list

def gain_ratio_list(split_infos, gains):
    gain_ratios = []
    for i in range(len(split_infos)):
        if split_infos[i] != 0: 
            gain_ratio = gains[i]/split_infos[i]
        else:
            gain_ratio = 0
        gain_ratios.append(gain_ratio)
    return gain_ratios

def best_attribute(gain_ratios):
    return gain_ratios.index(max(gain_ratios))


def all_values(data: list) -> dict:

    # Kolumny
    columns = transpose_list(data)

    # Decyzja
    decision = columns[-1]

    # Entropia
    entropy = entropia(columns[-1])

    # Unikatowe wartości dla każdej kolumny
    attributes = get_distinct_values_for_column(data)

    # Funkcja informacji dla każdej kolumny
    attrs_entropy = f_info_list(columns,decision)

    # Przyrost informacji dla każdej kolumny
    gains = gain_list(columns, decision)

    # Split info dla każdej kolumny
    splitinfos = split_info_list(columns)

    # Zrównoważony przyrost informacji dla każdej kolumny
    gainratios = gain_ratio_list(splitinfos, gains)

    # Index kolumny o najlepszy zrównoważonym przyroście informacji
    best_index = best_attribute(gainratios)

    # Sprawdzenie czy koniec drzewa
    if_zero_gain = gainratios[best_index] == 0

    # Słownik końcowych wartości
    return {
        "attributes": attributes,
        "entropy": entropy,
        "attrs_entropy": attrs_entropy,
        "gains": gains,
        "splitinfos": splitinfos,
        "gainratios": gainratios,
        "best_index": best_index,
        "if_zero_gain": if_zero_gain,
    }





'''Notatki'''
'''Entropia wg wzoru w pdf.- pierwsza entropia w pdf tylko dla decyzji a nie dla atrybutów'''
'''Funkcja informacji X - atrybut dla którego liczymy funkcję informacji czyli dla a1,a2,a3 bez decyzyjnego
   Trzeba obliczyć dla każdej wartości ze słownika result_list ile razy jest up ile razy jest down
   dla a1 bęzie to: 3/10 * I(3/3, 0/3) + 4/10 * I(2/4,2/4) + 3/10 *( 0/3, 3/3)'''
'''Przyrost informacji dla a1 Gain(a1) = Entropia całego wzoru - Funkcja informacji dla a1  IM WIĘCEJ TYM LEPIEJ'''
'''
dane = lista_list(path)
kolumny = transpose_list(dane)
decyzja = kolumny[-1]
gain_a1 = entropia_all - f_info_a1
gain_a2 = entropia_all - f_info_a2
gain_a3 = entropia_all - f_info_a3
gain_a4 = entropia_all - f_info_a4
split_info_a1 = entropia(kolumny[0])
split_info_a2 = entropia(kolumny[1])
split_info_a3 = entropia(kolumny[2])
split_info_a4 = entropia(kolumny[3])
f_info_a1 = f_info(kolumny[0], decyzja)
f_info_a2 = f_info(kolumny[1], decyzja)
f_info_a3 = f_info(kolumny[2], decyzja)
f_info_a4 = f_info(kolumny[3], decyzja)
print(f'entropia klasy decyzyjnej: {entropia_all}')
print(f'funkcje informacji: {f_info_a1, f_info_a2, f_info_a3, f_info_a4}')
print(f'przyrost informacji dla kolejnych atrybutów warunkowych: {gain_a1, gain_a2, gain_a3, gain_a4}')
print(f'split info:{split_info_a1, split_info_a2, split_info_a3, split_info_a4} ')
print(f'zrównoważony przyrost informacji dla kolejnych atrybutów warunkowych: {gain_a1/split_info_a1, gain_a2/split_info_a2, gain_a3/split_info_a3, gain_a4/split_info_a4}')
entropia_all = entropia(decyzja)
'''


'''Notatki 2'''
'''Gain ratio - zrównoważony przyrost informacji, najwyższa wartość oznacza, że jest najlepszy'''
'''Dokładniejszy niż zwykły gain'''


'''Na przykładzie gielda.txt
Wybieramy atrybut a1 - największy zrównoważony przyrost infromacji
Drzewo dzieli się na tabele według wartośći atrybutu a1
Jeżeli wszystkie decyzje w węźle są takie same to koniec poziomu drzewa
Jeżeli decyzje są różne to wybieramy z tabeli atrybut, który ma największy zrównoważony przyrost informacji'''

def tree(dane: list, value=None, counter=0):
    #Początkowo tworzy 'pusty' węzeł
    n = Wezel()
    all = all_values(dane)
    best_index = all["best_index"]
    if_zero_gain = all["if_zero_gain"]
    attributes = all["attributes"]
    n.value = value
    n.counter = counter
    if not if_zero_gain:
        # Wybór najlepszego atrybutu
        n.index = best_index
        for value in attributes[best_index]:
            # Wybór obserwacji do budowy kolejnego węzła
            dane_new = [row for row in dane if row[best_index] == value]
            # Rekurencyjne budowanie kolejnych węzłów i zapamiętywanie ich jako potomkowie
            child = tree(dane_new, value, counter + 1)
            n.next.append(child)
    else:
        # Określenie decyzji dla węzła
        n.decision = dane[0][-1]
        
    return n

dane = lista_list(path)
print(tree(dane))
