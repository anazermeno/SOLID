# Ana Lizbeth Zermeño Torres  A00824913
# SOLID
# October 2022
import requests
import re
import csv
from bs4 import BeautifulSoup

# Movie class to create movie type objects
# Single Responsability Principle - by creating a class that only handle movie objects
class Movie:  

    #Object definition
    def __init__(self, title, year, place, star_cast, rating, vote, link, preference_key):
        self.title = title
        self.year = year
        self.place = place
        self.star_cast = star_cast
        self.rating = rating
        self.vote = vote
        self.link = link
        self.preference_key = preference_key

    #Method to create dictionary element
    def createDictionary(self):
        data = {"movie_title": self.title,
                "year": self.year,
                "place": self.place,
                "star_cast": self.star_cast,
                "rating": self.rating,
                "vote": self.vote,
                "link": self.link,
                "preference_key": self.preference_key % 4 + 1}
        return data

#Dependency Inversion Principle - System functionality is partitioned into components
#Function that recolects data from source
def getMovieData():

    # Downloading imdb top 250 movie's data
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    movies = soup.select('td.titleColumn')
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

    getMovieDetails(movies, crew, ratings, votes, links)

#Open Closed Principle - to separate tasks in different functions
#Function that adds Movie objects into list prior to creating the CSV file
def getMovieDetails(movies, crew, ratings, votes, links):
    # create a empty list for storing
    # movie information
    list = []

    # Iterating over movies to extract
    # each movie's details
    for index in range(0, len(movies)):
        # Separating movie into: 'place',
        # 'title', 'year'
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index)) + 1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index)) - (len(movie))]

        #Craete Movie object
        movieData = Movie(movie_title, year, place, crew[index], ratings[index], votes[index], links[index], index % 4 + 1)

        #Create dictionary element using createDictionary method and append to list
        list.append(movieData.createDictionary())
    
    #Once list is complete call function to create CSV
    createCSV(list)

#Function that creates CSV file
def createCSV(list):
    fields = ["preference_key", "movie_title", "star_cast", "rating", "year", "place", "vote", "link"]
    with open("movie_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for movie in list:
            writer.writerow({**movie})

def main():
    getMovieData()


if __name__ == '__main__':
    main()
