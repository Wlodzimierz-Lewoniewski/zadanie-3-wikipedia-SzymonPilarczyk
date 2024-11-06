import re, requests
import itertools

# Wzorce regex dla różnych elementów artykułu
PATTERN_ARTICLE = r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>'
PATTERN_CATEGORY = r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'
PATTERN_IMAGE = r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>'
PATTERN_EXTERNAL_LINK = r'<a[^>]*class=\"external[^"]*\"[^>]*href=\"([^"]+)\"[^>]*>'
PATTERN_INTERNAL_LINK = r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'


# Funkcja wyszukująca wzorce
def find_patterns(pattern, text, limit=5, flag=0):
    return [match.groups() for match in itertools.islice(re.finditer(pattern, text, flags=flag), limit)]


# Pobiera listę artykułów z kategorii, konstruując URL kategorii
def fetch_articles_from_category(category_name, limit=3):
    category_url = 'https://pl.wikipedia.org/wiki/Kategoria:' + category_name.replace(' ', '_')
    html_content = requests.get(category_url).text
    return find_patterns(PATTERN_ARTICLE, html_content, limit)


# Wyświetla listę elementów jako wynik
def display_results(elements):
    print(" | ".join(elements) if elements else "")


# Funkcja główna, która pobiera i wyświetla dane z artykułów
def main():
    category = input("Podaj kategorię: ").strip()
    articles = fetch_articles_from_category(category)

    for link, title in articles:
        article_html = requests.get("https://pl.wikipedia.org" + link).text
        main_content = article_html[
                       article_html.find('<div id="mw-content-text"'):article_html.find('<div id="catlinks"')]

        # Zbiera linki wewnętrzne
        internal_links = find_patterns(PATTERN_INTERNAL_LINK, main_content, 5)
        display_results([name for _, name in internal_links])

        # Zbiera obrazki
        images = find_patterns(PATTERN_IMAGE, main_content, 3)
        display_results([url for url, in images])

        # Zbiera linki zewnętrzne z sekcji przypisów
        references_section = article_html[article_html.find('id="Przypisy"'):]
        references_section = references_section[:references_section.find('<div class="mw-heading')]
        external_links = find_patterns(PATTERN_EXTERNAL_LINK, references_section, 3)
        display_results([url for url, in external_links])

        # Kategorie
        category_section = article_html[article_html.find('<div id="catlinks"'):]
        categories = find_patterns(PATTERN_CATEGORY, category_section, 3)
        display_results([category_name for _, category_name in categories])


if __name__ == '__main__':
    main()
