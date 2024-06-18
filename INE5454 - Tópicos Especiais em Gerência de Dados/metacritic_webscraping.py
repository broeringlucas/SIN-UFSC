from bs4 import BeautifulSoup
import requests
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}

def metacritic_scraper(pages): 

    page_count = 1 
    movie_count = 1
    response = []

    while page_count < pages:

        url = f'https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2024&page={page_count}'

        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')

        movies = soup.find_all("div", class_="c-finderProductCard_info u-flexbox-column")

        for movie in movies: 
            title = movie.find("h3", class_="c-finderProductCard_titleHeading").get_text(strip=True)
            
            launch_year_span = movie.find("span", class_="u-text-uppercase")
            launch_year = launch_year_span.get_text(strip=True) if launch_year_span else "N/A"
            
            rated_span = movie.find("span", class_="u-text-capitalize")
            rated = rated_span.parent.get_text(strip=True) if rated_span else "N/A"

            description_div = movie.find("div", class_="c-finderProductCard_description")
            description = description_div.get_text(strip=True) if description_div else "N/A"
            
            score_div = movie.find("div", class_="c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall")
            score = score_div.get_text(strip=True) if score_div else "N/A"
            score_formatted = score + "/100"

            data = {'ID': str(movie_count), 'TITLE': title[2:], 'LAUNCH YEAR': launch_year, 'RATED': rated[5:], 'DESCRIPTION': description, 'SCORE': score_formatted, 'URL': url}
            
            response.append(data)

            movie_count += 1

        page_count += 1

    print(f'Scraping complete - {movie_count}')

    return response

def json_file(response):
    with open('INE5454 - Tópicos Especiais em Gerência de Dados/metacritic_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

def main(): 
    pages = int(input("Enter the number of pages you want to scrape (each page has 24 movies): "))
    response = metacritic_scraper(pages)
    json_file(response)

main()