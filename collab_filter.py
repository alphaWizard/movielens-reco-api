#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script demonstrates how to design the simplest recommender system based of
Collaborative Filtering. In order to make these predictions, we must first measure
similarity of users(in this case here) or items from the rows and columns of the Utility Matrix.
using the Pearson Correlation Similarity(PCS) Measure to find similar users.

"""

import numpy as np
import math
from sklearn.metrics import mean_squared_error


# User class stores the names and average rating for each user

class User:

    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id
        self.avg_r = 0.


# Item class stores the name of each item

class Item:

    def __init__(self, name, item_id):
        self.name = name
        self.id = item_id


# Rating class is used to assign ratings

class Rating:

    def __init__(
        self,
        user_id,
        item_id,
        rating,
        ):
        self.user_id = user_id
        self.item_id = item_id
        self.rating = rating


# We store users in a list. Note that user IDs start indexed at 1.

user = []
user.append(User('Ann', 1))
user.append(User('Bob', 2))
user.append(User('Carl', 3))
user.append(User('Doug', 4))

# Items are also stored in a list. Note that item IDs start indexed at 1.

item = []
item.append(Item('HP1', 1))
item.append(Item('HP2', 2))
item.append(Item('HP3', 3))
item.append(Item('SW1', 4))
item.append(Item('SW2', 5))
item.append(Item('SW3', 6))

rating = []
rating.append(Rating(1, 1, 4))
rating.append(Rating(1, 4, 1))
rating.append(Rating(2, 1, 5))
rating.append(Rating(2, 2, 5))
rating.append(Rating(2, 3, 4))
rating.append(Rating(3, 4, 4))
rating.append(Rating(3, 5, 5))
rating.append(Rating(4, 2, 3))
rating.append(Rating(4, 6, 3))

n_users = len(user)
n_items = len(item)
n_ratings = len(rating)

# The utility matrix stores the rating for each user-item pair in the matrix form.

utility = np.zeros((n_users, n_items))
for r in rating:
    utility[r.user_id - 1][r.item_id - 1] = r.rating


# Finds the Pearson Correlation Similarity Measure between two users

def pcs(x, y):
    num = 0.
    ct = 0
    (den_a , den_b) = (0., 0.)
    for i in range(n_items):
        if utility[x-1][i] != 0.0 and utility[y-1][i] != 0.0 :
            num += (utility[x-1][i]-user[x-1].avg_r) * (utility[y-1][i]-user[y-1].avg_r)
            den_a += (utility[x-1][i]-user[x-1].avg_r) * (utility[x-1][i]-user[x-1].avg_r)
            den_b += (utility[y-1][i]-user[y-1].avg_r) * (utility[y-1][i]-user[y-1].avg_r)
            ct += 1
    den = math.sqrt(den_a) * math.sqrt(den_b)       
    if den == 0.:
        return 0.
    return float(num) / float(den)



def number_map_to_sorted_list(map_dict,top_n):
    sorted_list = [v[0] for v in sorted(map_dict.iteritems(), key=lambda (k, v): (-v, k))]
    return sorted_list[:top_n]



# Guesses the ratings that user with id, user_id, might give to item with id, i_id.
# We will consider the top_n similar users to do this. Use top_n as 3 in this example.

def guess(user_id, i_id, top_n):
    dict = {}
    for i in range(n_users):
        if i+1 != user_id:
            dict[i+1] = pcs(user_id,i+1)

    top_n_list = number_map_to_sorted_list(dict,top_n)
    # print top_n_list
    sum_diff = 0.
    count = 0.
    for uid in top_n_list:
        if utility[uid-1][i_id-1] != 0.0:
            sum_diff += utility[uid-1][i_id-1] - user[uid-1].avg_r
            count += 1
    # print count 
    # print sum_diff
    if count == 0:
        return user[user_id-1].avg_r     
    return user[user_id-1].avg_r + float(sum_diff/count)       


# Display the utility matrix as given in Part 1 of your project description

np.set_printoptions(precision=3)
print utility

# Finds the average rating for each user and stores it in the user's object

for i in range(n_users):
    rated = np.nonzero(utility[i])
    n = len(rated[0])
    if n != 0:
        user[i].avg_r = np.mean(utility[i][rated])
    else:
        user[i].avg_r = 0.


n = 3  # Assume top_n users


# print guess(1,2,n)
# Finds all the missing values of the utility matrix

utility_copy = np.copy(utility)
for i in range(n_users):
    for j in range(n_items):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i + 1, j + 1, n)

print utility_copy

# Finds the utility values of the particular users in the test set. Refer to Q2

print "Ann's rating for SW2 should be " + str(guess(1, 5, n))
print "Carl's rating for HP1 should be " + str(guess(3, 1, n))
print "Carl's rating for HP2 should be " + str(guess(3, 2, n))
print "Doug's rating for SW1 should be " + str(guess(4, 4, n))
print "Doug's rating for SW2 should be " + str(guess(4, 5, n))

guesses = np.array([guess(1, 5, n), guess(3, 1, n), guess(3, 2, n),
                   guess(4, 4, n), guess(4, 5, n)])

### Actual Ratings from the test set
# Ann rates SW2 with 2 stars
# Carl rates HP1 with 2 stars
# Carl rates HP2 with 2 stars
# Doug rates SW1 with 4 stars
# Doug rates SW2 with 3 stars

test = np.array([2, 2, 2, 4, 3])

# Finds the mean squared error of the ratings with respect to the test set

print 'Mean Squared Error is ' + str(mean_squared_error(guesses, test))















