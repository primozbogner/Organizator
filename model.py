import json

NAPACNO_GESLO = 'Geslo je napačno!'
UPORABNIK_ZE_OBSTAJA = 'To uporabniško ime že obstaja!'
UPORABNIK_NE_OBSTAJA = 'To uporabniško ime ne obstaja!\nProsim preverite vnos ali se registrirajte'

 
class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, slovar_s_podatki):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.slovar_s_podatki = slovar_s_podatki
        
    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            return       

    def shrani_stanje(self, ime_datoteke):
        slovar_stanja = {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "slovar_s_podatki": self.slovar_s_podatki.podatki
        }
        with open(ime_datoteke, "w", encoding="utf-8") as datoteka:
            json.dump(slovar_stanja, datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke, encoding="utf-8") as dat:
            slovar_stanja = json.load(dat)
        uporabnisko_ime = slovar_stanja["uporabnisko_ime"]
        zasifrirano_geslo = slovar_stanja["zasifrirano_geslo"]
        slovar_s_podatki = Caj(slovar_stanja["slovar_s_podatki"])
        return cls(uporabnisko_ime, zasifrirano_geslo, slovar_s_podatki)

class Caj:
    def __init__(self, podatki=None):
        self.podatki = {} if podatki is None else podatki

    def nov_indeks(self):
        """Določi nov indeks za dodajanje čaja, če je slovar podatkov prazen določi indeks 1, v nasprotnem primeru poišče največji obstoječi indeks in ga poveča za 1"""
        if self.podatki == {}:
            return 1
        else:
            najvecji_indeks = 1
            for indeks in map(int, self.podatki.keys()):
                if indeks > najvecji_indeks:
                    najvecji_indeks = indeks
            najvecji_indeks += 1
            return najvecji_indeks

# podatki so oblikovani kot slovar slovarjev, kjer so ključi indeksi, vrednosti pa podatki zapisani v obliki slovarja:
# {
#     "1":
#         {
#             "ime": "Beli tiger",
#             "vrsta": "beli čaj",
#             "temperatura": 80,
#             "cas": "3-5",
#             "rok uporabe": "02/21",
#             "opombe": "Zmanjkuje!"
#         }
# }

    def dodaj_caj(self, ime, vrsta, temperatura, cas, rok, opombe):
        """Doda nov čaj v slovar podatkov"""
        self.podatki[self.nov_indeks()] = {
            "ime": ime,
            "vrsta": vrsta,
            "temperatura": temperatura,
            "cas": cas,
            "rok uporabe": rok,
            "opombe": opombe
        }

    def uredi_caj(self, indeks, ime, vrsta, temperatura, cas, rok, opombe):
        """Uredi že obstoječi čaj v slovarju podatkov"""
        self.podatki[indeks]["ime"] = ime
        self.podatki[indeks]["vrsta"] = vrsta
        self.podatki[indeks]["temperatura"] = temperatura
        self.podatki[indeks]["cas"] = cas
        self.podatki[indeks]["rok uporabe"] = rok
        self.podatki[indeks]["opombe"]= opombe

    def uredi_po_imenu(self):
        """Čaje uredi po abecednem vrstnem redu in jih oštevilči z indeksi od 1 do n."""
        seznam = []
        urejeni_podatki = {}
        for i in self.podatki:
            seznam.append((self.podatki[i]["ime"], i))
        seznam.sort(key=lambda x: x[0])
        for i, (_, indeks) in range(len(seznam)), seznam:
            urejeni_podatki[str(i + 1)] = self.podatki[indeks]
            self.podatki.pop(indeks)
        self.podatki = urejeni_podatki

    def uredi_po_vrsti(self):
        """Čaje uredi po abecednem vrstnem redu, najprej po vrsti, nato pa še po imenu in jih oštevilči z indeksi od 1 do n"""
        seznam = []
        urejeni_podatki = {}
        for i in self.podatki:
            seznam.append((self.podatki[i]["vrsta"], self.podatki[i]["ime"], i))
        seznam.sort(key=lambda x: (x[0], x[1]))
        for i, (_, _, indeks) in range(len(seznam)), seznam:
            urejeni_podatki[str(i + 1)] = self.podatki[indeks]
            self.podatki.pop(indeks)
        self.podatki = urejeni_podatki

    def isci_caj(self, podatki):
        pass

    def odstrani_caj(self, indeks):
        self.podatki.pop(indeks)