import pandas as pd
import graphlab

graphlab.product_key.set_product_key("BE53-A84E-1046-F087-83D6-1C3F-A908-323D")

# Reading ratings file
r_cols = ['item_id', 'user_id', 'rating', 'timestamp']

ratings_base = pd.read_csv('../data/ratings_3.txt', sep = ' ', names = r_cols, encoding='latin-1')
ratings_test = pd.read_csv('../data/test_0.txt', sep = ' ', names = r_cols, encoding='latin-1')

train_data = graphlab.SFrame(ratings_base)
test_data = graphlab.SFrame(ratings_test)

popularity_model = graphlab.popularity_recommender.create(train_data, user_id = 'user_id', item_id = 'item_id', target = 'rating')

#Get recommendations for first 5 users and print them
#users = range(1,6) specifies user ID of first 5 users
#k=5 specifies top 5 recommendations to be given
popularity_recomm = popularity_model.recommend(users=range(1,6),k=5)
popularity_recomm.print_rows(num_rows=20)

ratings_base.groupby(by='item_id')['rating'].mean().sort_values(ascending=False).head(20)

#Train Model
# item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id', target='rating', similarity_type='pearson')
item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id', target='rating', similarity_type='jaccard')

#Make Recommendations:
item_sim_recomm = item_sim_model.recommend(users=range(1,6),k=5)
item_sim_recomm.print_rows()

model_performance = graphlab.compare(test_data, [popularity_model, item_sim_model])
graphlab.show_comparison(model_performance,[popularity_model, item_sim_model])