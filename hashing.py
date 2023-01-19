from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash():
    def bcrypt(password: str):
        return password_context.hash(password)
