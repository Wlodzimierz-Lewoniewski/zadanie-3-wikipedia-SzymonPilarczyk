import urllib.request
import re
import urllib.parse


# Funkcja do pobierania HTML strony
def pobierz_html(url):
    fp = urllib.request.urlopen(url)
    tbytes = fp.read()
    html = tbytes.decode("utf-8")
    fp.close()
    return html


# Funkcja do wyciągania linków wewnętrznych
def wyciagnij_linki_wewnetrzne(html):
    linki_wewn = []
    for link, tekst in re.findall(r'<a href="/wiki/([^":]+)"[^>]*>([^<]+)</a>', html):
        linki_wewn.append((urllib.parse.unquote(link), tekst))
        if len(linki_wewn) >= 5:
            break
    return linki_wewn


# Funkcja do wyciągania URLi obrazków
def wyciagnij_obrazki(html):
    obrazki = re.findall(r'//upload\.wikimedia\.org[^"]+\.(jpg|png|svg)', html)
    return obrazki[:3]


# Funkcja do wyciągania zewnętrznych linków źródłowych
def wyciagnij_zewnetrzne_linki(html):
    zewnetrzne_linki = re.findall(r'<a href="(https?://[^"]+)"', html)
    return zewnetrzne_linki[:3]


# Funkcja do wyciągania kategorii
def wyciagnij_kategorie(html):
    kategorie = re.findall(r'<a href="/wiki/Kategoria:([^"]+)"', html)
    return kategorie[:3]


# Główna funkcja programu
def main():
    # Użytkownik podaje nazwę kategorii
    kat = "Miasta na prawach powiatu"
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + kat.replace(' ', '_')

    # Pobranie i przetworzenie HTML strony kategorii
    html_kategorii = pobierz_html(url)
    artykuly = re.findall(r'<li><a href="/wiki/([^"]+)" title="[^"]+">[^<]+</a>', html_kategorii)

    # Pobranie pierwszych dwóch artykułów z listy
    pierwsze_dwa_artykuly = artykuly[:2]

    for art in pierwsze_dwa_artykuly:
        art_url = "https://pl.wikipedia.org/wiki/" + art
        html_artykulu = pobierz_html(art_url)

        # Wyciąganie elementów z artykułu
        linki_wewnetrzne = wyciagnij_linki_wewnetrzne(html_artykulu)
        obrazki = wyciagnij_obrazki(html_artykulu)
        zewnetrzne_linki = wyciagnij_zewnetrzne_linki(html_artykulu)
        kategorie = wyciagnij_kategorie(html_artykulu)

        # Wyświetlanie wyników
        print(f"Artykuł: {art}")
        print("Linki wewnętrzne (nazwa i URL):")
        for link, tekst in linki_wewnetrzne:
            print(f"{tekst} | https://pl.wikipedia.org/wiki/{link}")

        print("\nObrazki:")
        for obrazek in obrazki:
            print(f"https:{obrazek}")

        print("\nZewnętrzne linki:")
        for zew_link in zewnetrzne_linki:
            print(zew_link)

        print("\nKategorie:")
        for kat in kategorie:
            print(kat)

        print("\n" + "=" * 40 + "\n")


# Uruchomienie programu
main()
