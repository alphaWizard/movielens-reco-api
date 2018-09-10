#!/bin/python
from movielens import *
import numpy as np
import math
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import sys, time

# Store data in arrays
user = []
item = []
rating = []
rating_test = []

# Load the movie lens dataset into arrays
d = Dataset()
d.load_users("data/u.user", user)
d.load_items("data/u.item", item)
d.load_ratings("data/u.base", rating)
d.load_ratings("data/u.test", rating_test)

n_users = len(user)
n_items = len(item)

print "no. of users : "+str(n_users)
print "no. of items : "+str(n_items)

# The utility matrix stores the rating for each user-item pair in the matrix form.
# Note that the movielens data is indexed starting from 1 (instead of 0).
utility = np.zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating

# Finds the average rating for each user and stores it in the user's object
for i in range(n_users):
    rated = np.nonzero(utility[i])
    n = len(rated[0])
    if n != 0:
        user[i].avg_r = np.mean(utility[i][rated])
    else:
        user[i].avg_r = 0.

# print utility

# Finds the Pearson Correlation Similarity Measure between two users
def pcs(x, y,utility):
    num = 0.
    ct = 0
    (den_a , den_b) = (0., 0.)
    for i in range(n_clusters_item):
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
# We will consider the top_n similar users to do this.
def guess(user_id, i_id, top_n,utility):
    dict = {}
    for i in range(n_users):
        if i+1 != user_id:
            dict[i+1] = pcs(user_id,i+1,utility)

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
    guessed_result = user[user_id-1].avg_r + float(sum_diff/count)
    if guessed_result < 1.0:
        return 1.0
    if guessed_result > 5.0:
        return 5.0
    return guessed_result

# to check for predictions using collaborative filtering
# guesses = []
# actual_rating = []
# for ratings_tests in rating_test:
#     guessed = guess(ratings_tests.user_id,ratings_tests.item_id,150)
#     print "user-id : "+str(ratings_tests.user_id)+ " item-id : "+str(ratings_tests.item_id) +  " expected-rating : "+str(ratings_tests.rating) +  " guessed-rating : "+str(guessed)
#     guesses.append(guessed)
#     actual_rating.append(ratings_tests.rating)

#print 'Mean Squared Error using collaborative-filtering is ' + str(mean_squared_error(guesses, actual_rating))
## THINGS THAT YOU WILL NEED TO DO:
# Perform clustering on users and items
# Predict the ratings of the user-item pairs in rating_test
# Find mean-squared error




X= []
for items in item:
    features = [items.unknown, items.action, items.adventure, items.animation, items.childrens, items.comedy, items.crime, items.documentary, items.drama, items.fantasy, items.film_noir, items.horror, items.musical, items.mystery, items.romance, items.sci_fi, items.thriller, items.war, items.western]
    X.append(features)
# X = np.array(X)    
kmeans = KMeans(n_clusters=400).fit(X)
clustered_label = kmeans.labels_
n_clusters_item = 400
print clustered_label[0:30]



utility_item_clustered = np.zeros((n_users, n_clusters_item))
for user_id in range(n_users):
    label_dict_sum = {}
    label_dict_count = {}
    for cluster_id in range(n_clusters_item):
        label_dict_count[cluster_id] = 0
        label_dict_sum[cluster_id] = 0.0
    for item_id in range(n_items):
        if utility[user_id][item_id] != 0.0:
            label_dict_sum[clustered_label[item_id]] += utility[user_id][item_id]
            label_dict_count[clustered_label[item_id]] += 1
    for cluster_id in range(n_clusters_item):
        if label_dict_count[cluster_id] != 0:
            utility_item_clustered[user_id][cluster_id] = float(label_dict_sum[cluster_id]/label_dict_count[cluster_id])
print utility_item_clustered[0] 




# kmeans_user = KMeans(n_clusters=300).fit(utility_item_clustered) #clustering users
# clustered_label_user = kmeans_user.labels_
# n_clusters_user = 300
# print clustered_label_user[0:20]

# print len(clustered_label_user)

# utility_user_clustered = np.zeros((n_clusters_user, n_clusters_item))
# for i in range(n_clusters_item):
#     label_sum = {}   #sum for each label of users
#     label_count = {}
#     for j in range(n_clusters_user):
#         label_sum[j] = 0.0
#         label_count[j] = 0
#     for k in range(n_users):
#         if utility_item_clustered[k][i] != 0.0:
#             label_sum[clustered_label_user[k]] += utility_item_clustered[k][i]
#             label_count[clustered_label_user[k]] += 1
#     for v in range(n_clusters_user):
#         if label_count[v] != 0:
#             utility_user_clustered[v][i] = float(label_sum[v] / label_count[v])  


# print len(utility_user_clustered)


# Find the average rating(of clusters) for each user and stores it in the user's object
for i in range(0, n_users):
    x = utility_item_clustered[i]
    user[i].avg_r = sum(a for a in x if a > 0) / sum(a > 0 for a in x)  


utility_copy = np.copy(utility_item_clustered)   # to fill the empty values in the clustered utility2 matrix
for i in range(0, n_users):
    for j in range(0, n_clusters_item):
        if utility_copy[i][j] == 0:
            sys.stdout.write("\rGuessing [User:Rating] = [%d:%d]" % (i, j))
            sys.stdout.flush()
            time.sleep(0.00005)
            utility_copy[i][j] = guess(i+1, j+1, 155,utility_item_clustered)
print "\rGuessing [User:Rating] = [%d:%d]" % (i, j)

print utility_copy

test = np.zeros((n_users, n_items))
for r in rating_test:
    test[r.user_id - 1][r.item_id - 1] = r.rating

# Predict ratings for u.test and find the mean squared error
y_true = []
y_pred = []
f = open('test_prediction.txt', 'w')
for i in range(0, n_users):
    for j in range(0, n_items):
        if test[i][j] > 0:
            f.write("%d, %d, %.5f\n" % (i+1, j+1, utility_copy[i][clustered_label[j]]))
            y_true.append(test[i][j])
            y_pred.append(utility_copy[i][clustered_label[j]])
f.close()

print "Mean Squared Error using clustering: %f" % mean_squared_error(y_true, y_pred)    