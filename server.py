#!/usr/bin/python3
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from json import dumps

from movielens import *

app = Flask(__name__)
api = Api(app)

from recommender import recommender
r = recommender({},k=10)
r.loadmovieDB()

user = []
item = []
d = Dataset()
d.load_users("data/u.user", user)
d.load_items("data/u.item", item)
# print(item[0])


class Users(Resource):
    def get(self):
        return jsonify({'users': [i for i in range(1,1683)]})

class UsersDetail(Resource):
    def get(self,user_id):
        result = user[int(user_id)-1]
        result_dict = {'id':result.id, 'age':result.age, 'sex':result.sex, 'occupation':result.occupation}    #avg_r to be added  
        return jsonify(result_dict) 
    
class Movies(Resource):
    def get(self):
        result = {'movies': [i for i in range(1,944)]}
        return jsonify(result)

class MoviesDetail(Resource):
    def get(self, movie_id):
        result = item[int(movie_id)-1]
        result_dict = {'id':result.id, 'title':result.title, 'release_date':result.release_date, 'video_release_date':result.video_release_date, 'imdb_url':result.imdb_url, 'unknown':result.unknown, 'is_action':result.action, 'is_adventure':result.adventure, 'is_animation':result.animation, 'is_childrens':result.childrens, 'is_comedy':result.comedy, 'is_crime':result.crime, 'is_documentary':result.documentary, 'is_drama':result.drama, 'is_fantasy':result.fantasy, 'is_film_noir':result.film_noir, 'is_horror':result.horror,'is_musical':result.musical, 'is_mystery':result.mystery, 'is_romance':result.romance, 'is_sci_fi':result.sci_fi, 'is_thriller':result.thriller, 'is_war':result.war, 'is_western':result.western }
        return jsonify(result_dict)

class Query(Resource):
    def get(self, user_id):
        result = r.recommend(int(user_id))
        return jsonify(result)


api.add_resource(Users, '/users') # Route_1
api.add_resource(UsersDetail, '/users/<user_id>') # Route_2
api.add_resource(Movies, '/movies') # Route_3
api.add_resource(MoviesDetail, '/movies/<movie_id>') # Route_4
api.add_resource(Query, '/query/<user_id>') # Route_5


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(debug = True)
