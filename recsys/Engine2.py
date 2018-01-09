import graphlab as gl

ratings = gl.SFrame.read_csv('../data/ratings_0.txt', delimiter=' ', header=False)
items = gl.SFrame.read_csv('../data/poi_data_0.txt', delimiter=';', header=False)

## Rename columns
ratings = ratings.rename({'X1': 'item_id', 'X2': 'user_id', 'X3': 'score', 'X4': 'timestamp'})
items = items.rename({'X1': 'item_id', 'X2': 'name', 'X3': 'type'})

# print(ratings)
# print(items)
# print(items.show())
## How many unique users do we have?
# print(ratings['user_id'].unique().size())

explicit = ratings[['item_id', 'user_id', 'score']]
# print(explicit)

implicit = explicit[explicit['score'] >= 4.0][['item_id', 'user_id']]
# print (implicit)
m = gl.recommender.create(implicit, 'user_id', 'item_id')

## Getting similar items Elevador Lacerda
# print (items[items['item_id'] == 'ChIJbwjQpe8EFgcReGfBceMwWXI'])
# print (m.get_similar_items(['ChIJbwjQpe8EFgcReGfBceMwWXI'], k=5))
# print (m.get_similar_items(['ChIJbwjQpe8EFgcReGfBceMwWXI']).join(items, on={'similar': 'item_id'}).sort('rank'))

## Build a model for predicting predicted score
m2 = gl.recommender.create(explicit, 'user_id', 'item_id', target='score')

## Making batch recommendations
recs = m.recommend()
# print(recs)
# print(ratings[ratings['user_id'] == '109061523463683935873'].join(items, on='item_id'))
# print(m.recommend(users=['109061523463683935873'], k=20).join(items, on='item_id').sort('rank'))

## Recommendations for new users
recent_data = gl.SFrame()
recent_data['item_id'] = ['ChIJbwjQpe8EFgcReGfBceMwWXI'] # Elevador Lacerda
recent_data['user_id'] = 99999
# print(m.recommend(users=[99999], new_observation_data=recent_data).join(items, on='item_id').sort('rank'))

## Split the data into a training set and a test set
## This allows us to evaluate generalization ability.
# train, valid = gl.recommender.util.random_split_by_user(implicit)

# Train models
# Collaborative filtering approach that uses the Jaccard similarity of two users' item lists
# m0 = gl.item_similarity_recommender.create(train)
#
# # Collaborative filtering approach that learns latent factors for each user and each item
# m1 = gl.ranking_factorization_recommender.create(train, max_iterations=10)
#
# # Collaborative filtering approach that learns latent factors for users, items, and side data
# m2 = gl.ranking_factorization_recommender.create(train, item_data=items[['item_id', 'name']], max_iterations=10)
# m3 = gl.ranking_factorization_recommender.create(train, item_data=items[['item_id', 'name', 'type']], max_iterations=10)
#
# # Evaluation
# # Create a precision/recall plot to compare the recommendation quality of the above models given our heldout data.
# model_comparison = gl.compare(valid, [m0, m1, m2, m3], user_sample=.3)
# gl.show_comparison(model_comparison, [m0, m1, m2, m3])