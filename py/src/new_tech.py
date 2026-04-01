import requests
import new_tech_config as Config
import os

def download_images(_set: str):
    choosen_set = _set
    
    print("- Creating export folder")
    os.makedirs(os.path.join(Config.EXPORT_FOLDER, choosen_set))
    
    print("- Getting cards in set: {}".format(choosen_set.upper()))
    res = requests.get(Config.CARDS_ENDPOINT(choosen_set)).json()
    num_of_cards = res["total_cards"]
    cards_in_set = res["data"]
    print("- Cards found in set {}: {}".format(choosen_set.upper(), num_of_cards))
    yield num_of_cards
    
    for card in cards_in_set:
        title = "{}_{}".format(
            card["Number"],
            card["Name"].replace(" ", "_").replace("-", "_")
        )
        if "Subtitle" in card:
            title += "_{}".format(card["Subtitle"].replace(" ", "_").replace("-", "_"))
        image_req = requests.get(
            Config.CARD_ENDPOINT(choosen_set, card["Number"]),
            params=Config.IMAGE_PARAM
        )
        image_type = image_req.headers.get("content-type").split("/")[-1]
        with open(os.path.join(Config.EXPORT_FOLDER, choosen_set, "{}.{}".format(title, image_type)), "wb") as front:
            front.write(image_req.content)
            print("- Saved card: {}".format(title))
        yield title
        if card["DoubleSided"]:
            image_back_req = requests.get(
                Config.CARD_ENDPOINT(choosen_set, card["Number"]),
                params=Config.IMAGE_BACK_PARAM
            )
            image_back_type = image_req.headers.get("content-type").split("/")[-1]
            with open(os.path.join(Config.EXPORT_FOLDER, choosen_set, "{}-back.{}".format(title, image_back_type)), "wb") as front:
                front.write(image_req.content)
                print("- Saved card: {}-back".format(title))
            yield "{}-back".format(title)
    