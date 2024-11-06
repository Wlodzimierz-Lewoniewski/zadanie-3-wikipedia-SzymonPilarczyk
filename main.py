import re, requests
import itertools

# Pobieranie zawartości artykułu
def pobierz_zawartosc(html):
    return html[html.find('<div id="mw-content-text"'):html.find('<div id="catlinks"')]

# Pobieranie przypisów
def pobierz_przypisy_html(html):
    html = html[html.find('id="Przypisy"'):]
    html = html[:html.find('<div class="mw-heading')]
    return html

# Pobieranie kategorii
def pobierz_kategorie_html(html):
    return html[html.find('<div id="catlinks"'):]

# Znajdowanie dopasowań wyrażeń regularnych
def znajdz_wzorce(wzorzec, tekst, flaga=0, maks=5):
    return [dopasowanie.groups() for dopasowanie in itertools.islice(re.finditer(wzorzec, tekst, flags=flaga), maks)]

# Generowanie URL kategorii
def generuj_url_kategorii(nazwa_kategorii):
    nazwa_dopasowana = nazwa_kategorii.replace(' ', '_')
    return f'https://pl.wikipedia.org/wiki/Kategoria:{nazwa_dopasowana}'

# Pobieranie listy artykułów z kategorii
def pobierz_artykuly_z_kategorii(nazwa_kategorii, maks=3):
    url_kategorii = generuj_url_kategorii(nazwa_kategorii)
    odp = requests.get(url_kategorii)
    html = odp.text
    artykuly = znajdz_wzorce(WZORZEC_ARTYKUL, html, maks=maks)
    return artykuly

# Pobranie zawartości artykułu
def pobierz_zawartosc_artykulu(link):
    odp = requests.get("https://pl.wikipedia.org" + link)
    html = odp.text
    return html

# Pobieranie obrazków z artykułu
def pobierz_obrazki(artykul, maks=3):
    html = pobierz_zawartosc(artykul)
    obrazki = znajdz_wzorce(WZORZEC_OBRAZEK, html, maks=maks)
    return obrazki

# Pobieranie linków wewnętrznych
def pobierz_linki_wewnetrzne(artykul, maks=5):
    html = pobierz_zawartosc(artykul)
    linki_wewn = znajdz_wzorce(WZORZEC_LINK_WEWN, html, maks=maks)
    return linki_wewn

# Pobieranie linków zewnętrznych
def pobierz_linki_zewnetrzne(artykul, maks=3):
    html = pobierz_przypisy_html(artykul)
    linki_zewn = znajdz_wzorce(WZORZEC_LINK_ZEW, html, maks=maks)
    return linki_zewn

# Pobieranie kategorii dla artykułu
def pobierz_kategorie(artykul, maks=3):
    html = pobierz_kategorie_html(artykul)
    kategorie = znajdz_wzorce(WZORZEC_KATEGORIA, html, maks=maks)
    return kategorie

# Wyświetlanie wyników
def wyswietl_wynik(lista_elementow):
    wynik = ' | '.join(lista_elementow).strip()
    print(wynik)

# Wzorce wyrażeń regularnych
WZORZEC_ARTYKUL = r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>'
WZORZEC_KATEGORIA = r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'
WZORZEC_OBRAZEK = r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>'
WZORZEC_LINK_ZEW = r'<a[^>]*class=\"external[^"]*\"[^>]*href=\"([^"]+)\"[^>]*>'
WZORZEC_LINK_WEWN = r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'

# Główna funkcja
def main():
    kat = input("Podaj kategorię: ").strip()
    artykuly = pobierz_artykuly_z_kategorii(kat)

    for link_art, tytul_art in artykuly:
        tresc = pobierz_zawartosc_artykulu(link_art)

        # Pobieranie i wyświetlanie wyników
        linki_wewn = pobierz_linki_wewnetrzne(tresc)
        wyswietl_wynik([elem[1] for elem in linki_wewn])
        obrazki = pobierz_obrazki(tresc)
        wyswietl_wynik([elem[0] for elem in obrazki])
        linki_zewn = pobierz_linki_zewnetrzne(tresc)
        wyswietl_wynik([elem[0] for elem in linki_zewn])
        kategorie = pobierz_kategorie(tresc)
        wyswietl_wynik([elem[1].removeprefix('Kategoria:') for elem in kategorie])

if __name__ == '__main__':
    main()
