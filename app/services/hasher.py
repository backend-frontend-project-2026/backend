from pwdlib import PasswordHash


class Hasher:
    _password_hash = PasswordHash.recommended()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls._password_hash.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._password_hash.verify(plain_password, hashed_password)