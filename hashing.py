from passlib.context import CryptContext

# bycrypt algoritm set kar rhe hai hashing ke liye
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)
    