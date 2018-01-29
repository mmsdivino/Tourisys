import graphlab as gl
from routes.Route import *

class RecSys:
    def __init__(self, user_data='', item_data='', rating_data=''):
        if user_data:
            self._users = gl.SFrame.read_json(user_data, orient='records')
            self._users = self._users.unique()
        if item_data:
            self._items = gl.SFrame.read_json(item_data, orient='records')
            self._items = self._items.unique()
        if rating_data:
            self._ratings = gl.SFrame.read_json(rating_data, orient='records')
            self._ratings = self._ratings.unique()
            # Normalize ratings
            maxValue = max(self._ratings['rating'])
            range = 1.0/maxValue;
            self._ratings['rating'] = self._ratings['rating'].apply(lambda x: x * range)
            self._train, self._test = gl.recommender.util.random_split_by_user(self._ratings)

    def usersSize(self):
        return self._users.size()

    def itemsSize(self):
        return self._items.size()

    def ratingsSize(self):
        return self._ratings.size()

    def itemSimilarity(self, similarityType='jaccard', newUsers=None, newObservationData=None, eval=False, similarItem=None):
        print(self._ratings.dtype())
        isr = gl.item_similarity_recommender.create(self._ratings, target='rating', similarity_type=similarityType)
        recs = isr.recommend(users=newUsers, new_observation_data=newObservationData).join(self._items, on='item_id').sort('rank')
        print(recs)

        if eval:
            isrTrain = gl.item_similarity_recommender.create(self._train, target='rating', similarity_type=similarityType)
            evalPrecisionRecall = isrTrain.evaluate_precision_recall(self._test)
            evalRMSE = isrTrain.evaluate_rmse(self._test, target='rating')
            eval = isrTrain.evaluate(self._test)
            print(eval)

        if similarItem:
            similarity = isr.get_similar_items(similarItem).join(self._items, on={'similar': 'item_id'}).sort('rank')
            print(similarity)

        if newUsers and newObservationData:
            route = Route(recs['latitude'], recs['longitude'])
            route.map()

    def itemContent(self, attributes='', splitAttribute='', newUsers=None, newObservationData=None, eval=False, similarItem=None):
        newItems = self._items.copy()
        if attributes:
            newItems = self._items[attributes]
        if splitAttribute:
            newItems = self._splitAttribute(newItems, splitAttribute)
        icr = gl.item_content_recommender.create(newItems, 'item_id', self._ratings, 'user_id', target='rating')
        recs = icr.recommend(users=newUsers, new_observation_data=newObservationData).join(self._items, on='item_id').sort('rank')
        print(recs)

        if similarItem:
            similarity = icr.get_similar_items(similarItem).join(self._items, on={'similar': 'item_id'}).sort('rank')
            print(similarity)

        if eval:
            icrTrain = gl.item_content_recommender.create(newItems, 'item_id', self._train, 'user_id', target='rating')
            evalPrecisionRecall = icrTrain.evaluate_precision_recall(self._test)
            evalRMSE = icrTrain.evaluate_rmse(self._test, target='rating')
            eval = icrTrain.evaluate(self._test)
            print(eval)

        if newUsers and newObservationData:
            route = Route(recs['latitude'], recs['longitude'])
            route.map()

    def _splitAttribute(self, items, attribute):
        removeItems = []
        for item in items:
            if len(item[attribute]) > 1:
                for value in item[attribute]:
                    i = item.copy()
                    i[attribute] = [value]
                    i.update({k:[v] for k, v in i.items()})
                    items = items.append(gl.SFrame(i))
                removeItems.append(item[attribute])
        items = items.filter_by(removeItems, attribute, exclude=True)
        del removeItems
        return items

## Getting similar items Elevador Lacerda
# print (items[items['item_id'] == 59224731])
# print (m.get_similar_items([59224731], k=5))
# print (m.get_similar_items([59224731]).join(items, on={'similar': 'item_id'}).sort('rank'))