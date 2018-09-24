#!/bin/python3
from recommender import recommender
r = recommender({},k=10)
r.loadmovieDB()

print(r.recommend(100))

