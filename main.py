import discord
from discord.ext import commands
from config import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)



@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command(pass_context=True)
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
         await ctx.channel.purge(limit=(int(amount) + 1))
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command(pass_context=True)
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
         await ctx.channel.purge(limit=(int(amount) + 1))

@bot.command()
async def create(ctx):
    if ctx.channel.id in games:
        await ctx.send("A game is already active in this channel!")
    else:
        games[ctx.channel.id] = {
            "players":[],
            "team 1": [], 
            "team 2":[],
            "hands": [],
            "state": "lobby", 
            "scores": [0, 0]}
        await ctx.send("Spades game created! Use `!join` to join.")

@bot.command()
async def join(ctx):
    game = games.get(ctx.channel.id)
    if not game:
        await ctx.send("No active game in this channel.")
    elif len(game["players"]) >= 4:
        await ctx.send("The game is full!")
    else:
        game["players"].append(ctx.author)
        await ctx.send(f"{ctx.author} has joined the game!")

#commands to join a team for scoring and bidding purpsoses
@bot.command()
async def team1(ctx):
    game = games.get(ctx.channel.id)
    if not game:
            await ctx.send("No active game in this channel.")
    elif ctx.author in game["players"]:
        game["team 1"].append(ctx.author)
        await ctx.send(f"{ctx.author}has joined team 1")

@bot.command()
async def team2(ctx):
    game = games.get(ctx.channel.id)
    if not game:
            await ctx.send("No active game in this channel.")
    elif ctx.author in game["players"]:
        game["team 2"].append(ctx.author)
        await ctx.send(f"{ctx.author}has joined team 2")
    

@bot.command()
async def deal(ctx):
    game = games.get(ctx.channel.id)
    deck = create_deck
    hands = deal(deck)
    
    if len(game["players"]) == 4:
        hands = game["hands"]
        for i, player in enumerate(game["players"]):
            hand = hands[i]

            view = HandView(player, hand)
            await ctx.send(f"{player.display_name}, click the button below to see your hand.", view=view)
    elif len(game["players"]) != 4:
        await ctx.send("Exactly 4 players are required to start.")
    else:
        game["state"] = "playing"
        await ctx.send("All players are in! Hands have been dealt. Check your DMs for your cards.")
        
    

#game start command
@bot.command()
async def round(ctx):
    """Start the bidding phase."""
    game = games.get(ctx.channel.id)
    if not game:
        await ctx.send("No active game in this channel.")
        return
    if len(game["players"]) != 4:
        await ctx.send("Exactly 4 players are required to start.")
        return
    
    game["state"] = "bidding"
    game["bids"] = {player: None for player in game["players"]}
    await ctx.send("Bidding phase started! Use `!bid <number>` to place your bid.")

#bidding commands 
@bot.command()
async def bid(ctx, amount: int):
    """Allow a player to place their bid."""
    game = games.get(ctx.channel.id)
    if not game or game["state"] != "bidding":
        await ctx.send("No active bidding phase.")
        return
    if ctx.author not in game["players"]:
        await ctx.send("You are not part of this game.")
        return
    
    if amount < 0 or amount > 13:
        await ctx.send("Bids must be between 0 and 13.")
        return

    game["bids"][ctx.author] = amount
    await ctx.send(f"{ctx.author.display_name} bid {amount}.")

    if all(bid is not None for bid in game["bids"].values()):
        await ctx.send("Bidding complete!")
        game["state"] = "playing"  # Move to next phase
