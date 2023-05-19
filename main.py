import interactions
from lib import *

bot = interactions.Client(token="token")

calls = {}

chiptune_links = [
    "https://www.youtube.com/watch?v=Hj3W6nthrKU",
    "https://www.youtube.com/watch?v=GLMhBE99byM",
    "https://www.youtube.com/watch?v=LUJNH_36GjQ",
    "https://www.youtube.com/watch?v=ByKCPbScgsU",
    "https://www.youtube.com/watch?v=qrtt7mgwCTw"
]

@bot.command(
    name="chiptune",
    description="Get a link to some cool chiptune.",
    default_scope=False
)

async def chiptune(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    if not user in json_data["users"]:
        create_user(user)
        save_db()
    out = f"""Some chiptune (or sometimes 16-bit music) :
{random.choice(chiptune_links)}"""
    await ctx.send(f"```{out}```")

@bot.command(
    name="about",
    description="About this bot.",
    default_scope=False
)

async def about(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = about_this_bot(user)
    await ctx.send(f"```{out[:1000]}```")
    await ctx.send(f"```{out[1000:]}```")

##################### PROFILE #####################

@bot.command(
    name="profile",
    description="See a profile.",
    options = [
        interactions.Option(
            name="user",
            description="Which profile I will show",
            type=interactions.OptionType.USER,
            required=False,
        ),
    ],
    default_scope=False
)

async def profile(ctx: interactions.CommandContext, user: str = None):
    if user == None: user = f"{ctx.user.id}"
    else: user = f"{user.id}"
    profile = get_profile(user)
    await ctx.send(f"```{profile}```")

##################### BASIC ACTIONS #####################

@bot.command(
    name="fish",
    description="Fish some fish.",
    default_scope=False
)

async def fish(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_fish(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="dig",
    description="Dig in the ground to find some items.",
    default_scope=False
)

async def dig(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_dig(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="shop_sell",
    description="Sell items to get some coins.",
    options = [
        interactions.Option(
            name="item",
            description="Which item you want to sell",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="amount",
            description="How many items you want to sell",
            type=interactions.OptionType.INTEGER,
            required=False
        )
    ],
    default_scope=False
)

async def shop_sell(ctx: interactions.CommandContext, item: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_sell(user, item, amount)
    await ctx.send(f"```{out}```")

@bot.command(
    name="shop_buy",
    description="Sell items to get some coins.",
    options = [
        interactions.Option(
            name="item",
            description="Which item you want to sell",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="amount",
            description="How many items you want to sell",
            type=interactions.OptionType.INTEGER,
            required=False
        )
    ],
    default_scope=False
)

async def shop_buy(ctx: interactions.CommandContext, item: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_buy(user, item, amount)
    await ctx.send(f"```{out}```")

@bot.command(
    name="shop_view",
    description="See what is in the shop.",
    default_scope=False
)

async def shop_view(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_shop_see(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="dive",
    description="Dive in the sea to find some items.",
    default_scope=False
)

async def dive(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_dive(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="scratch",
    description="Scratch a ticket and see what you won.",
    default_scope=False
)

async def scratch(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_scratch(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="deposit",
    description="Deposit some coins on your bank account.",
    options = [
        interactions.Option(
            name="num",
            description="How many coins do you want to deposit.",
            type=interactions.OptionType.INTEGER,
            required=True,
        )
    ],
    default_scope=False
)

async def deposit(ctx: interactions.CommandContext, num: int):
    user = f"{ctx.user.id}"
    out = do_deposit(user, num)
    await ctx.send(f"```{out}```")

@bot.command(
    name="withdraw",
    description="withdraw some coins from your bank account.",
    options = [
        interactions.Option(
            name="num",
            description="How many coins do you want to withdraw.",
            type=interactions.OptionType.INTEGER,
            required=True,
        )
    ],
    default_scope=False
)

async def withdraw(ctx: interactions.CommandContext, num: int):
    user = f"{ctx.user.id}"
    out = do_withdraw(user, num)
    await ctx.send(f"```{out}```")

@bot.command(
    name="use",
    description="Use an item.",
    options = [
        interactions.Option(
            name="item",
            description="Which item do you want to use.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="num",
            description="How many items do you want to use.",
            type=interactions.OptionType.INTEGER,
            required=False,
        )
    ],
    default_scope=False
)

async def use(ctx: interactions.CommandContext, item: str, num: int = 1):
    user = f"{ctx.user.id}"
    out = do_use(user, item, num)
    await ctx.send(f"```{out}```")

@bot.command(
    name="rob",
    description="Rob someone.",
    options = [
        interactions.Option(
            name="user",
            description="The user you want to rob.",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="beer",
            description="Set this to true if you want to drink some beer before.",
            type=interactions.OptionType.BOOLEAN,
            required=False,
        )
    ],
    default_scope=False
)

async def rob(ctx: interactions.CommandContext, user: str, beer: bool = False):
    user_st = f"{ctx.user.id}"
    user = f"{user.id}"
    out = do_rob(user_st, user, beer)
    await ctx.send(f"```{out}```")

##################### MARKET #####################

@bot.command(
    name="market_add",
    description="Sell or buy items to get some coins/items.",
    options = [
        interactions.Option(
            name="type",
            description="The type of your post 'sell' or 'buy'.",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="item",
            description="Which item you want to buy/sell",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="amount",
            description="How many items you want to buy/sell",
            type=interactions.OptionType.INTEGER,
            required=True
        ),
        interactions.Option(
            name="for_item",
            description="For which item ? Set this arg. to 'coins' if you want to get coins.",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="for_amount",
            description="For how many items (or coins) ?",
            type=interactions.OptionType.INTEGER,
            required=True
        )
    ],
    default_scope=False
)

async def market_add(ctx: interactions.CommandContext, type: str,
item: str, for_item: str, amount: int = 1, for_amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_market_add(user, type, item, amount, for_item, for_amount)
    await ctx.send(f"```{out}```")

@bot.command(
    name="market_remove",
    description="Remove an offer from the market.",
    options = [
        interactions.Option(
            name="id",
            description="Id of the offer.",
            type=interactions.OptionType.INTEGER,
            required=True
        )
    ],
    default_scope=False
)

async def market_remove(ctx: interactions.CommandContext, id: int):
    user = f"{ctx.user.id}"
    out = do_market_remove(user, id)
    await ctx.send(f"```{out}```")

@bot.command(
    name="market_accept",
    description="Accept an offer from the market.",
    options = [
        interactions.Option(
            name="id",
            description="Id of the offer.",
            type=interactions.OptionType.INTEGER,
            required=True
        ),
        interactions.Option(
            name="amount",
            description="How many items do you want to buy/sell.",
            type=interactions.OptionType.INTEGER,
            required=False
        )
    ],
    default_scope=False
)

async def market_accept(ctx: interactions.CommandContext, id: int, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_market_accept(user, id, amount)
    await ctx.send(f"```{out}```")

@bot.command(
    name="market_view",
    description="Search an offer in the market.",
    options = [
        interactions.Option(
            name="item",
            description="The item that you want to buy/sell.",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    default_scope=False
)

async def market_view(ctx: interactions.CommandContext, item: str):
    user = f"{ctx.user.id}"
    out = do_market_see(user, item)
    await ctx.send(f"```{out}```")

##################### ECONOMY #####################

@bot.command(
    name="economy_info",
    description="Economy infos.",
    default_scope=False
)

async def economy_info(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = view_stat(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="price",
    description="Get the price of an item.",
    options = [
        interactions.Option(
            name="item",
            description="The item that you want to buy/sell.",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    default_scope=False
)

async def price(ctx: interactions.CommandContext, item: str):
    user = f"{ctx.user.id}"
    out = view_price(user, item)
    await ctx.send(f"```{out}```")

##################### FARMING #####################

@bot.command(
    name="farm_plant",
    description="Plant some seeds.",
    options = [
        interactions.Option(
            name="item",
            description="Which item do you want to plant.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="num",
            description="How many items do you want to plant.",
            type=interactions.OptionType.INTEGER,
            required=False,
        )
    ],
    default_scope=False
)

async def farm_plant(ctx: interactions.CommandContext, item: str, num: int = 1):
    user = f"{ctx.user.id}"
    out = do_farm_plant(user, item, num)
    await ctx.send(f"```{out}```")

@bot.command(
    name="farm_harvest",
    description="Harvest your crops.",
    default_scope=False
)

async def farm_harvest(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_farm_harvest(user)
    await ctx.send(f"```{out}```")

@bot.command(
    name="farm_view",
    description="View what's growing in your farm.",
    default_scope=False
)

async def farm_view(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_farm_see(user)
    await ctx.send(f"```{out}```")

##################### CRAFTING #####################

@bot.command(
    name="crafting_craft",
    description="Craft some items.",
    options = [
        interactions.Option(
            name="item",
            description="Which item you want to craft",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="amount",
            description="How many items you want to craft",
            type=interactions.OptionType.INTEGER,
            required=False
        )
    ],
    default_scope=False
)

async def crafting_craft(ctx: interactions.CommandContext, item: str, amount: int = 1):
    user = f"{ctx.user.id}"
    out = do_craft_craft(user, item, amount)
    await ctx.send(f"```{out}```")

@bot.command(
    name="crafting_view",
    description="See what you can craft.",
    default_scope=False
)

async def crafting_view(ctx: interactions.CommandContext):
    user = f"{ctx.user.id}"
    out = do_craft_see(user)
    await ctx.send(f"```{out}```")

bot.start()
