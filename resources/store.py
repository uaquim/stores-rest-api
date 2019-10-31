from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt import jwt_required

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category', type=str,
     required=True, help='required parameter')

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': f'Store {name} does not exists'}, 404

    @jwt_required()
    def post(self, name):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(name):
            return {'message': f'{name} already exists'}
        store = StoreModel(name, **data)
        try:
            store.save_to_db()
        except:
            return {'message':'an error has ocurred'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            if len(store.items.all()) > 0:
                return {'message': 'There are items in store'}
            store.delete_from_db()
            return {'message': 'Store deleted!'}
        else:
            return {'message': 'Store not found'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}
