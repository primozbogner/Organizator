import bottle
from model import Caj, Uporabnik
import hashlib
import os

uporabniki = {}
SKRIVNOST = ':3'

for ime_datoteke in os.listdir('uporabniki'):
    uporabnik = Uporabnik.nalozi_stanje(os.path.join('uporabniki', ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik

def trenutni_uporabnik():
    uporabnisko_ime = 'uporabnik' #bottle.request.get_cookie('uporabnisko_ime', secret=SKRIVNOST)
    return uporabniki[uporabnisko_ime]

def podatki_trenutnega_uporabnika():
    return trenutni_uporabnik().slovar_s_podatki

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_stanje(os.path.join('uporabniki', '{}.json'.format(uporabnik.uporabnisko_ime))) # stanje shrani v json datoteko v mapi 'uporabniki', ime datoteke je uporabniško ime

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/organizator/')

@bottle.get('/organizator/')
def organizator():
    podatki = podatki_trenutnega_uporabnika().podatki
    return bottle.template('organizator.html', podatki=podatki)

@bottle.get('/dodaj_caj/')
def dodaj_caj_get():
    return bottle.template('dodaj_caj.html')

@bottle.post('/dodaj_caj/')
def dodaj_caj_post():
    ime = bottle.request.forms.getunicode('ime')
    vrsta = bottle.request.forms.getunicode('vrsta')
    temperatura = bottle.request.forms.getunicode('temperatura')
    cas = bottle.request.forms.getunicode('cas')
    rok = bottle.request.forms.getunicode('rok uporabe')
    opombe = bottle.request.forms.getunicode('opombe')
    podatki_trenutnega_uporabnika().dodaj_caj(ime, vrsta, temperatura, cas, rok, opombe)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/organizator/')

#@bottle.get('/prijava/')
#def prijava_get():
#    return bottle.template('prijava.html')
#
# @bottle.post('/prijava/')
# def prijava_post():
#     uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
#     if uporabnisko_ime not in uporabniki:
#         raise ValueError('Uporabniško ime ne obstaja')
#         bottle.redirect('/registracija/')
#     geslo = bottle.request.forms.getunicode('geslo')
#     uporabnik.preveri_geslo
#     h = hashlib.blake2b()
#     h.update(geslo.encode(encoding='utf-8'))
#     zasifrirano_geslo = h.hexdigest()
#     uporabnik.preveri_geslo(zasifrirano_geslo)
#     
# @bottle.post('/registracija/')
# def registracija_post():
#     pass


bottle.run(debug=True, reloader=True)