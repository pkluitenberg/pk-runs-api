from pymongo import MongoClient, cursor
from src.constants import MONGO_URL, MONGO_DB_NAME, MONGO_ACTIVITIES_COLLECTION


class Database:
    url = MONGO_URL

    def __init__(self):
        self._database = MongoClient(Database.url)[MONGO_DB_NAME]

    def find_one(self, collection: str, query: dict) -> any:
        return self._database[collection].find_one(query)

    def insert_one(self, collection: str, data: any) -> str:
        return self._database[collection].insert_one(data).inserted_id

    def delete_one(self, collection: str, query: dict) -> dict:
        return self._database[collection].delete_one(query)

    def find_all(self, collection: str, fields_to_include: list = []) -> cursor.Cursor:
        projection = {'_id': 0}
        projection.update({field: 1 for field in fields_to_include})
        return self._database[collection].find({}, projection=projection)

    def insert_activity(self, activity_id: int, data: dict) -> str:
        if bool(self.find_one(
                collection=MONGO_ACTIVITIES_COLLECTION,
                query={'id': activity_id})):
            print(f'Activity {activity_id} already exists!')
        else:
            doc_id = self.insert_one(collection=MONGO_ACTIVITIES_COLLECTION,
                                     data=data)
            print(f'Inserted activity {activity_id} to document {doc_id}')
            return doc_id

    def delete_activity(self, activity_id: int) -> bool:
        result = self.delete_one(collection=MONGO_ACTIVITIES_COLLECTION,
                                 query={'id': activity_id})
        if bool(result.get('deleted_count')):
            print(f'Successfully deleted activity {activity_id}')
            return True
        else:
            print(
                f'Could not delete activity {activity_id}. Check if activity exists.')
            return False

    def find_all_activities(self, fields_to_include: list = []) -> list:
        return list(self.find_all(collection=MONGO_ACTIVITIES_COLLECTION,
                                  fields_to_include=fields_to_include))
