from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
     required=True, help='required parameter')
    parser.add_argument('store_name', type=str,
    required=True, help='Every item needs a store')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item_json =item.json()
            item_json['store'] = item.store.name
            print(item_json['store'])
            return item_json
        return {'message': f"{name} does not exists"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':f'{name} already exists'}
        data = Item.parser.parse_args()
        store = StoreModel.find_by_name(data['store_name'])
        if store:
            item = ItemModel(name, data['price'], store.sqstore)
            item.save_to_db()
            return item.json(), 201
        else:
            return {'message':'store not found'}, 404

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'{name} deleted from db'}
        return {'message': f'{name} does not exists'}

    @jwt_required()
    def put(self, name):
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()
        if item:
            item.price = data['price']
            store = StoreModel.find_by_name(data['store_name'])
            if store:
                item.sqstore = store.sqstore
            else:
                return {'message':'store note found'}, 404
        else:
            store = StoreModel.find_by_name(data['store_name'])
            if store:
                item = ItemModel(name, data['price'], store.sqstore)
            else:
                return {'message':'store note found'}, 404
        try:
            item.save_to_db()
        except:
            return {'an error has ocurred'}, 500
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'item':[item.json() for item in ItemModel.query.all()]}
