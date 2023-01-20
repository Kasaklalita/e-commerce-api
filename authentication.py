
async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if user and verify_password(password, user.password)


async def token_generator(username: str, password: str):
    user = await authenticate_user(username, password)
    pass
