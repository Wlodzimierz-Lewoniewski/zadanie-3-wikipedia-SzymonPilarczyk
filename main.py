import re, requests, itertools

# Wzorce regex dla różnych elementów artykułu
PAT_ART = r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>'
PAT_KAT = r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'
PAT_IMG = r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>'
PAT_EXT_LINK = r'<a[^>]*class=\"external[^"]*\"[^>]*href=\"([^"]+)\"[^>]*>'
PAT_WW_LINK = r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'

# Funkcja wyszukująca wzorce
def szukaj(wzor, tekst, limit=5, f=0): return [m.groups() for m in itertools.islice(re.finditer(wzor, tekst, flags=f), limit)]

# Pobiera listę artykułów z kategorii, konstruując URL kategorii
def pobierz_art_z_kat(nazwa, lim=3):
    url = 'https://pl.wikipedia.org/wiki/Kategoria:' + nazwa.replace(' ', '_')
    html = requests.get(url).text
    return szukaj(PAT_ART, html, lim)

# Wyświetla listę elementów jako wynik
def wynik(lista): print(" | ".join(lista) if lista else "")

# Funkcja główna, która pobiera i wyświetla dane z artykułów
def glowna():
    kat = input("Podaj kategorię: ").strip()
    artykuly = pobierz_art_z_kat(kat)
    
    for link, tytul in artykuly:
        html = requests.get("https://pl.wikipedia.org" + link).text
        tresc_html = html[html.find('<div id="mw-content-text"'):html.find('<div id="catlinks"')]
        
        # Zbiera linki wewnętrzne
        wew_linki = szukaj(PAT_WW_LINK, tresc_html, 5)
        wynik([nazwa for _, nazwa in wew_linki])

        # Zbiera obrazki
        obrazki = szukaj(PAT_IMG, tresc_html, 3)
        wynik([url for url, in obrazki])

        # Zbiera linki zewnętrzne z sekcji przypisów
        przypisy_html = html[html.find('id="Przypisy"'):]
        przypisy_html = przypisy_html[:przypisy_html.find('<div class="mw-heading')]
        zew_linki = szukaj(PAT_EXT_LINK, przypisy_html, 3)
        wynik([url for url, in zew_linki])

        # Kategorie
        kat_html = html[html.find('<div id="catlinks"'):]
        kategorie = szukaj(PAT_KAT, kat_html, 3)
        wynik([kat for _, kat in kategorie])

if __name__ == '__main__': glowna()
