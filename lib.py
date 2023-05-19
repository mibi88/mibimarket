import json
import os
import random
import datetime as dt

json_data = {}

VERSION = "v.0.1a2"

ABOUT = f"""##### ABOUT MIBIMARKET #####

Mibimaket {VERSION}
(c) 2023 mibi88

The commands that you can use :
- /profile       : See your profile.
- /fish          : Fish for some items. You need to have a fishing pole.
- /dig           : Dig to get some items. With a shovel you have x2 more chances
                   to get something. You have 1 chance of 100 to break your
                   shovel.
- /shop_sell     : Sell an item. Some items are not sellable in the shop, so you
                   need to sell them in the market.
- /shop_buy      : Buy an item from the shop.
- /shop_view     : See which items are in the shop.
- /dive          : Dive in the sea to find some items. With a wetsuit you have
                   2x more chances to find items. You have 1 chance of 100 to
                   break your wetsuit.
- /scratch       : Scratch a ticket and see what you won. You can only do that
                   1x per hour. This is in some cases the only way to get some
                   items.
- /deposit       : Deposit some coins on your bank account.
- /withdraw      : Withdraw some coins from your bank account.
- /use           : Use an item. If you use the following items, that's what it
                   does :
  - "bank note"  : You get more space on your bank account.
  - "deed"       : You have a bigger farm.
  - "classic box": Open the box and see what you got !
  - "farmer box" : Open the box and see what you got !
- /rob           : Rob some coins from the wallet of someone. If you have some
                   beer, you can drink beer and then you have 2x more chances to
                   be caught but you can get 2x more coins. You will also pay
                   only $50 if you where caught.
- /market_add    : Post an offer on the market. You can post an offer to sell
                   something or for buying something. You need to pay something
                   when you post an offer.
- /market_remove : Remove an offer from the market.
- /market_accept : Accept an offer from the market. By default you will accept
                   the offer for only one item.
- /market_view   : View what's in the market for one item. That's were tou get
                   the id of an offer.
- /economy_info  : See what's the price to post an offer on the market and the %
                   of inflation.
- /price         : Get the price of an item (and sometimes some extra infos).
- /farm_plant    : Plant some seeds and let a this plant grow !
- /farm_view     : See what's in your fields !
- /farm_harvest  : Harvest your crops.
+ an easter egg HAHA !

Contact me at <mbcontact50@gmail.com> if you find a bug.
"""

usable_items = ["bank note", "deed", "farmer box", "classic box"]

existing_items = ["gray fish", "worm", "box of sand", "golden tux",
"plastic tux", "shovel", "fishing pole", "seaweed", "wetsuit", "marble tux",
"golden treasure", "exotic fish", "multicolor fish", "luminescent fish",
"golden fish", "diamond fish", "bank note", "farmer box", "classic box",
"potato seeds", "watermelon seeds", "corn seeds", "bone seeds",
"carrot seeds", "brocoli seeds", "hoe", "potato", "watermelon", "corn", "bone",
"carrot", "brocoli", "beer", "deed", "barrel"]

farm_out = {
    "potato seeds": "potato",
    "corn seeds": "corn",
    "bone seeds": "bone",
    "carrot seeds": "carrot",
    "brocoli seeds": "brocoli",
    "watermelon seeds": "watermelon"
}

farm_amount = {
    "potato seeds": [1, 5],
    "corn seeds": [2, 6],
    "bone seeds": [2, 6],
    "carrot seeds": [2, 12],
    "brocoli seeds": [1, 3],
    "watermelon seeds": [2, 3]
}

craftings = {
    "potato seeds": {
        "recipe": {"potato": 1},
        "amount": 2
    },
    "corn seeds": {
        "recipe": {"corn": 1},
        "amount": 2
    },
    "bone seeds": {
        "recipe": {"bone": 1},
        "amount": 2
    },
    "carrot seeds": {
        "recipe": {"carrot": 1},
        "amount": 2
    },
    "brocoli seeds": {
        "recipe": {"brocoli": 1},
        "amount": 2
    },
    "watermelon seeds": {
        "recipe": {"watermelon": 1},
        "amount": 2
    },
    "beer": {
        "recipe": {"corn": 5, "barrel": 1},
        "amount": 5
    }
}

classic_box_items = [
    "beer",
    "shovel",
    "wetsuit",
    "fishing pole",
    "bank note",
    "deed",
    "plastic tux"
]

farmer_box_items = [
    "beer",
    "hoe",
    "potato seeds",
    "corn seeds",
    "bone seeds",
    "carrot seeds",
    "brocoli seeds",
    "watermelon seeds",
    "potato",
    "watermelon",
    "corn",
    "bone",
    "carrot",
    "brocoli",
    "deed"
]

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
    "multicolor fish": 45, "luminescent fish": 140, "golden fish": 280,
    "diamond fish": 1120, "bank note": 65, "farmer box": 1620, "classic box": 1270,
    "potato seeds": 5, "watermelon seeds": 30, "corn seeds": 10, "bone seeds": 15,
    "carrot seeds": 20, "brocoli seeds": 25, "hoe": 30, "potato": 10,
    "watermelon": 35, "corn": 15, "bone": 20, "carrot": 25, "brocoli": 30,
    "beer": 40, "deed": 85, "barrel": 75}
    json_data["non_sellable_prices"] = {"worm": 1, "seaweed": 3}
    json_data["inflation"] = 0
    json_data["scratch_update"] = 255
    json_data["scratch_now"] = []
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
    "golden tux": 1, "plastic tux": 6, "shovel": 2, "bank note": 4, "deed": 2,
    "hoe": 4}
    json_data["users"][user]["probas"]["dive"] = {"seaweed": 30,
    "fishing pole": 10, "wetsuit": 5, "marble tux": 4, "golden treasure": 1,
    "barrel": 5}
    json_data["users"][user]["lastscratch"] = 255
    json_data["users"][user]["farm_size"] = 9
    json_data["users"][user]["farm_items"] = []
    json_data["users"][user]["growing_speed"] = {"watermelon seeds": 30,
    "brocoli seeds": 25, "carrot seeds": 20, "bone seeds": 15, "corn seeds": 10,
    "potato seeds": 5}

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
        json_data["users"][user]["inventory"][item] = num
    else:
        json_data["users"][user]["inventory"][item] += num

def del_items(user, item, num):
    json_data["users"][user]["inventory"][item] -= num
    if json_data["users"][user]["inventory"][item] <= 0:
        del json_data["users"][user]["inventory"][item]

def has_item(user, item, num):
    if item in json_data["users"][user]["inventory"]:
        if json_data["users"][user]["inventory"][item] >= num and num > 0:
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

##################### BOT #####################

def about_this_bot(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    return ABOUT

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
            del_items(user, "shovel", 1)
    save_db()
    return f"""##### YOU DIGGED #####
{items}"""

def do_sell(user, item, num):
    global existing_items
    item = item.lower().strip()
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
    update_marketprice()
    save_db()
    return f"""##### YOU SOLD #####
- {item} x{num} for ${price} ({json_data["inflation"]}% inflation)"""

def do_buy(user, item, num):
    global existing_items
    item = item.lower().strip()
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
    update_marketprice()
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
            del_items(user, "wetsuit", 1)
    save_db()
    return f"""##### YOU FOUND #####
{items}"""

def do_use(user, item, num):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    item = item.lower().strip()
    if not item in existing_items:
        return f"The item {item} item do not exists"
    if not has_item(user, item, num):
        return f"You do not have {item}"
    if not item in usable_items:
        return f"You cannot use {item}"
    used = 1
    message = ""
    for i in range(num):
        if item == "bank note":
            json_data["users"][user]["bank_max"] += random.randint(20000, 40000)
        elif item == "deed":
            json_data["users"][user]["farm_size"] += random.randint(5, 9)
        elif item == "classic box" or item == "farmer box":
            items_got = []
            message = "You got :\n"
            for i in range(5):
                if item == "farmer box": items_got.append(random.choice(farmer_box_items))
                else: items_got.append(random.choice(classic_box_items))
            for i in items_got:
                amount = random.randint(1, 3)
                add_items(user, i, amount)
                message += f" - {i} x{amount}\n"
        else:
            used = 0
    if used == 0:
        save_db()
        return f"""There was a bug that made that you could not use this item.
Please post an issue or contact the developper."""
    else:
        del_items(user, item, num)
    save_db()
    return f"You used {num}x {item}\n{message}"

def do_rob(user, dest, has_beer):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    if not dest in json_data["users"]:
        create_user(dest)
        save_db()
    if not has_money(user, 100):
        return f"You need to have at least $100."
    if not has_money(dest, 100):
        return f"User {dest} has less than $100."
    message = ""
    div = 1
    if has_item(user, "beer", 1) and has_beer:
        message = "You drunk some beer before.\n"
        del_items(user, "beer", 1)
        div = 2
    elif has_beer:
        return f"You do not have some beer."
    amount = random.randint(1, 100*div)
    if random.randint(1, 20//div) == 0:
        pay(user, 100//div)
        save_db()
        if div == 2: return f"You where caught and paid $50"
        else: return f"You where caught and paid $100"
    else:
        pay(dest, amount)
        get_money(user, amount)
        save_db()
        return f"You robbed ${amount}"

def do_scratch(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    hour = dt.datetime.now().hour
    if hour == json_data["users"][user]["lastscratch"]:
        return f"You already scratched in this hour"
    if json_data["scratch_update"] != hour:
        json_data["scratch_now"] = []
        num = random.randint(1, 5)
        for i in range(num):
            json_data["scratch_now"].append(random.choice(existing_items))
        json_data["scratch_update"] = hour
    items_got = ""
    scratch_items = ""
    for i in json_data["scratch_now"]:
        scratch_items += f" - {i}\n"
        if random.randint(1, len(json_data["scratch_now"])) == 1:
            items_got += f" - {i}\n"
            add_items(user, i, 1)
    json_data["users"][user]["lastscratch"] = hour
    if items_got == "": items_got = "Nothing.\n"
    save_db()
    return f"""##### YOU SCRATCHED #####
{items_got}
And you could get :
{scratch_items}
"""

##################### MARKET #####################

def update_marketprice():
    if len(json_data["market"]) < 50 and json_data["marketprice"] > 1:
        if random.randint(0, 30) == 0: json_data["marketprice"] -= 1
        if random.randint(0, 30) == 0: json_data["inflation"] += 1
    elif json_data["marketprice"] < 100:
        if random.randint(0, 30) == 0: json_data["marketprice"] += 1
        if random.randint(0, 30) == 0: json_data["inflation"] -= 1
    shop_sum = 0
    for i in json_data["shop"].values(): shop_sum += i
    if shop_sum < 50:
        if random.randint(0, 60) == 0: json_data["inflation"] += 1
    elif shop_sum < 100:
        if random.randint(0, 60) == 0: json_data["inflation"] -= 1

def do_market_add(user, type, item, amount, for_item, for_amount):
    type = type.lower().strip()
    item = item.lower().strip()
    for_item = for_item.lower().strip()
    if for_amount < 1 or amount < 1:
        return "You cannot post an offer for less than 1 item."
    if for_item != "coins" and amount != for_amount:
        return """If you post for coins,
amount and for_amount need to be the same."""
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
    if json_data["market"][id]["type"] == "sell":
        if not has_item(dest, json_data["market"][id]["item"], amount):
            item = json_data["market"][id]["item"]
            return f"User {dest} has not {item} x{amount} anymore."
        if amount > json_data["market"][id]["amount"]:
            return "You cannot buy so much at this offer."
        if json_data["market"][id]["for_item"] == "coins":
            if not has_money(user, amount):
                for_amount = json_data["market"][id]["for_amount"]/json_data["market"][id]["amount"]*amount
                return f"You do not have ${for_amount} !"
            add_items(user, json_data["market"][id]["item"], amount)
            del_items(dest, json_data["market"][id]["item"], amount)
            price = round(json_data["market"][id]["for_amount"]/json_data["market"][id]["amount"]*amount)
            if price < 1: price = 1
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
        if amount > json_data["market"][id]["for_amount"]:
            return "You cannot sell so much at this offer."
        if not has_item(dest, json_data["market"][id]["for_item"], amount):
            item = json_data["market"][id]["for_item"]
            return f"User {dest} has not {item} x{amount} anymore."
        if json_data["market"][id]["for_item"] == "coins":
            if not has_money(dest, amount):
                coins = json_data["market"][id]["for_amount"]
                return f"You do not have ${coins} !"
            del_items(user, json_data["market"][id]["item"], amount)
            add_items(dest, json_data["market"][id]["item"], amount)
            price = round(json_data["market"][id]["for_amount"]/json_data["market"][id]["amount"]*amount)
            if price < 1: price = 1
            get_money(user, price)
            pay(dest, price)
        else:
            if not has_item(user, json_data["market"][id]["item"], amount):
                item = json_data["market"][id]["item"]
                return f"You do not have {amount} {item} !"
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
    json_data["market"][id]["amount"] -= amount
    if json_data["market"][id]["amount"] <= 0:
        del json_data["market"][id]
    update_marketprice()
    save_db()
    return text

def do_market_see(user, item):
    item = item.lower().strip()
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

def view_price(user, item):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    item = item.lower().strip()
    if not item in existing_items:
        return f"Item {item} does not exists."
    if item in json_data["prices"]:
        price_normal = json_data["prices"][item]
    elif item in json_data["non_sellable_prices"]:
        price_normal = json_data["non_sellable_prices"][item]
    else:
        return f"Ow, I could not find the price of {item}. Please report it to the developpers."
    price_inflation = int(price_normal+price_normal/100*json_data["inflation"])
    specific_infos = ""
    if item in json_data["users"][user]["growing_speed"]:
        speed = json_data["users"][user]["growing_speed"][item]
        specific_infos += "This item takes ~{speed}min to grow when he is planted."
    return f"""##### PRICES #####
Item {item} costs ${price_normal} with 0% Inflation.
   > {item} costs ${price_inflation} with {json_data["inflation"]}% inflation.
"""

##################### FARMING #####################

def get_growing_speed(user, data):
    time = data["time"].split("-")
    for i, n in enumerate(time): time[i] = int(n)
    start = dt.datetime(time[0], time[1], time[2], time[3], time[4])
    end = dt.datetime.now()
    return (end - start).total_seconds()//60

def update_farm_state(user):
    for i, data in enumerate(json_data["users"][user]["farm_items"]):
        item = data["item"]
        if not data["stat"]:
            min = get_growing_speed(user, data)
            if min >= data["growing_speed"]:
                json_data["users"][user]["farm_items"][i]["stat"] = 1

def do_farm_see(user):
    if not user in json_data["users"]:
        create_user(user)
    items = ""
    update_farm_state(user)
    for i, data in enumerate(json_data["users"][user]["farm_items"]):
        item = data["item"]
        if data["stat"]:
            stat = "Ready to harvest"
        else:
            stat = "Growing ..."
        time = int(json_data["users"][user]["growing_speed"][item]-(get_growing_speed(user, data)//5*5))
        if time < 0: time = 0
        items += f" - {item} : {stat}\n"
        if not data["stat"]: items += f"   It will take ~{time}min to grow.\n"
    if items == "":
        items = "Nothing."
    save_db()
    return f"""##### FARM #####
The content of your fields :
{items}
"""

def do_farm_plant(user, item, num):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    item = item.lower().strip()
    if not item in existing_items:
        return f"Item {item} do not exists."
    if not item in json_data["users"][user]["growing_speed"]:
        return f"You cannot plant {item}."
    if not has_item(user, "hoe", 1):
        return f"You do not have a hoe."
    if not has_item(user, item, num):
        return f"You do not have {num} {item}."
    if len(json_data["users"][user]["farm_items"])+num > json_data["users"][user]["farm_size"]:
        return """You need a bigger farm to plant so many seeds.
Try to get a deed and use it, so you will get more fields."""
    out = ""
    for i in range(num):
        time = dt.datetime.now()
        timestr = f"{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}"
        growspeed = json_data["users"][user]["growing_speed"][item]+random.randint(-5, 5)
        data = {"item": item, "stat": 0, "time": timestr,
        "growing_speed": growspeed}
        json_data["users"][user]["farm_items"].append(data)
        del_items(user, item, 1)
        out += f""" - {item} x{num}
   It will take ~{json_data["users"][user]["growing_speed"][item]}min to grow.\n"""
    if random.randint(1, 100) == 1:
        out += "But you broke your hoe !"
        del_items(user, "hoe", 1)
    save_db()
    return f"""##### FARM #####
You planted :
{out}
"""

def do_farm_harvest(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    update_farm_state(user)
    to_del = []
    out = ""
    for i, data in enumerate(json_data["users"][user]["farm_items"]):
        if data["stat"]:
            item = data["item"]
            real_item = farm_out[item]
            amount_range = farm_amount[item]
            amount = random.randint(amount_range[0], amount_range[1])
            seeds_amount = random.randint(1, 4)
            out += f" - {real_item} x{amount} and {item} x{seeds_amount}\n"
            add_items(user, real_item, amount)
            add_items(user, item, seeds_amount)
            to_del.append(i)
    for n, i in enumerate(to_del):
        try:
            del json_data["users"][user]["farm_items"][i - n]
        except:
            out += "Ow there was a little error. Please report it to the developper.\n"
    if out == "": out = "Nothing."
    save_db()
    return f"""##### FARM #####
You harvested :
{out}
"""

##################### CRAFTING #####################

def do_craft_craft(user, item, num):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    item = item.lower().strip()
    if not item in existing_items:
        return f"Item {item} do not exists !"
    if not item in craftings:
        return f"You cannot craft {item}."
    for a in range(num):
        for i, n in craftings[item]["recipe"].items():
            if not has_item(user, i, n):
                return f"You need to have {i} x{n} to craft one {item}."
    for a in range(num):
        for i, n in craftings[item]["recipe"].items():
            del_items(user, i, n)
        add_items(user, item, craftings[item]["amount"])
    save_db()
    return f"You crafted {item} x{num}"

def do_craft_see(user):
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    out = ""
    for i in craftings:
        amount = craftings[i]["amount"]
        out += f"Item {i} x{amount}\n"
        for i, n in craftings[i]["recipe"].items():
            out += f" - {i} x{n}\n"
        out += "\n"
    return f"""##### CRAFTINGS #####
{out}
"""
