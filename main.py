import interactions
from lib import *

bot = interactions.Client(token="token")

calls = {}

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

bot.start()
