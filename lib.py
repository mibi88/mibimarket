import json
import os
import random

json_data = {}

existing_items = ["gray fish", "worm", "box of sand", "golden tux",
"plastic tux", "shovel", "fishing pole"]

DATABASE = "db.json"

def get_db():
    global json_data
    return json.dumps(json_data, indent=4)
def load_db():
    global json_data
    with open(DATABASE, "r") as fp:
        json_data = json.loads(fp.read())
def save_db():
    global json_data
    with open(DATABASE, "w") as fp:
        fp.write(get_db())
def set_channel_rate(ctx):
    channel = interactions.api.models.channel.Channel()
    channel.id = ctx.channel_id
    ctx.channel_id.set_rate_limit_per_user(rate_limit_per_user = 1,
    reason = "Please do not spam !")


if os.path.exists(DATABASE):
    load_db()
else:
    json_data["users"] = {}
    json_data["market"] = []
    json_data["shop"] = {}
    json_data["prices"] = {"gray fish": 20, "box of sand": 40,
    "golden tux": 320, "plastic tux": 6, "shovel": 25, "fishing pole": 65}
    json_data["inflation"] = 0
    save_db()

##################### PROFILE #####################

def create_user(user):
    json_data["users"][user] = {}
    json_data["users"][user]["wallet"] = 0
    json_data["users"][user]["bank"] = 0
    json_data["users"][user]["bank_max"] = 30000
    json_data["users"][user]["inventory"] = {}
    json_data["users"][user]["probas"] = {}
    json_data["users"][user]["probas"]["fish"] = {"gray fish": 30}
    json_data["users"][user]["probas"]["dig"] = {"worm": 30, "box of sand": 10,
    "golden tux": 1, "plastic tux": 6, "shovel": 2}

def get_profile(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    wallet = json_data["users"][user]["wallet"]
    bank = json_data["users"][user]["bank"]
    bank_max = json_data["users"][user]["bank_max"]
    inventory = json_data["users"][user]["inventory"]
    newinventory = ""
    for key, values in inventory.items():
        newinventory += f"- {key} x{values}\n"
    if newinventory == "":
        newinventory = "You have nothing in your inventory."
    return f"""##### COINS #####
- ${wallet} in your wallet
- ${bank}/${bank_max} in your bank account
##### INVENTORY #####
{newinventory}"""

##################### INVENTORY #####################

def add_items(user, item, num):
    if not item in json_data["users"][user]["inventory"]:
        json_data["users"][user]["inventory"][item] = 1
    else:
        json_data["users"][user]["inventory"][item] += num

def del_items(user, item, num):
    json_data["users"][user]["inventory"][item] -= num
    if json_data["users"][user]["inventory"][item] <= 0:
        del json_data["users"][user]["inventory"][item]

def has_item(user, item, num):
    if item in json_data["users"][user]["inventory"]:
        if json_data["users"][user]["inventory"][item] >= num:
            return 1

##################### MONEY #####################

def pay(user, num):
    json_data["users"][user]["wallet"] -= int(num)

def get_money(user, num):
    json_data["users"][user]["wallet"] += int(num)

def has_money(user, num):
    if json_data["users"][user]["wallet"] >= int(num): return 1
    return 0

##################### BASIC ACTIONS #####################

def do_fish(user):
    if not user in json_data["users"]:
        create_user(user)
    if not has_item(user, "fishing pole", 1):
        return "You need to buy a fishing pole ..."
    proba = json_data["users"][user]["probas"]["fish"]
    items = ""
    for k, i in proba.items():
        r = random.randint(0, 100)
        if r < i:
            add_items(user, k, 1)
            items += f"- {k} x{1}\n"
    if items == "":
        items = "Nothing."
    save_db()
    return f"""##### YOU FISHED #####
{items}"""

def do_dig(user):
    if not user in json_data["users"]:
        create_user(user)
    proba = json_data["users"][user]["probas"]["dig"]
    items = ""
    if has_item(user, "shovel", 1):
        shovel = 1
    else:
        shovel = 0
    for k, i in proba.items():
        r = random.randint(0, 100)
        if not shovel:
            i = i // 2
        if r < i:
            add_items(user, k, 1)
            items += f"- {k} x{1}\n"
    if items == "":
        items = "Nothing.\n"
    if shovel and random.randint(1, 100) == 1:
            items += "But you broke your shovel !"
    save_db()
    return f"""##### YOU DIGGED #####
{items}"""

def do_sell(user, item, num):
    global existing_items
    item = item.lower()
    if not user in json_data["users"]:
        create_user(user)
    if not item in existing_items:
        return f"{item} is not a valid item !"
    if not item in json_data["prices"]:
        return f"""You cannot sell {item} in the shop.
Try to sell it in the market."""
    if not has_item(user, item, num):
        return f"You do not have {num} {item} !"
    del_items(user, item, num)
    price = int(num * json_data["prices"][item] + num * (json_data["prices"][item]/100*json_data["inflation"]))
    get_money(user, price)
    if item in json_data["shop"]:
        json_data["shop"][item] += num
    else:
        json_data["shop"][item] = num
    save_db()
    return f"""##### YOU SOLD #####
- {item} x{num} for ${price} ({json_data["inflation"]}% inflation)"""

def do_buy(user, item, num):
    global existing_items
    item = item.lower()
    if not user in json_data["users"]:
        create_user(user)
    if not item in existing_items:
        return f"{item} is not a valid item !"
    if not item in json_data["shop"]:
        return f"""This item is not available in the shop.
Check out the market."""
    price = int(num * json_data["prices"][item] + num * (json_data["prices"][item]/100*json_data["inflation"]))
    if not has_money(user, price):
        return f"You do not have ${price} !"
    add_items(user, item, num)
    pay(user, price)
    if json_data["shop"][item] > 1:
        json_data["shop"][item] -= num
    else:
        del json_data["shop"][item]
    save_db()
    return f"""##### YOU BROUGHT #####
- {item} x{num} for ${price} ({json_data["inflation"]}% inflation)"""

def do_shop_see(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    items = ""
    inflation = json_data["inflation"]
    for key, values in json_data["shop"].items():
        price = int(json_data["prices"][key] + json_data["prices"][key]/100*inflation)
        items += f"- {key} x{values} for ${price} per item ({inflation}% inflation)\n"
    if items == "":
        items = "There is nothing in the shop."
    return f"""##### SHOP #####
{items}"""
