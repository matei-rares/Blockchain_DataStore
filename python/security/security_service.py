import base64
import hashlib
import json
from datetime import datetime, timedelta
import uuid
import jwt
from CustomException import *
from security.token_service import *
from repo import database_repo as dbc
from security.secrets_reader import get_secret,Keys

ISS = get_secret(Keys.ISS)
SECRET = get_secret(Keys.TOKEN_KEY)
MINUTES_EXP = int(get_secret(Keys.MINUTES_EXP))


##########################TOKEN#####################################
def gen_token(id_user):
    time = datetime.utcnow()
    time = time + timedelta(minutes=MINUTES_EXP)
    exp_date = time
    claims = {
        "iss": ISS,
        "sub": id_user,
        "exp": exp_date,
        "jti": str(uuid.uuid4()),
    }
    token = jwt.encode(claims, SECRET, algorithm='HS256')
    return token


def refresh_token(token):
    decoded = decode_and_verify_token(token)
    time = datetime.utcnow()
    time = time + timedelta(minutes=MINUTES_EXP)
    exp_date = time
    claims = {
        "iss": ISS,
        "sub": decoded['sub'],
        "exp": exp_date,
        "jti": decoded['jti'],
    }
    token = jwt.encode(claims, SECRET, algorithm='HS256')
    return token


def decode_and_verify_token(token):
    blacklisted = False
    try:
        blocked_tokens = []
        for t in read_blacklist():
            blocked_tokens.append(t[1])

        if token not in blocked_tokens:
            decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])  # semnatura e verificata aici
            if decoded_token['iss'] != ISS:
                write_to_blacklist(decoded_token['jti'], token)
                raise CustomException("ISS invalid!", 401)

            try:
                dbc.get_user_by_id(decoded_token['sub'])  # verific daca sub e in db
            except Exception as es:
                raise CustomException("Acest sub nu e valid!", 401)

            return decoded_token
        else:
            blacklisted = True
            raise CustomException("Token invalid", 401)
    except Exception as e:
        if blacklisted == False:
            try:
                count_dots = token.count(".")
                if count_dots == 2:
                    _, payload, _ = token.split(".")
                    padding = len(payload) % 4
                    if padding:
                        payload += '=' * (4 - padding)

                    dec = base64.urlsafe_b64decode(payload).decode('utf-8')
                    decoded = json.loads(dec)
                    if decoded.get('jti'):
                        write_to_blacklist(decoded['jti'], token)
                    else:
                        write_to_blacklist(str(uuid.uuid4()), token)
                else:
                    write_to_blacklist(str(uuid.uuid4()), token)
            except Exception as ess:
                print("Error decoding that token")
                raise CustomException("Token invalid!", 401)
        if "Signature" in str(e):
            raise CustomException("Token expirat!", 401)
        raise CustomException(str(e), 400)

def cancel_token(token):
    write_to_blacklist(str(uuid.uuid4()),token)

##########################TOKEN#####################################

##########################VERIFY USER DATA#####################################
def verify_user_data(username, password, role):
    verify_username(username)
    verify_password(password)
    verify_role(role)
    return True


def verify_password(password):
    if len(password) < 1:
        raise CustomException("Parola trebuie sa aiba minim 2 caractere!", 422)
    if len(password) > 100:
        raise CustomException("Parola trebuie sa aiba maxim 50 caractere!", 422)
    return True


def verify_username(username):
    if len(username) < 1:
        raise CustomException("Username-ul trebuie sa aiba minim 2 caractere!", 422)
    if len(username) > 50:
        raise CustomException("Username-ul trebuie sa aiba maxim 50 caractere!", 422)
    return True


def verify_role(role):
    if role not in ["ADMIN", "USER"]:
        raise CustomException("Rolul trebuie sa fie ADMIN sau USER", 422)
    return True


##########################VERIFY USER DATA#####################################

def hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_password = sha256_hash.hexdigest()
    return hashed_password

