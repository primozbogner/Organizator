import json
 
class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo, podatki):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.podatki = podatki
        
    def shrani_stanje(self, ime_datoteke):
        slovar = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'geslo': self.geslo,
            'podatki': self.podatki.podatki
        }
        with open(ime_datoteke, 'w') as dat:
            json.dump(slovar, dat, ensure_ascii=False)

    def nalozi_stanje(self, ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
        uporabnisko_ime = slovar['uporabnisko_ime']
        geslo = slovar['geslo']
        podatki = Caj(slovar['podatki'])
        return Uporabnik(uporabnisko_ime, geslo, podatki)

class Caj:
    def __init__(self, podatki=None):
        self.podatki = {} if podatki is None else podatki

    def nov_indeks(self):
        '''Določi nov indeks za dodajanje čaja, če je slovar podatkov prazen določi indeks 1, v nasprotnem primeru poišče največji obstoječi indeks in ga poveča za 1'''
        if self.podatki == {}:
            return 1
        else:
            return map(max, int(self.podatki.keys())) + 1

# podatki so oblikovani kot slovar slovarjev, kjer so ključi indeksi, vrednosti pa podatki zapisani v obliki slovarja:
# {
#     '1':
#         {
#             'ime': 'Vroče poletje',
#             'vrsta': 'črni čaj',
#             'temperatura': '100°C'
#             'cas': '3 min'
#             'rok uporabe': '06/21',
#             'opombe': 'Zmanjkuje!'
#         }
# }

    def dodaj_caj(self, ime, vrsta, temperatura, cas, rok, opombe):
        '''Doda nov čaj v slovar podatkov'''
        self.podatki[self.nov_indeks()] = {
            'ime': ime,
            'vrsta': vrsta,
            'temperatura': temperatura,
            'čas': cas,
            'rok uporabe': rok,
            'opombe': opombe
        }

    def uredi_caj(self, indeks, ime, vrsta, temperatura, cas, rok, opombe):
        '''Uredi že obstoječi čaj v slovarju podatkov'''
        self.podatki[indeks]['ime'] = ime
        self.podatki[indeks]['vrsta'] = vrsta
        self.podatki[indeks]['temperatura'] = temperatura
        self.podatki[indeks]['cas'] = cas
        self.podatki[indeks]['opombe']= opombe

    def uredi_po_imenu(self):
        '''Čaje uredi po abecednem vrstnem redu in jih oštevilči z indeksi od 1 do n.'''
        seznam = []
        urejeni_podatki = {}
        for i in self.podatki:
            seznam.append((self.podatki[i]['ime'], i))
        seznam.sort(key=lambda x: x[0])
        for i, (_, indeks) in range(len(seznam)), seznam:
            urejeni_podatki[str(i + 1)] = self.podatki[indeks]
            self.podatki.pop(indeks)
        self.podatki = urejeni_podatki

    def uredi_po_vrsti(self):
        '''Čaje uredi po abecednem vrstnem redu, najprej po vrsti, nato pa še po imenu in jih oštevilči z indeksi od 1 do n'''
        seznam = []
        urejeni_podatki = {}
        for i in self.podatki:
            seznam.append((self.podatki[i]['vrsta'], self.podatki[i]['ime'], i))
        seznam.sort(key=lambda x: (x[0], x[1]))
        for i, (_, _, indeks) in range(len(seznam)), seznam:
            urejeni_podatki[str(i + 1)] = self.podatki[indeks]
            self.podatki.pop(indeks)
        self.podatki = urejeni_podatki

    def isci_caj(self, podatki):
        pass

    def odstrani_caj(self, indeks):
        self.podatki.pop(indeks)