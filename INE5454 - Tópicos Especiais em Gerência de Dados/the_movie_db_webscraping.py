from bs4 import BeautifulSoup
import requests
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}

def the_movie_db_scraper(movies): 

    count = 1
    response = []
    movie_count = 0

    while movie_count < movies:

        url = f'https://www.themoviedb.org/movie/{count}'

        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')

        movie = soup.find("section", class_="header poster")

        if movie is None:
            count += 1
        else: 
            movie_main_info = movie.find("div", class_="title")

            title = movie_main_info.find("a").get_text(strip=True)
            certification = movie_main_info.find("span", class_="certification").get_text(strip=True) if movie_main_info.find("span", class_="certification") else "N/A"
            release = movie_main_info.find("span", class_="release").get_text(strip=True) if movie_main_info.find("span", class_="release") else "N/A"
            genres = movie_main_info.find("span", class_="genres").get_text(strip=True) if movie_main_info.find("span", class_="genres") else "N/A"
            runtime = movie_main_info.find("span", class_="runtime").get_text(strip=True) if movie_main_info.find("span", class_="runtime") else "N/A"

            movie_extra_info = movie.find("div", class_="header_info")

            description = movie_extra_info.find("p").get_text(strip=True) if movie_extra_info.find("p") else "N/A"
            director = movie_extra_info.find("li", class_="profile").get_text(strip=True) if movie_extra_info.find("li", class_="profile") else "N/A"

            count += 1
            movie_count += 1

            data = {'ID': str(movie_count), 'TITLE': title, 'CERTIFICATION': certification, 'RELEASE': release, 'GENRES': genres, 'RUNTIME': runtime, 'DESCRIPTION': description, 'DIRECTOR': director, 'URL': url}

            response.append(data)

    print(f'Scraping complete - {movie_count}')

    return response

def json_file(response):
    with open('INE5454 - Tópicos Especiais em Gerência de Dados/the_movie_db_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

def main(): 
    movies = int(input("Enter the number of movies you want to scrape: "))
    response = the_movie_db_scraper(movies)
    json_file(response)

main()

