import datetime

EXPORT_FOLDER = "{}".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

API_ENPOINT = "https://api.swu-db.com"

SETS = [
    "ibh",
    "sec",
    "twi",
    "g25",
    "jtl",
    "law",
    "sor",
    "gg",
    "lof",
    "ts26",
    "shd",
    "c24",
    "c25",
    "j24",
    "j25",
    "p25",
    "p26",
    "ss1",
    "ss1j",
    "ss2",
    "ss2j"
]

IMAGE_PARAM = {
    "format": "image"
}

IMAGE_BACK_PARAM = {
    "format": "image",
    "face" : True
}

def CARDS_ENDPOINT(card_set: str):
    return "https://api.swu-db.com/cards/{}".format(card_set)

def CARD_ENDPOINT(card_set: str, card: int):
    return "https://api.swu-db.com/cards/{}/{}".format(card_set, int(card))
