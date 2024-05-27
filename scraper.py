from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json

driver = webdriver.Chrome()
req = str(sys.argv[1])
# req = "avengers"
driver.get("https://www.imdb.com/find/?q=" + req + "&ref_=nv_sr_sm")

movies = driver.find_elements(
    By.CLASS_NAME, "ipc-metadata-list-summary-item__t")

top_related_movies = list()
for movie in movies:
    link_to_movie = movie.get_attribute("href")
    movie_name = movie.text
    if "title" in link_to_movie:
        plot_link = link_to_movie[:36] + "/plotsummary/?ref_=tt_stry_pl"

        top_related_movies.append((movie_name, plot_link))

# print(top_related_movies)

movie_short_plots = list()
movie_long_plots = list()

for movie, movie_plot_link in top_related_movies:
    driver.get(movie_plot_link)

    summaries = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list__item")
    movie_short_plots.append((movie, summaries[0].text))
    movie_long_plots.append((movie, summaries[1].text))

print(json.dumps(movie_short_plots))
