from db.mongo_conn import create as create_mongo_conn
from tokenz.tokens import generate_password_reset_token, verify_password_reset_token
from notification_service.emails.service import send_password_reset_email
import bcrypt

def request_password_reset(email):
    client = create_mongo_conn()
    db = client['exodus']
    users_collection = db['users']

    user = users_collection.find_one({"email": email})

    if not user:
        client.close()
        return {"Message": "No account found with this email address", "statusCode": 404}

    reset_token = generate_password_reset_token(str(user['_id']))
    
    result = send_password_reset_email(email, reset_token)

    client.close()
    return result

def reset_password(reset_token, new_password):
    token_data = verify_password_reset_token(reset_token)

    if token_data == 0:
        return {"Message": "Invalid or expired token", "statusCode": 400}

    user_id = token_data['sub']

    client = create_mongo_conn()
    db = client['exodus']
    users_collection = db['users']

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    result = users_collection.update_one(
        {"_id": user_id},
        {"$set": {"password": hashed_password}}
    )

    client.close()

    if result.modified_count == 1:
        return {"Message": "Password successfully reset", "statusCode": 200}
    else:
        return {"Message": "Failed to reset password", "statusCode": 500}
