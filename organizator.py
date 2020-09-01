import bottle
from model import Caj, Uporabnik, NAPACNO_GESLO, UPORABNIK_ZE_OBSTAJA,UPORABNIK_NE_OBSTAJA
import hashlib
import os

uporabniki = {}
SKRIVNOST = ':3'

for ime_datoteke in os.listdir('uporabniki'):
    uporabnik = Uporabnik.nalozi_stanje(os.path.join('uporabniki', ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SKRIVNOST)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
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

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html', napaka=None)

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='utf-8'))
    zasifrirano_geslo = h.hexdigest()
    if uporabnisko_ime not in uporabniki:
        return bottle.template('prijava.html', napaka=UPORABNIK_NE_OBSTAJA)
    uporabnik = uporabniki[uporabnisko_ime]
    if uporabnik.preveri_geslo(zasifrirano_geslo) == NAPACNO_GESLO:
        return bottle.template('prijava.html', napaka=NAPACNO_GESLO)
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=SKRIVNOST)
    bottle.redirect('/')

@bottle.get('/registracija/')
def registracija_get():
    return bottle.template('registracija.html', napaka=None)

@bottle.post('/registracija/')
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    if uporabnisko_ime in uporabniki:
        return bottle.template('registracija.html', napaka=UPORABNIK_ZE_OBSTAJA)
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='utf-8'))
    zasifrirano_geslo = h.hexdigest()
    uporabnik = Uporabnik(
        uporabnisko_ime,
        zasifrirano_geslo,
        Caj()
        )
    uporabniki[uporabnisko_ime] = uporabnik
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=SKRIVNOST)
    bottle.redirect('/')    

@bottle.post('/odjava/')
def odjava():
    shrani_trenutnega_uporabnika()
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.post('/dodaj_caj/')
def dodaj_caj_post():
    ime = bottle.request.forms.getunicode('ime')
    vrsta = bottle.request.forms.getunicode('vrsta')
    temperatura = bottle.request.forms.getunicode('temperatura')
    cas = bottle.request.forms.getunicode('cas')
    rok = bottle.request.forms.getunicode('rok uporabe')
    opombe = bottle.request.forms.getunicode('opombe')
    nakupovalni = bool(bottle.request.forms.getunicode('nakupovalni'))
    podatki_trenutnega_uporabnika().dodaj_caj(ime, vrsta, temperatura, cas, rok, opombe, nakupovalni)
    podatki_trenutnega_uporabnika().uredi_indekse()
    shrani_trenutnega_uporabnika()
    if nakupovalni:
        bottle.redirect('/nakupovalni_seznam/')
    else:
        bottle.redirect('/organizator/')

@bottle.post('/odstrani_caj<indeks>/')
def odstrani_caj(indeks):
    nakupovalni = bool(podatki_trenutnega_uporabnika().podatki[indeks]['nakupovalni'])
    podatki_trenutnega_uporabnika().odstrani_caj(indeks)
    podatki_trenutnega_uporabnika().uredi_indekse()
    shrani_trenutnega_uporabnika()
    if nakupovalni:
        bottle.redirect('/nakupovalni_seznam/')
    bottle.redirect('/')

@bottle.get('/uredi_caj<indeks>/')
def uredi_caj_get(indeks):
    shrani_trenutnega_uporabnika()
    podatki = podatki_trenutnega_uporabnika().podatki
    return bottle.template('uredi_caj.html', podatki=podatki, indeks=indeks)

@bottle.post('/uredi_caj<indeks>/')
def uredi_caj_post(indeks):
    nakup_sez = bool(podatki_trenutnega_uporabnika().podatki[indeks]['nakupovalni'])
    ime = bottle.request.forms.getunicode('ime')
    vrsta = bottle.request.forms.getunicode('vrsta')
    temperatura = bottle.request.forms.getunicode('temperatura')
    cas = bottle.request.forms.getunicode('cas') 
    rok = bottle.request.forms.getunicode('rok uporabe')
    opombe = bottle.request.forms.getunicode('opombe')
    nakupovalni = bool(bottle.request.forms.getunicode('nakupovalni'))
    podatki_trenutnega_uporabnika().uredi_caj(str(indeks), ime, vrsta, temperatura, cas, rok, opombe, nakupovalni)
    shrani_trenutnega_uporabnika()
    if nakup_sez:
        bottle.redirect('/nakupovalni_seznam/')
    bottle.redirect('/organizator/')

@bottle.get('/razvrsti_po_imenu/')
def razvrsti_po_imenu():
    podatki_trenutnega_uporabnika().razvrsti_po_imenu()
    bottle.redirect('/')

@bottle.get('/razvrsti_po_vrsti/')
def razvrsti_po_vrsti():
    podatki_trenutnega_uporabnika().razvrsti_po_vrsti()
    bottle.redirect('/')

@bottle.get('/razvrsti_po_imenu_nakupovalni/')
def razvrsti_po_imenu_nakupovalni():
    podatki_trenutnega_uporabnika().razvrsti_po_imenu()
    bottle.redirect('/nakupovalni_seznam/')

@bottle.get('/razvrsti_po_vrsti_nakupovalni/')
def razvrsti_po_vrsti_nakupovalni():
    podatki_trenutnega_uporabnika().razvrsti_po_vrsti()
    bottle.redirect('/nakupovalni_seznam/')

@bottle.get('/nakupovalni_seznam/')
def nakupovalni_seznam():
    podatki = podatki_trenutnega_uporabnika().podatki
    return bottle.template('nakupovalni_seznam.html', podatki=podatki)

@bottle.get('/iskanje/')
def iskanje_get():
   return bottle.template('iskanje.html', najdeno=None)

@bottle.post('/iskanje/')
def iskanje_post():
    iskani_niz = bottle.request.forms.getunicode('iskani_niz')
    najdeno = podatki_trenutnega_uporabnika().isci_caj(iskani_niz)
    return bottle.template('iskanje.html', najdeno=najdeno)

bottle.run(debug=True, reloader=True)