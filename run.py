import redis

from bson.objectid import ObjectId
from eve.io.mongo import mongo
from eve import Eve

r = redis.StrictRedis(host='redis', port=6379, db=0)

app = Eve(settings='settings.py', redis=r)
mongo = app.data.driver

# добавляем тэг (только уникальный) 
@app.route('/document/<string:tag>/<regex("[a-f0-9]{24}"):document_id>', methods=['POST'])
def add_tag(tag, document_id):   
    f = {'_id': ObjectId(document_id)}
    mongo.db.document.update_one(f, {'$addToSet':{"tags": tag}})
    return f'I add tag to document {document_id}'

# добавляем комментарий
@app.route('/comment/<string:comment>/<regex("[a-f0-9]{24}"):document_id>', methods=['POST'])
def add_comment(comment, document_id):
    print(comment)
    print(f'app route document comment {document_id}')
    f = {'_id': ObjectId(document_id)}
    mongo.db.document.update_one(f, {'$push':{"comments": comment}})
    return f'I have add comment to document {document_id}'

# кэшируем создание поста
def for_cache(response):
    r.set(str(response[0]['_id']), ';'.join(str(atr) for atr in response))

def calc_counts_items(response): 
        # считаем количество тэгов
    try:
        count_tag = len(response['tags'])
        response['count_tag'] = count_tag
    except KeyError:
        pass
    # считаем количество комментариев
    try:
        count_comments = len(response['comments'])
        response['count_comments'] = count_comments
    except KeyError:
        pass

#  кэшируем        
app.on_inserted_document += for_cache

app.on_fetched_document += for_cache

# перехват отрисовки ответа
app.on_fetched_item_document += calc_counts_items

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)