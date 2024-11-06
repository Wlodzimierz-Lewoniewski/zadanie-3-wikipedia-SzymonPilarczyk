import urllib.request
import urllib.parse
import re


# Funkcja do pobierania zawartości strony z kategorii
def pobierz_zawartosc_kategorii(kategoria):
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + kategoria.replace(' ', '_')
    fp = urllib.request.urlopen(url)
    tbytes = fp.read()
    txt = tbytes.decode("utf-8")
    fp.close()
    return txt


# Funkcja do zbierania linków wewnętrznych z artykułów
def pobierz_linki_wewnetrzne_z_artykulu(tresc_artykulu, maks=5):
    linki_wewn = []
    for link in re.findall('<a href="/wiki/([^"]+)"', tresc_artykulu):
        if ":" in link: continue  # Pomija linki do kategorii i innych specjalnych stron
        linki_wewn.append(urllib.parse.unquote(link).replace(' ', '_'))
        if len(linki_wewn) >= maks:  # Maksymalna liczba linków
            break
    return linki_wewn


# Funkcja do pobierania artykułu na podstawie linku
def pobierz_artykul(link):
    url_artykulu = "https://pl.wikipedia.org/wiki/" + link
    fp = urllib.request.urlopen(url_artykulu)
    tbytes = fp.read()
    txt = tbytes.decode("utf-8")
    fp.close()
    return txt


# Główna funkcja - pobieranie artykułów z kategorii i wyciąganie linków
def main():
    kat = "Miasta na prawach powiatu"  # Przykładowa kategoria
    txt = pobierz_zawartosc_kategorii(kat)

    # Wyciąganie linków do artykułów z kategorii
    wzor = r'<li>.*?<a href="/wiki/([^"]+)"[^>]*>([^<]+)</a>.*?</li>'
    wynik = re.findall(wzor, txt)

    # Zbieramy tylko 2 pierwsze artykuły z kategorii
    artykuly = wynik[:2]

    for link_art, tytul_art in artykuly:
        print(f"Przetwarzam artykuł: {tytul_art}")

        # Pobieramy zawartość artykułu
        tresc_artykulu = pobierz_artykul(link_art)

        # Wyciąganie linków wewnętrznych
        linki_wewn = pobierz_linki_wewnetrzne_z_artykulu(tresc_artykulu)
        print("Linki wewnętrzne:", linki_wewn)


if __name__ == '__main__':
    main()
