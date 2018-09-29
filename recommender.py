#!/bin/python3
import codecs 
import re
from math import sqrt

class recommender:

    def __init__(self, data, k=1, metric='pearson', n=5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized
        to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        # for some reason I want to save the name of the metric
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        #
        # if data is dictionary set recommender data to it
        #
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        """Given product id number return product name"""
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id


    def userRatings(self, id, n):
        """Return n top ratings for user with id"""
        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print("user have rated {} movies".format(len(ratings)))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v)
                   for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda artistTuple: artistTuple[1],
                     reverse = True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))
        

        

    def loadmovieDB(self, path=''):
        """loads the movielens dataset. Path is where the BX files are
        located"""
        self.data = {}
        i = 0
        #
        # First load movie ratings into self.data
        #
        f = open("data/u.base", "r", encoding = "ISO-8859-1")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('\t', 4)
            if len(e) == 4:
                i += 1
                userid = int(e[0])
                movieid = int(e[1])
                rating = int(e[2])
                if userid in self.data:
                  currentRatings = self.data[userid]
                else:
                  currentRatings = {}
                currentRatings[movieid] = rating
                self.data[userid] = currentRatings
        f.close()
        print("no. of ratings in database: "+str(i))

        i=0

        #
        # Now load movies into self.productid2name
        # Movies contains isbn, title, and author among other fields
        #
        f = open("data/u.item", "r", encoding = "ISO-8859-1")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 24)
            if len(e) == 24:
                i += 1
                movieid = int(e[0])
                movie_title = e[1]
                self.productid2name[movieid] = movie_title
        f.close()
        print("no. of movies in database: "+str(i))
        i = 0
        #
        #  Now load user info into both self.userid2name and
        #  self.username2id
        #
        f = open("data/u.user", "r", encoding = "ISO-8859-1")
        text = f.read()
        entries = re.split("\n+", text)
        i = 0
        for entry in entries:
            e = entry.split('|', 5)
            if len(e) == 5:
                i += 1
                userid = int(e[0])
                age = int(e[1])
                sex = e[2]
                occupation = e[3]
                value = "id: "+str(userid)+" age: "+str(age)+" sex: "+str(sex)+" occupation: "+str(occupation)
                self.userid2name[userid] = value
                self.username2id[value] = userid
        print("no. of users in database: "+str(i))


                
        
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator


    def computeNearestNeighbor(self, username):
        """creates a sorted list of users based on their distance to
        username"""
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],
                                   self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances

    def recommend(self, user,metric='pearson',k=10, n=5):

       self.k = k
       self.n = n
       self.metric = metric
       if self.metric == 'pearson':
          self.fn = self.pearson
       """Give list of recommendations"""
       recommendations = {}
       # first get list of users  ordered by nearness
       nearest = self.computeNearestNeighbor(user)
       #
       # now get the ratings for the user
       #
       userRatings = self.data[user]
       #
       # determine the total distance
       totalDistance = 0.0
       for i in range(self.k):
          totalDistance += nearest[i][1]
       # now iterate through the k nearest neighbors
       # accumulating their ratings
       for i in range(self.k):
          # compute slice of pie 
          weight = nearest[i][1] / totalDistance
          # get the name of the person
          name = nearest[i][0]
          # get the ratings for this person
          neighborRatings = self.data[name]
          # get the name of the person
          # now find bands neighbor rated that user didn't
          for artist in neighborRatings:
             if not artist in userRatings:
                if artist not in recommendations:
                   recommendations[artist] = (neighborRatings[artist]
                                              * weight)
                else:
                   recommendations[artist] = (recommendations[artist]
                                              + neighborRatings[artist]
                                              * weight)
       # now make list from dictionary
       recommendations = list(recommendations.items())
       recommendations = [(self.convertProductID2name(k), v)
                          for (k, v) in recommendations]
       # finally sort and return
       recommendations.sort(key=lambda artistTuple: artistTuple[1],
                            reverse = True)
       # Return the first n items
       return recommendations[:self.n]
