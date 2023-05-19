import json
import os
import random

json_data = {}

existing_items = ["gray fish", "worm", "box of sand", "golden tux",
"plastic tux", "shovel", "fishing pole", "seaweed", "wetsuit", "marble tux",
"golden treasure", "exotic fish", "multicolor fish", "luminescent fish",
"golden fish", "diamond fish", "bank note"]

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
    json_data["market"] = {}
    json_data["marketprice"] = 3
    json_data["shop"] = {}
    json_data["prices"] = {"gray fish": 20, "box of sand": 40,
    "golden tux": 320, "plastic tux": 6, "shovel": 25, "fishing pole": 65,
    "wetsuit": 65, "marble tux": 220, "golden treasure": 860, "exotic fish": 25,
    "multicolor fish": 45, "luminescent fish": 140, "golden fish": 280}
    json_data["non_sellable_prices"] = {"worm": 1, "seaweed": 3}
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
    json_data["users"][user]["probas"]["fish"] = {"gray fish": 30,
    "exotic fish": 10, "multicolor fish": 5, "luminescent fish": 3,
    "golden fish": 2, "diamond fish": 1}
    json_data["users"][user]["probas"]["dig"] = {"worm": 30, "box of sand": 10,
    "golden tux": 1, "plastic tux": 6, "shovel": 2, "bank note": 4}
    json_data["users"][user]["probas"]["dive"] = {"seaweed": 30,
    "fishing pole": 10, "wetsuit": 5, "marble tux": 4, "golden treasure": 1}

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
    return f"""##### PROFILE #####
User {user}
##### COINS #####
- ${wallet} in the wallet
- ${bank}/${bank_max} in the bank account
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

def do_deposit(user, num):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    num = int(num)
    if not has_money(user, num):
        return f"You do not have ${num} in your wallet."
    if json_data["users"][user]["bank"] + num <= json_data["users"][user]["bank_max"]:
        json_data["users"][user]["bank"] += num
        pay(user, num)
        save_db()
        return f"You deposited ${num} on your bank account."
    else:
        return "You need more space on your bank account."

def do_withdraw(user, num):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    if json_data["users"][user]["bank"] < num:
        return f"You do not have ${num} on your bank account."
    get_money(user, num)
    json_data["users"][user]["bank"] -= num
    save_db()
    return f"You withdrew ${num} from your bank account."

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
            del_items("shovel", 1)
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

def do_dive(user):
    if not user in json_data["users"]:
        create_user(user)
    proba = json_data["users"][user]["probas"]["dive"]
    items = ""
    if has_item(user, "wetsuit", 1):
        wetsuit = 1
    else:
        wetsuit = 0
    for k, i in proba.items():
        r = random.randint(0, 100)
        if not wetsuit:
            i = i // 2
        if r < i:
            add_items(user, k, 1)
            items += f"- {k} x{1}\n"
    if items == "":
        items = "Nothing.\n"
    if wetsuit and random.randint(1, 100) == 1:
            items += "But you broke your wetsuit !"
            del_items("wetsuit", 1)
    save_db()
    return f"""##### YOU FOUND #####
{items}"""

##################### MARKET #####################

def update_marketprice():
    if len(json_data["market"]) < 50 and json_data["marketprice"] > 1:
        if random.randint(1, 30): json_data["marketprice"] -= 1
        if random.randint(1, 30): json_data["inflation"] += 1
    elif json_data["marketprice"] < 100:
        if random.randint(1, 30): json_data["marketprice"] += 1
        if random.randint(1, 30): json_data["inflation"] -= 1

def do_market_add(user, type, item, amount, for_item, for_amount):
    type = type.lower()
    item = item.lower()
    for_item = for_item.lower()
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    if not item in existing_items:
        return f"{item} is not a valid item !"
    if type != "buy" and type != "sell":
        return f"""{type} is not a valid type in the market !
type can be :
buy : You want to buy something
sell : You want to sell something"""
    if type == "sell":
        if not has_item(user, item, amount):
            return f"You do not have {amount} {item} !"
    else:
        if not has_item(user, for_item, for_amount):
            return f"You do not have {for_amount} {for_item} !"
    if not for_item in existing_items and for_item != "coins":
        return f"{for_item} is not a valid item !"
    if for_item == "coins":
        price = int(for_amount/100*json_data["marketprice"])
    else:
        if for_item in json_data["prices"]:
            price = int((json_data["prices"][for_item]*for_amount)/100*json_data["marketprice"]*json_data["inflation"])
        elif for_item in json_data["non_sellable_prices"]:
            price = int((json_data["non_sellable_prices"][for_item]*for_amount)/100*json_data["marketprice"]*json_data["inflation"])
        else:
            return f"Item {for_item} has an unknown price !"
        if price < 1:
            price = 1
        if not has_money(user, price):
            return f"You need ${price} to post this offer !"
        pay(user, price)
    id = 0
    while str(id) in json_data["market"]: id += 1
    json_data["market"][str(id)] = {"user": user, "type": type, "item": item,
    "amount": amount, "for_item": for_item, "for_amount": for_amount}
    update_marketprice()
    save_db()
    return f"""##### MARKET #####
You added an offer :
Id : {id}
Offer of type {type}.
- {item} x{amount}
- For : {for_item} x{for_amount}
"""

def do_market_remove(user, id):
    id = str(id)
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    if not id in json_data["market"]:
        return f"id {id} does not exists !"
    if user == json_data["market"][id]["user"]:
        del json_data["market"][id]
        update_marketprice()
        save_db()
        return f"You removed offer {id}."
    return f"You connot remove offer {id}."

def do_market_accept(user, id, amount):
    id = str(id)
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    if not id in json_data["market"]:
        return f"id {id} does not exists !"
    dest = json_data["market"][id]["user"]
    if user == dest:
        return "You cannot accept your own offer."
    if amount == None: amount = 1
    if json_data["market"][id]["type"] == "sell":
        if amount > json_data["market"][id]["amount"]:
            return "You cannot buy so much at this offer."
        if json_data["market"][id]["for_item"] == "coins":
            if not has_money(user, amount):
                for_amount = json_data["market"][id]["for_amount"]
                return f"You do not have ${for_amount} !"
            add_items(user, json_data["market"][id]["item"], amount)
            del_items(dest, json_data["market"][id]["item"], amount)
            price = int(json_data["market"][id]["for_amount"]/json_data["market"][id]["amount"]*amount)
            pay(user, price)
            get_money(dest, price)
        else:
            if not has_item(user, json_data["market"][id]["for_item"], amount):
                for_item = json_data["market"][id]["for_item"]
                return f"You do not have {amount} {for_item} !"
            dest = json_data["market"][id]["user"]
            add_items(user, json_data["market"][id]["item"], amount)
            del_items(dest, json_data["market"][id]["item"], amount)
            add_items(dest, json_data["market"][id]["for_item"], amount)
            del_items(user, json_data["market"][id]["for_item"], amount)
    elif json_data["market"][id]["type"] == "buy":
        dest = json_data["market"][id]["user"]
        if amount > json_data["market"][id]["for_amount"]:
            return "You cannot sell so much at this offer."
        if json_data["market"][id]["for_item"] == "coins":
            if not has_money(dest, amount):
                coins = json_data["market"][id]["for_amount"]
                return f"You do not have ${coins} !"
            del_items(user, json_data["market"][id]["item"], amount)
            add_items(dest, json_data["market"][id]["item"], amount)
            price = int(json_data["market"][id]["for_amount"]/json_data["market"][id]["amount"]*amount)
            get_money(user, price)
            pay(dest, price)
        else:
            if not has_item(user, json_data["market"][id]["item"], amount):
                for_item = json_data["market"][id]["for_item"]
                return f"You do not have {amount} {for_item} !"
            del_items(user, json_data["market"][id]["item"], amount)
            add_items(dest, json_data["market"][id]["item"], amount)
            del_items(dest, json_data["market"][id]["for_item"], amount)
            add_items(user, json_data["market"][id]["for_item"], amount)
    else:
        type = json_data["market"][id]["type"]
        return f"Unknown offer type {type}"
    if json_data["market"][id]["type"] == "buy":
        text = f"""You accepted offer {id}
You got :
{json_data["market"][id]["for_item"]} x{amount}"""
    else:
        text = f"""You accepted offer {id}
You got :
{json_data["market"][id]["item"]} x{amount}"""
    del json_data["market"][id]
    update_marketprice()
    save_db()
    return text

def do_market_see(user, item):
    item = item.lower()
    if not item in existing_items:
        return f"{item} is not a valid item !"
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    out = ""
    for i in json_data["market"]:
        if json_data["market"][i]["item"] == item:
            out += f"""MARKET OFFER
Id : {i}
Offer of type {json_data["market"][i]["type"]}.
- {json_data["market"][i]["item"]} x{json_data["market"][i]["amount"]}
- For : {json_data["market"][i]["for_item"]} x{json_data["market"][i]["for_amount"]}
"""
        if json_data["market"][i]["item"] == user:
            out += "(Posted by you)\n"
    if out == "":
        return "Ow, there is nothing in the market for this item ..."
    else:
        return f"##### MARKET #####\n\n{out}"

##################### ECONOMY #####################

def view_stat(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    return f"""##### ECONOMY #####
Inflation : {json_data["inflation"]}%
Offer price in the market : {json_data["marketprice"]}%
of the income of the offer.
"""
