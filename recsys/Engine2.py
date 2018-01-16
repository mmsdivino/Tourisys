import graphlab as gl
from sklearn.metrics import mean_absolute_error
from geopy.distance import vincenty

def calcArea(location, origin, destination):
    # Distance between origin e destination
    dOriginDest = vincenty(origin, destination).meters
    # Distance between origin and location
    dOriginActual = vincenty(origin, location).meters
    # Distance between destination and location
    dDestActual = vincenty(destination, location).meters

    # Calc Area
    ## calculate the semi-perimeter
    s = (dOriginDest + dOriginActual + dDestActual) / 2;

    ## calculate the area
    area = (s * (s - dOriginDest) * (s - dOriginActual) * (s - dDestActual)) ** 0.5

    return area

ratings = gl.SFrame.read_csv('../data/ratings_0.txt', delimiter=' ', header=False)
items = gl.SFrame.read_csv('../data/poi_data_0.txt', delimiter=';', header=False)

## Rename columns
ratings = ratings.rename({'X1': 'item_id', 'X2': 'user_id', 'X3': 'rating', 'X4': 'timestamp'})
items = items.rename({'X1': 'item_id', 'X2': 'name', 'X3': 'type', 'X4': 'location'})

# How many unique users do we have?
# print(ratings['user_id'].unique().size())
# print(ratings['item_id'].unique().size())
# print(items['type'].unique().size())

## Getting similar items Elevador Lacerda
# print (items[items['item_id'] == 59224731])
# print (m.get_similar_items([59224731], k=5))
# print (m.get_similar_items([59224731]).join(items, on={'similar': 'item_id'}).sort('rank'))

## Build a model for predicting predicted score
# m2 = gl.recommender.create(explicit, 'user_id', 'item_id', target='score')

## Making batch recommendations
# recs = m.recommend()
# print(recs)
# print(ratings[ratings['user_id'] == '109061523463683935873'].join(items, on='item_id'))
# print(m.recommend(users=['109061523463683935873'], k=20).join(items, on='item_id').sort('rank'))

# m = gl.recommender.item_content_recommender.create(item_data=items, item_id='item_id', observation_data=ratings, user_id='user_id', target='rating')
# recs = m.recommend()
# print(recs)

## Recommendations for new users

# print(poiRec[poiRec['user_id'] == 99999].join(items, on='item_id').sort('rank'))
# print(poiRec)
#
# recent_data['origin'] = [(-12.9691653, -38.5120631)]
# recent_data['destination'] = [(-12.9731013, -38.5099296)]
#
# itemsArray = []
# distanceArray = []
# for item in poiRec:
#     itemsArray.append(item['item_id'])
#     distanceArray.append(calcArea(item['location'], recent_data['origin'], recent_data['destination']))
#
# itemsSa = gl.SArray(itemsArray)
# distanceSa = gl.SArray(distanceArray)
#
# itemsDistance = gl.SFrame();
# itemsDistance.add_column(itemsSa, name='item_id')
# itemsDistance.add_column(distanceSa, name='distance')
#
# poiRecDist = poiRec.join(itemsDistance, on='item_id').sort('distance')
#
# print(poiRecDist)

## Split the data into a training set and a test set
## This allows us to evaluate generalization ability.
# train, test = gl.recommender.util.random_split_by_user(ratings)
# m = gl.recommender.item_content_recommender.create(item_data=items, item_id='item_id', observation_data=train, user_id='user_id', target='rating')
# eval_precision_recall = m.evaluate_precision_recall(test)
# print(eval_precision_recall)

# eval_rmse_test = m.evaluate_rmse(test, target='rating')
# print (eval_rmse_test)
#
# eval_rmse_train = m.evaluate_rmse(train, target='rating')
# print (eval_rmse_train)

# eval= m.evaluate(test)
# print (eval)

folds = gl.cross_validation.KFold(ratings, 10)
params = dict([('target', 'rating')])
job = gl.cross_validation.cross_val_score(folds, gl.ranking_factorization_recommender.create, params)
print(job)
print(job.get_results())
