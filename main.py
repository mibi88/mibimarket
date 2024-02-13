import interactions
from interactions import slash_command, slash_option, component_callback
from lib import *
from math import *
from bot_token import *

bot = interactions.Client(token=BOT_TOKEN)

calls = {}

chiptune_links = [
    "https://www.youtube.com/watch?v=Hj3W6nthrKU",
    "https://www.youtube.com/watch?v=GLMhBE99byM",
    "https://www.youtube.com/watch?v=LUJNH_36GjQ",
    "https://www.youtube.com/watch?v=ByKCPbScgsU",
    "https://www.youtube.com/watch?v=qrtt7mgwCTw",
    "https://www.youtube.com/watch?v=miu4xLcnW8c",
    "https://www.youtube.com/watch?v=Bpy59q0ddfo",
    "https://www.youtube.com/watch?v=HMP18fU4Cms",
    "https://www.youtube.com/watch?v=ULbnOsLojA8",
    "https://www.youtube.com/watch?v=v-AgYsawdAc",
    "https://www.youtube.com/watch?v=EMM9CV1SjF4",
    "https://www.youtube.com/watch?v=VGXTBeRwDdc",
    "https://www.youtube.com/watch?v=FSKtNeBUO1E",
    "https://www.youtube.com/watch?v=EcTPUoFUN3I"
]

@slash_command(
    name="chiptune",
    description="Get a link to some cool chiptune.",
)

async def chiptune(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    out = f"""Some chiptune (or sometimes 16-bit music) :
{random.choice(chiptune_links)}"""
    await ctx.send(f"```{out}```")

@slash_command(
    name="about",
    description="About this bot."
)

async def about(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = about_this_bot(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### MOVE BUTTONS #####################

LIMIT = 1000
cmd_data = {}

def dtext(text, start):
    # Get how many lines I can send
    n = 0
    for c in text[start:start+LIMIT]:
        if c == '\n': n += 1
    # Get how many lines I will skip
    s = 0
    for c in text[:start]:
        if c == '\n': s += 1
    # The part of text that I will show.
    ntext = ""
    for i in text.split('\n')[s:s+n]:
        ntext += i+'\n'
    return ntext, len(ntext)

leftb = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="<",
    custom_id="leftb"
)

rightb = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=">",
    custom_id="rightb"
)

@component_callback("leftb")
async def button_left(ctx):
    if not f"{ctx.message.id}" in cmd_data:
        await ctx.send("```Ow, I do not remember what I wrote there ...```", ephemeral = True)
    else:
        idstr = f"{ctx.message.id}"
        data = cmd_data[idstr]
        if data[0]>0:
            data[0] -= 1
            out, n = dtext(data[2], data[0]*LIMIT)
            if data[0] <= 0:
                message = await ctx.send(f"```{out}```", components = [rightb])
            else:
                message = await ctx.send(f"```{out}```", components = [leftb, rightb])
            del cmd_data[idstr]
            cmd_data[f"{message.id}"] = data
        else:
            await ctx.send("```You are already at the start of the text.```", ephemeral = True)

@component_callback("rightb")
async def button_right(ctx):
    if not f"{ctx.message.id}" in cmd_data:
        await ctx.send("```Ow, I do not remember what I wrote there ...```", ephemeral = True)
    else:
        idstr = f"{ctx.message.id}"
        data = cmd_data[idstr]
        if data[0]<data[1]-1:
            data[0] += 1
            out, n = dtext(data[2], data[0]*LIMIT)
            if data[0] >= data[1]-1:
                message = await ctx.send(f"```{out}```", components = [leftb])
            else:
                message = await ctx.send(f"```{out}```", components = [leftb, rightb])
            del cmd_data[idstr]
            cmd_data[f"{message.id}"] = data
        else:
            await ctx.send("```You are already at the end of the text.```", ephemeral = True)

##################### PROFILE #####################

@slash_command(
    name="profile",
    description="See a profile."
)
@slash_option(
    name="user",
    description="Which profile I will show",
    opt_type=interactions.OptionType.USER,
    required=False,
)

async def profile(ctx: interactions.SlashContext, user: str = None):
    if user == None: user = f"{ctx.user.id}"
    else: user = f"{user.id}"
    profile = get_profile(user)
    # Displaying
    if len(profile) > LIMIT:
        ntext, n = dtext(profile, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(profile)/LIMIT), profile]
    else: await ctx.send(f"```{profile}```")

##################### BASIC ACTIONS #####################

@slash_command(
    name="fish",
    description="Fish some fish."
)

async def fish(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_fish(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="dig",
    description="Dig in the ground to find some items."
)

async def dig(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_dig(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="shop_sell",
    description="Sell items to get some coins."
)
@slash_option(
    name="item",
    description="Which item you want to sell",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="amount",
    description="How many items you want to sell",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def shop_sell(ctx: interactions.SlashContext, item: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_sell(user, item, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="shop_buy",
    description="Buy some items."
)

@slash_option(
    name="item",
    description="Which item you want to buy",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="amount",
    description="How many items you want to buy",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def shop_buy(ctx: interactions.SlashContext, item: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_buy(user, item, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="shop_view",
    description="See what is in the shop."
)

async def shop_view(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_shop_see(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="dive",
    description="Dive in the sea to find some items."
)

async def dive(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_dive(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="hunt",
    description="Hunt some animals in the woods."
)

async def hunt(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_hunt(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="scratch",
    description="Scratch a ticket and see what you won."
)

async def scratch(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_scratch(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="deposit",
    description="Deposit some coins on your bank account."
)

@slash_option(
    name="num",
    description="How many coins do you want to deposit.",
    opt_type=interactions.OptionType.INTEGER,
    required=True
)

async def deposit(ctx: interactions.SlashContext, num: int):
    user = f"{ctx.user.id}"
    out = do_deposit(user, num)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="withdraw",
    description="withdraw some coins from your bank account."
)

@slash_option(
    name="num",
    description="How many coins do you want to withdraw.",
    opt_type=interactions.OptionType.INTEGER,
    required=True
)

async def withdraw(ctx: interactions.SlashContext, num: int):
    user = f"{ctx.user.id}"
    out = do_withdraw(user, num)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="use",
    description="Use an item."
)

@slash_option(
    name="item",
    description="Which item do you want to use.",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="num",
    description="How many items do you want to use.",
    opt_type=interactions.OptionType.INTEGER,
    required=False,
)

async def use(ctx: interactions.SlashContext, item: str, num: int = 1):
    user = f"{ctx.user.id}"
    out = do_use(user, item, num)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="rob",
    description="Rob someone."
)

@slash_option(
    name="user",
    description="The user you want to rob.",
    opt_type=interactions.OptionType.USER,
    required=True,
)
@slash_option(
    name="beer",
    description="Set this to true if you want to drink some beer before.",
    opt_type=interactions.OptionType.BOOLEAN,
    required=False,
)

async def rob(ctx: interactions.SlashContext, user: str, beer: bool = False):
    user_st = f"{ctx.user.id}"
    user = f"{user.id}"
    out = do_rob(user_st, user, beer)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### MARKET #####################

@slash_command(
    name="market_add",
    description="Sell or buy items to get some coins/items."
)

@slash_option(
    name="opt_type",
    description="The opt_type of your post 'sell' or 'buy'.",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="item",
    description="Which item you want to buy/sell",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="amount",
    description="How many items you want to buy/sell",
    opt_type=interactions.OptionType.INTEGER,
    required=True
)
@slash_option(
    name="for_item",
    description="For which item? Set this arg. to 'coins' if you want to get coins.",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="for_amount",
    description="For how many items (or coins)?",
    opt_type=interactions.OptionType.INTEGER,
    required=True
)

async def market_add(ctx: interactions.SlashContext, opt_type: str,
item: str, for_item: str, amount: int = 1, for_amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_market_add(user, opt_type, item, amount, for_item, for_amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="market_remove",
    description="Remove an offer from the market."
)

@slash_option(
    name="id",
    description="Id of the offer.",
    opt_type=interactions.OptionType.INTEGER,
    required=True
)

async def market_remove(ctx: interactions.SlashContext, id: int):
    user = f"{ctx.user.id}"
    out = do_market_remove(user, id)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="market_accept",
    description="Accept an offer from the market."
)

@slash_option(
    name="id",
    description="Id of the offer.",
    opt_type=interactions.OptionType.INTEGER,
    required=True
)
@slash_option(
    name="amount",
    description="How many items do you want to buy/sell.",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def market_accept(ctx: interactions.SlashContext, id: int, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_market_accept(user, id, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="market_view",
    description="Search an offer in the market."
)

@slash_option(
    name="item",
    description="The item that you want to buy/sell.",
    opt_type=interactions.OptionType.STRING,
    required=True
)

async def market_view(ctx: interactions.SlashContext, item: str):
    user = f"{ctx.user.id}"
    out = do_market_see(user, item)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### ECONOMY #####################

@slash_command(
    name="economy_info",
    description="Economy infos."
)

async def economy_info(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = view_stat(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="price",
    description="Get the price of an item."
)

@slash_option(
    name="item",
    description="The item that you want to buy/sell.",
    opt_type=interactions.OptionType.STRING,
    required=True
)

async def price(ctx: interactions.SlashContext, item: str):
    user = f"{ctx.user.id}"
    out = view_price(user, item)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### FARMING #####################

@slash_command(
    name="farm_plant",
    description="Plant some seeds."
)

@slash_option(
    name="item",
    description="Which item do you want to plant.",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="num",
    description="How many items do you want to plant.",
    opt_type=interactions.OptionType.INTEGER,
    required=False,
)

async def farm_plant(ctx: interactions.SlashContext, item: str, num: int = 1):
    user = f"{ctx.user.id}"
    out = do_farm_plant(user, item, num)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="farm_harvest",
    description="Harvest your crops."
)

async def farm_harvest(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_farm_harvest(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="farm_view",
    description="View what's growing in your farm."
)

async def farm_view(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_farm_see(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### CRAFTING #####################

@slash_command(
    name="crafting_craft",
    description="Craft some items."
)

@slash_option(
    name="item",
    description="Which item you want to craft",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="amount",
    description="How many items you want to craft",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def crafting_craft(ctx: interactions.SlashContext, item: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_craft_craft(user, item, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="crafting_view",
    description="See what you can craft."
)

async def crafting_view(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_craft_see(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### PETS #####################

@slash_command(
    name="pets_view",
    description="See which pets you have."
)

async def pets_view(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_pets_see(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="pets_adopt",
    description="Adopt some pets."
)

@slash_option(
    name="pet",
    description="Which pet you want to adopt",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="name",
    description="The name of your pet",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="amount",
    description="How many pets do you want to adopt",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def pets_adopt(ctx: interactions.SlashContext, pet: str, name: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_pets_adopt(user, pet, name, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="pets_care",
    description="Take care of a pet."
)

@slash_option(
    name="id",
    description="The id of your pet that you can get with /pets_view",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="category",
    description="Do you want to give him food, wash hin or play with him?",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="amount",
    description="How much do you want to do it",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def pets_care(ctx: interactions.SlashContext, id: str, category: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_pets_care(user, id, category, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

@slash_command(
    name="pets_upgrade",
    description="Make your pet more powerful."
)

@slash_option(
    name="id",
    description="The id of your pet that you can get with /pets_view",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@slash_option(
    name="category",
    description="What do you want to improve?",
    opt_type=interactions.OptionType.STRING,
    required=True
)
@slash_option(
    name="amount",
    description="How much do you want to do it",
    opt_type=interactions.OptionType.INTEGER,
    required=False
)

async def pets_upgrade(ctx: interactions.SlashContext, id: str, category: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_pets_upgrade(user, id, category, amount)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

##################### EXPLORING #####################

@slash_command(
    name="explore",
    description="Go on a trip to get some items."
)

async def explore(ctx: interactions.SlashContext):
    user = f"{ctx.user.id}"
    out = do_explore(user)
    # Displaying
    if len(out) > LIMIT:
        ntext, n = dtext(out, 0)
        message = await ctx.send(f"```{ntext}```", components = [rightb])
        cmd_data[f"{message.id}"] = [0, ceil(len(out)/LIMIT), out]
    else: await ctx.send(f"```{out}```")

bot.start()
