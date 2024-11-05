import os
from enum import Enum

from CustomException import CustomException


class Keys(Enum):
    TOKEN_KEY = "TOKEN_KEY"
    CONTRACT_ADDRESS = "CONTRACT_ADDRESS"
    PRIVATE_KEY = "PRIVATE_KEY"
    ABI_FILE_HASH = "ABI_FILE_HASH"
    ABI_FILE_PATH = "ABI_FILE_PATH"
    ISS = "ISS"
    MINUTES_EXP = "MINUTES_EXP"
    CONTRACT1_HASH = "CONTRACT1_HASH"
    CONTRACT2_HASH = "CONTRACT2_HASH"
    SOLCX_PATH = "SOLCX_PATH"

def get_secret(key: Keys) -> str:
    key = key.value
    secrets = {}
    secrets_file_path = os.path.join(os.path.dirname(__file__), 'secrets.txt')
    with open(secrets_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('==', 1)
            if len(parts) == 2:
                secrets[parts[0]] = parts[1]
    if key in secrets:
        return secrets[key]
    else:
        raise CustomException(f"Secretul cu cheia {key} nu exista!", 500)


def update_secret(key: Keys, value):
    key = key.value
    secrets = {}
    secrets_file_path = os.path.join(os.path.dirname(__file__), 'secrets.txt')
    found = False
    with open(secrets_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('==', 1)
            if len(parts) == 2:
                secrets[parts[0]] = parts[1]
                if parts[0] == key:
                    found = True
    if not found:
        raise CustomException(f"Secret with key {key} does not exist!", 404)

    with open(secrets_file_path, 'w') as file:
        for k, v in secrets.items():
            if k == key:
                file.write(f"{k}=={value}\n")
            else:
                file.write(f"{k}=={v}\n")
# token_key = get_secret_value('TOKEN_KEY')
