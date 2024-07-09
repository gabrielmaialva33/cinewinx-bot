from Bot.core.mongo import mongodb

bans_db = mongodb.bans
blocked_db = mongodb.blockeds


# banned users
async def get_banned() -> list:
    """
    Get all the banned users
    :return:
    """
    results = []
    async for user in bans_db.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results


async def get_blocked_users() -> list:
    """
    Get all the blocked users
    :return:
    """
    results = []
    async for user in blocked_db.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results
