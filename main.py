import urllib.request
import re
import urllib.parse

def pobierz_zawartosc_strony(url):
    """Pobiera zawartość strony podanej w URL i dekoduje do formatu tekstowego."""
    with urllib.request.urlopen(url) as fp:
        zawartosc = fp.read().decode("utf-8")
    return zawartosc

def znajdz_elementy(wzor, tekst, limit=2):
    """Znajduje elementy pasujące do wzorca, zwraca ograniczoną liczbę wyników."""
    elementy = re.findall(wzor, tekst)
    return elementy[:limit]

def pobierz_linki_wewnetrzne(html, limit=5):
    """Pobiera linki wewnętrzne z tekstu HTML, pomija linki zawierające dwukropek."""
    linki_wewn = []
    for link in re.findall(r'<a href="/wiki/([^":]+)"', html):
        linki_wewn.append(urllib.parse.unquote(link).replace(' ', '_'))
        if len(linki_wewn) >= limit:
            break
    return linki_wewn

def main():
    # Wybór kategorii i formatowanie URL
    kat = "Miasta na prawach powiatu"
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + kat.replace(' ', '_')
    
    # Pobieranie zawartości strony kategorii
    tekst_html = pobierz_zawartosc_strony(url)
    
    # Szukanie artykułów z listy w kategorii
    wzor_artykul = r'<li>.*?</li>'
    artykuly = znajdz_elementy(wzor_artykul, tekst_html)
    
    if artykuly:
        # Pobranie pierwszego artykułu do dalszej analizy
        artykul_html = artykuly[0]
        print("Artykuł HTML:", artykul_html)
        
        # Podzielenie zawartości, by znaleźć treść
        sekcja_html = tekst_html.split('class="mw-body-content"')
        
        if len(sekcja_html) > 1:
            tresc_artykulu = sekcja_html[1]
            
            # Pobranie linków wewnętrznych z treści artykułu
            linki_wewnetrzne = pobierz_linki_wewnetrzne(tresc_artykulu)
            print("Linki wewnętrzne:", linki_wewnetrzne)

if __name__ == "__main__":
    main()
