from repo.database_repo import get_user_by_username, get_user_by_id
from security.security_service import *
from CustomException import *

def login_user(username, password):
    password = hash_password(password)
    user = get_user_by_username(username)
    if user:
        if user.is_active == False:
            raise CustomException("User is deactivated!", 403)

        if user.password == password:
            return gen_token(user.id), user.role
        else:
            print("Parola gresita!")
            raise CustomException("Wrong credentials!", 401)
    else:
        print("Username gresit!")
        raise CustomException("Wrong credentials!", 401)

def get_role_by_id(id):
    user = get_user_by_id(id)
    if user:
        return user.role
    raise CustomException("User not found!", 404)

def change_password(token, curr, new):
    decoded = decode_and_verify_token(token)
    user = get_user_by_id(decoded['sub'])
    if user.password == hash_password(curr):
        dbc.update_password_by_username(user.username, hash_password(new))
        user.password = hash_password(new)
        user.save()
        return "ok"
    else:
        raise CustomException("Wrong current password!", 401)
