from pymongo import MongoClient



client = MongoClient("mongodb://localhost:27017/")
user_db = client["user-database"]
user_collection = user_db["user-collection"]

def set_categories(categories : list[str]):
    """
        Inputs new categories for user and updates the user database.

        Param:
            -categories: list of categories

        Returns:
            -success: boolean value indicating where the database was updated or not
    """
