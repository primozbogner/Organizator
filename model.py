# import json
#  
# class Uporabnik:
#     def __init__(self, uporabnisko_ime, geslo, podatki):
#         self.uporabnisko_ime = uporabnisko_ime
#         self.geslo = geslo
#         self.podatki = podatki
#         
#     def shrani_stanje(self, podatki):
#         pass
# 
#     def nalozi_stanje(self, ime_datoteke):
#         pass

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
#     "1":
#         {
#             "ime": "Vroče poletje",
#             "vrsta": "črni čaj",
#             "temperatura": "100°C"
#             "cas": "3 min"
#             "rok uporabe": "06/21",
#             "opombe": "Zmanjkuje!"
#         }
# }

    def dodaj_caj(self, ime, vrsta, temperatura, cas, rok, opombe):
        '''Doda nov čaj v slovar podatkov'''
        self.podatki[self.nov_indeks()] = {
            "ime": ime,
            "vrsta": vrsta,
            "temperatura": temperatura,
            "čas": cas,
            "rok uporabe": rok,
            "opombe": opombe
        }

    def uredi_caj(self, indeks, ime, vrsta, temperatura, cas, rok, opombe):
        '''Uredi že obstoječi čaj v slovarju podatkov'''
        self.podatki[indeks]["ime"] = ime
        self.podatki[indeks]["vrsta"] = vrsta
        self.podatki[indeks]["temperatura"] = temperatura
        self.podatki[indeks]["cas"] = cas
        self.podatki[indeks]["opombe"]= opombe

    def uredi_po_imenu(self, podatki):
        pass

    def uredi_po_vrsti(self, podatki):
        pass

    def isci_po_imenu(self, podatki):
        pass

    def isci_po_vrsti(self, podatki):
        pass

    def odstrani_caj(self, podatki):
        pass