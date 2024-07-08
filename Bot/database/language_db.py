from Bot.core.mongo import mongodb

lang_db = mongodb.language
lang_m = {}


async def get_lang(chat_id: int) -> str:
    """
    Get the language of the chat
    :param chat_id:
    :return:
    """
    mode = lang_m.get(chat_id)
    if not mode:
        lang = await lang_db.find_one({"chat_id": chat_id})
        if not lang:
            lang_m[chat_id] = "pt-br"
            return "pt-br"
        lang_m[chat_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(chat_id: int, lang: str):
    """
    Set the language of the chat
    :param chat_id:
    :param lang:
    :return:
    """
    lang_m[chat_id] = lang
    await lang_db.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)
