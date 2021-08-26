import webbrowser
from pprint import pprint
import json
from discord import Client
from discord.ext import commands
import discord
import requests
import aiohttp
import os
import base64
from cryptography.fernet import Fernet
import asyncpraw
from asyncpraw import Reddit
import time
import random
import logging
import httpx

client = httpx.AsyncClient()

class Moderation(commands.Cog):
    logging.basicConfig(filename="bot_logs.txt", filemode="a")

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ['OPENWEATHERMAP_TOKEN']

    @commands.command()
    async def members(self, ctx):
        for member in ctx.guild.members:
            await ctx.send(f"{member} is in this server! Here is their member id: {member.id}")
            logging.info(f"Member id got: {member.id}")


    @commands.command()
    async def add(self, ctx, left: int, right: int):
        await ctx.send(left + right)

    @commands.command()
    async def subtract(self, ctx, left: int, right: int):
        await ctx.send(left - right)

    @commands.command()
    async def multiply(self, ctx, left: int, right: int):
        await ctx.send(left * right)

    @commands.command()
    async def divide(self, ctx, left: int, right: int):
        await ctx.send(left / right)

    @commands.command(aliases=['wd'])
    async def whole_divide(self, ctx, left: int, right: int):
        await ctx.send(left // right)

    @commands.command()
    async def open(self, website: str):
        url = "https://" + website
        webbrowser.open_new_tab(url)

    @commands.command()
    async def search(self, keywords):
        url = f"https://www.google.com/search?q={keywords}"
        webbrowser.open_new_tab(url)

    # async def getWeather(self, weather_call):
    #     return requests.get(weather_call).json()

    @commands.command()
    async def weather(self, ctx, city_name: str):
        api_key = "bd2f8a8f8ed9058c8bd1aae2c45452cf"
        weather_call = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial"
        async with self.bot.session.get(weather_call) as response:
            weather_data = await response.json()
        temp = weather_data['main']['temp']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        embed = discord.Embed(title=f"Weather for {city_name}")
        embed.add_field(name=f"Average temperature for {city_name} today: ", value=f"The average temperature for {city_name} today is {temp} degrees fahrenheit.")
        embed.add_field(name=f"Lowest temperature for {city_name} today: ", value=f"The lowest temperature for {city_name} today is {temp_min} degrees fahrenheit.")
        embed.add_field(name=f"Highest temperature for {city_name} today: ", value=f"The highest temperature for {city_name} today is {temp_max} degrees fahrenheit.")
        embed.add_field(name=f"Humidity for {city_name} today: ", value=f"The humidity for {city_name} is {humidity}%.")
        embed.add_field(name=f"Wind speed for {city_name} today: ", value=f"The average wind speed for {city_name} today is {wind_speed} mph.")
        await ctx.send(embed=embed)
        logging.info(f"Weather returned for {city_name}.")

    @commands.command()
    async def python(self, ctx):
        await ctx.send('https://docs.python.org/3/tutorial/index.html')
        await ctx.send("Here are some great resources for learning python!")

    @commands.command()
    async def dictionary(self, ctx, word: str):
        full_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        async with self.bot.session.get(full_url) as response:
            word_description = await response.json()
            # print(type(response))
            # print(type(word_description))
            word_info = word_description[0]
        main_definition = word_info["meanings"][0]["definitions"][0]["definition"]
        part_of_speech = word_info["meanings"][0]["partOfSpeech"]
        usage_example = word_info["meanings"][0]["definitions"][0]["example"]

        # definitions = word_description['meanings'][0]['definitions'][0]['definition']
        # main_definition = definitions
        # partOfSpeech = word_description['meanings'][0]['partOfSpeech']
        # usage_example = word_description['meanings'][0]['definitions'][1]['example']

        embed = discord.Embed(name=f"Information about word: {word}")
        embed.add_field(name=f"Definition for {word}: ", value=f"{main_definition}")
        embed.add_field(name=f"Part of speech for {word}: ", value=f"The part of speech for '{word}' is {part_of_speech}.")
        embed.add_field(name=f"Usage example for {word}: ", value=f"{usage_example}")
        await ctx.send(embed=embed)


    @commands.command(aliases=['b64_encode'], help="This is a basic encoding command that will take a input from you, and encode it in base64 format!")
    async def my_b64_encode(self, ctx, phrase: str):
        bytes_phrase = str.encode(phrase)
        encoded_phrase = base64.b64encode(bytes_phrase)
        await ctx.send(encoded_phrase)

    @commands.command(aliases=['b64_decode'], help="This is a basic decoding command that will take a input in b64, and decode it for you!")
    async def my_b64_decode(self, ctx, phrase: str):
        bytes_phrase = str.encode(phrase)
        decoded_phrase = base64.b64decode(bytes_phrase)
        await ctx.send(decoded_phrase)

    @commands.command()
    async def check_servers(self, ctx, member: discord.Member):
        pass

    @commands.command()
    async def crypto(self, ctx):
        api_key = "5b479184-96f9-457a-83c6-c14993b1c191"
        base_url = "https://pro-api.coinmarketcap.com/cryptocurrency/exchange=USD"

    # @commands.command()
    # async def give_points(self, ctx, member: discord.Member):

    @commands.command()
    async def popular_reddit_python(self, ctx):
        reddit_client_info = asyncpraw.Reddit( # read only reddit instance
            client_id="r9-WSL281nWO_MTHIvBKLg",
            client_secret="ATAjyT2Qro7IPKsjRKp_wc5j4YFR_g",
            user_agent="discord reddit bot command parser",
        )

        # client = discord.Client()
        # await ctx.channel.send("Please enter the subreddit you would like to pull data from: ")
        # ask_subreddit = await client.wait_for("message")
        # await ctx.channel.send("Please enter the number of posts you would like to pull: ")
        # ask_times = await client.wait_for("message")
        user_subreddit = await reddit_client_info.subreddit("py"
                                                            "thon")
        async for submission in user_subreddit.hot(limit=1):
            # await ctx.channel.send(submission.title)
            # await ctx.channel.send(submission.score)
            # await ctx.channel.send(submission.id)
            # await ctx.channel.send(submission.url)
            embed = discord.Embed(name=f"Most popular posts from r/Python")
            embed.add_field(name="Popular submission found: ", value=f"{submission.title}")
            embed.add_field(name="Score of submission: ", value=f"{submission.score}")
            embed.add_field(name="Submission id: ", value=f"{submission.id}")
            embed.add_field(name="Submission url: ", value=f"{submission.url}")
            time.sleep(10)
            await ctx.send(embed=embed)

    @commands.command()
    async def warn(self, ctx, member: discord.Member, reason):
        guild = ctx.Guild()
        guild.warn(member)
        embed = discord.Embed(name=f"Warning applied to {member.display_name}")
        embed.add_field(name="Reason for warning: ", value=f"{reason.title()}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["roll"])
    async def roll_dice(self, ctx, user_range: int):
        rolled_number = random.randint(0, user_range)
        embed = discord.Embed(name="Dice rolling!")
        embed.add_field(name="Rolled number: ", value=f"You rolled a {rolled_number}")
        await ctx.send(embed=embed)

    @commands.command()
    async def get_guilds(self, ctx):
        client = discord.Client
        async for guild in client.fetch_guilds(limit=5):
            await ctx.send(guild.name)

    @commands.command(aliases=["eval_equation", "ee", "EE"])
    async def evaluate_equation(self, ctx, equation):
        evaluated_equation = eval(equation)
        await ctx.send(evaluated_equation)

    @commands.command(aliases=["github_user"])
    async def get_github_user(self, ctx, user):
        user_data = (await client.get(f"https://api.github.com/users/{user}")).json()
        username = user_data['login']
        user_id = user_data['id']
        user_html_url = user_data['html_url']
        embed = discord.Embed(name=f"{user}")
        embed.add_field(name=f"Username:", value=f"{username}")
        embed.add_field(name="User ID", value=f"{user_id}")
        embed.add_field(name="User profile url: ", value=f"{user_html_url}")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Moderation(bot))
