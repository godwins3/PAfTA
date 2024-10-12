from db.mongo_conn import create as create_mongo_conn
from tokenz import tokens
import json
from bson import json_util



def get_user_db(user_id):
    # Connect to MongoDB
    client = create_mongo_conn()
    db = client['exodus']
    users_collection = db['users_database']

    # Query for the user
    user = users_collection.find_one({'user_id': user_id})

    # Close the connection
    client.close()

    # Return the db_name if user is found, otherwise return an empty string
    return user['db_name'] if user else ''


def get_user_info(email=None, user_locator=None, user_id=None, client=None):
    original_client = 0
    if client is None:
        client = create_mongo_conn()
        original_client = 1

    try:
        db = client['exodus'] 
        users_collection = db['users']
        personal_info_collection = db['personal_information']

        # Determine the query based on the provided parameter
        query = {}
        if email:
            query['email'] = email
        elif user_locator:
            query['locator'] = user_locator
        elif user_id:
            query['_id'] = user_id
        else:
            return {"Message": "No valid identifier provided", "statusCode": 400}

        # Find the user
        user = users_collection.find_one(query)

        if user:
            user_id = str(user['_id'])
            email = user.get('email', '')
            display_name = user.get('display_name', '')
            phone_number = user.get('phone_number', '')
            user_locator = user.get('locator', '')
            db_name = user.get('db_name', '')

            # Get personal information
            personal_info = personal_info_collection.find_one({'user_id': user_id}, {'_id': 0, 'user_id': 0})
            personal_information = json.loads(json_util.dumps(personal_info)) if personal_info else {}

            return {
                "user_id": user_id,
                "display_name": display_name,
                'db_name': db_name,
                'personalInformation': personal_information,
                "user_locator": user_locator,
                "phone_number": phone_number,
                "email": email
            }
        else:
            return {"Message": "User does not exist", "statusCode": 404}

    except Exception as e:
        print(e)
        return {"Message": "Error retrieving user information", "statusCode": 500}

    finally:
        if original_client == 1:
            client.close()

def get_user_personal_info(header):
    user_id = tokens.get_id(header)

    if not str(user_id).isalnum():
        return {'Message': 'login in again.', "statusCode": 600}

    client = create_mongo_conn()
    personal_information = {"statusCode": 401, "displayName": "", "email": "", "phoneNumber": ""}

    db_name = get_user_db.get(user_id)
    db = client[db_name]
    users_collection = db["users"]
    personal_info_collection = db["personal_information"]

    user_data = users_collection.find_one({"user_id": user_id}, {"_id": 0, "displayName": 1, "email": 1, "phoneNumber": 1, "locator": 1})
    
    if user_data:
        personal_information.update({
            "locator": user_data.get("locator", ""),
            "displayName": user_data.get("displayName", ""),
            "email": user_data.get("email", ""),
            "phoneNumber": user_data.get("phoneNumber", "")
        })

    additional_info = personal_info_collection.find_one({"user_id": user_id}, {"_id": 0, "user_id": 0, "locator": 0})
    if additional_info:
        personal_information.update(additional_info)
        personal_information["statusCode"] = 200

    client.close()
    return personal_information
