import graphlab as gl
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

categories = ['Casinos', 'Castles', 'Art Galleries', 'Landmarks & Historical Buildings', 'Museums', 'Zoos',
              'Observatories', 'Performing Arts', 'Wineries',
              'Aquariums', 'Beaches', 'Parks', 'Water Parks',
              'Tours']

def containsCategory(categoryItem):
    return (i for i in categoryItem if i in categories)

ratings = gl.SFrame.read_json('../data/dataset/review.json', orient='lines')
items = gl.SFrame.read_json('../data/dataset/business.json', orient='lines')

items = items[['business_id', 'name', 'city', 'state', 'latitude', 'longitude', 'categories']]
items = items[items['categories'].apply(lambda x: containsCategory(x))]
ratings_part = ratings[:430627]
ratings_part = ratings_part[['user_id', 'business_id', 'stars']]
ratings_part = ratings_part[ratings_part['business_id'].apply(lambda x: True if x in items['business_id'] else False)]
# print(filteredItems[filteredItems['state'] == 'AZ'].sort('review_count', ascending=False))

## Getting similar items
# print (items[items['business_id'] == 'amNromvj2O7OAYYrlDEUcQ'])
# print (items[items['business_id'] == '7RTwUpuPFnIHPoTmWJpWhQ'])
# print (m.get_similar_items([59224731], k=5))
# print (m.get_similar_items([59224731]).join(items, on={'similar': 'item_id'}).sort('rank'))

m = gl.recommender.item_content_recommender.create(item_data=items, item_id='business_id', observation_data=ratings_part, user_id='user_id', target='stars')
recs = m.recommend()
print(recs)

recent_data = gl.SFrame()
recent_data['business_id'] = ['amNromvj2O7OAYYrlDEUcQ']
recent_data['user_id'] = 99999
recent_data['stars'] = 4
recs_new_user = m.recommend(users=[99999], new_observation_data=recent_data).join(items, on='business_id').sort('rank')
print(recs_new_user)

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
train, test = gl.recommender.util.random_split_by_user(ratings_part, item_id='business_id', max_num_user=1)
m = gl.recommender.item_content_recommender.create(item_data=items, item_id='business_id', observation_data=train, user_id='user_id', target='stars')
eval_precision_recall = m.evaluate_precision_recall(test)
print(eval_precision_recall)

eval_rmse_test = m.evaluate_rmse(test, target='stars')
print (eval_rmse_test)
eval_rmse_train = m.evaluate_rmse(train, target='stars')
print (eval_rmse_train)

eval= m.evaluate(test)
print (eval)
