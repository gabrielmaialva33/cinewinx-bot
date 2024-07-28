from CineWinx.utils.httpx import fetch

API_URL = "https://lexica.qewertyy.me"


async def list_models():
    return await fetch.get(f"{API_URL}/models")


# {
#     "models": {
#         "chat": [
#             {
#                 "id": 1,
#                 "name": "Gemma",
#                 "baseModel": ""
#             },
#             {
#                 "id": 5,
#                 "name": "gpt-3.5-turbo",
#                 "baseModel": "GPT"
#             },
#             {
#                 "id": 19,
#                 "name": "gpt-4",
#                 "baseModel": "GPT",
#                 "type": "Premium"
#             },
#             {
#                 "id": 18,
#                 "name": "Llama 2",
#                 "baseModel": "Llama",
#                 "version": "7b-chat-int8"
#             },
#             {
#                 "id": 14,
#                 "name": "Llama 2",
#                 "baseModel": "Llama",
#                 "version": "7b-chat-fp16"
#             },
#             {
#                 "id": 20,
#                 "name": "bard",
#                 "baseModel": "LLM"
#             },
#             {
#                 "id": 21,
#                 "name": "Mistral",
#                 "baseModel": "LLM",
#                 "version": "7b-instruct-v0.1"
#             },
#             {
#                 "id": 23,
#                 "name": "Gemini-Pro",
#                 "baseModel": "PaLM 2"
#             },
#             {
#                 "id": 24,
#                 "name": "Gemini-Pro-Vision",
#                 "baseModel": "PaLM 2"
#             },
#             {
#                 "id": 26,
#                 "name": "Llama 2",
#                 "baseModel": "Llama",
#                 "version": "13b-chat-awq"
#             },
#             {
#                 "id": 27,
#                 "name": "OpenHermes",
#                 "baseModel": "Mistral 7B",
#                 "version": "2.5-mistral-7b-awq"
#             },
#             {
#                 "id": 31,
#                 "name": "Zephyr",
#                 "baseModel": "LLM",
#                 "version": "7b-beta-awq"
#             }
#         ],
#         "image": [
#             {
#                 "id": 2,
#                 "name": "Meina Mix",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 3,
#                 "name": "AnyLora",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 4,
#                 "name": "AnyThingV4",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 7,
#                 "name": "Goofball Mix",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 8,
#                 "name": "MeinaHentai",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 9,
#                 "name": "DarkSushi Mix",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 10,
#                 "name": "SDXL",
#                 "baseModel": "SDXL 1.0"
#             },
#             {
#                 "id": 11,
#                 "name": "Creative",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 12,
#                 "name": "CreativeV2",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 13,
#                 "name": "Absolute Reality",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 17,
#                 "name": "CalicoMix",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 15,
#                 "name": "AnimeV1",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 16,
#                 "name": "Lexica",
#                 "baseModel": "SD",
#                 "type": "Exclusive"
#             },
#             {
#                 "id": 34,
#                 "name": "Dreamshaper",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 25,
#                 "name": "CetusMix",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 30,
#                 "name": "Anime",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 32,
#                 "name": "Anime 2",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 33,
#                 "name": "Dall-E",
#                 "baseModel": "Dall-E"
#             },
#             {
#                 "id": 35,
#                 "name": "Realistic",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 36,
#                 "name": "Logo",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 39,
#                 "name": "Sticker",
#                 "baseModel": "SD"
#             },
#             {
#                 "id": 40,
#                 "name": "Anime v1.1",
#                 "baseModel": "SD"
#             }
#         ],
#         "AntiNSFW": [
#             {
#                 "id": 28,
#                 "name": "Serene"
#             },
#             {
#                 "id": 29,
#                 "name": "nsfwjs",
#                 "source": "https://github.com/infinitered/nsfwjs"
#             },
#             {
#                 "id": 41,
#                 "name": "Limpid?"
#             }
#         ],
#         "customGPTs": [
#             {
#                 "id": 22,
#                 "name": "Title Generator",
#                 "baseModel": "gpt-3.5-turbo"
#             }
#         ],
#         "upscale": [
#             {
#                 "name": "Lexica",
#                 "id": 37
#             },
#             {
#                 "name": "Pixel",
#                 "id": 38
#             }
#         ]
#     },
#     "message": "ok",
#     "code": 2
# }


async def get_chats_model():
    response = await list_models()
    return response["models"]["chat"]


async def get_images_model():
    response = await list_models()
    return response["models"]["image"]
