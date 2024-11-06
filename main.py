import re
import urllib.request
import urllib.parse

# Wzorce wyrażeń regularnych
wzorzec_odn_artykul = r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>'
wzorzec_odn_kategoria = r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'
wzorzec_odn_obrazek = r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>'
wzorzec_odn_zewnetrzny = r'<a[^>]*class=\"external[^"]*\"[^>]*href=\"([^"]+)\"[^>]*>'
wzorzec_odn_wewn = r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'

# Funkcja do znajdowania wzorców w HTML
def znajdz_wzorce(wzorzec, tekst, maks=5):
    return re.findall(wzorzec, tekst)[:maks]

# Zamiana spacji na "_"
def generuj_url_kat(kategoria_nazwa):
    return f'https://pl.wikipedia.org/wiki/Kategoria:{kategoria_nazwa.replace(" ", "_")}'

# Główna część programu
kat = input().strip()  # Wprowadź nazwę kategorii
url = generuj_url_kat(kat)

# Pobieranie artykułów z kategorii
with urllib.request.urlopen(url) as fp:
    html = fp.read().decode("utf-8")

artykuly = znajdz_wzorce(wzorzec_odn_artykul, html, maks=3)  # Pobieramy 3 artykuły

# Przetwarzanie każdego artykułu
for link_art, tytul_art in artykuly:
    # Pobieranie zawartości artykułu
    with urllib.request.urlopen("https://pl.wikipedia.org" + link_art) as fp:
        tresc = fp.read().decode("utf-8")

    # Linki wewnętrzne
    linki_wewn = znajdz_wzorce(wzorzec_odn_wewn, tresc, maks=5)
    print("Linki wewnętrzne:")
    print(' | '.join([link[1] for link in linki_wewn]))

    # Obrazki
    obrazki = znajdz_wzorce(wzorzec_odn_obrazek, tresc, maks=3)
    print("Obrazki:")
    print(' | '.join([obrazek[0] for obrazek in obrazki]))

    # Linki zewnętrzne (przypisy)
    with urllib.request.urlopen("https://pl.wikipedia.org" + link_art) as fp:
        przypisy_html = fp.read().decode("utf-8")
    zewnetrzne_linki = znajdz_wzorce(wzorzec_odn_zewnetrzny, przypisy_html, maks=3)
    print("Linki zewnętrzne:")
    print(' | '.join([link for link in zewnetrzne_linki]))

    # Kategorie
    with urllib.request.urlopen("https://pl.wikipedia.org" + link_art) as fp:
        kategorie_html = fp.read().decode("utf-8")
    kategorie = znajdz_wzorce(wzorzec_odn_kategoria, kategorie_html, maks=3)
    print("Kategorie:")
    print(' | '.join([kategoria[1].removeprefix('Kategoria:') for kategoria in kategorie]))

    print("-" * 50)  # Separator między artykułami
