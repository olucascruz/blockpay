from passlib.context import CryptContext
from Block import Block

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(list_users: list[Block], username: str, password: str):
    user = False
    for block in list_users:
        if block["data"]["email"] == username:
            user = block

    if not user:
        return False
    
    hashed_password = block["data"]["senha"]
    if not verify_password(password,  hashed_password):
        return False
    return user