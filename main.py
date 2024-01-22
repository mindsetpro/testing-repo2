import discord
from discord.ext import commands
import random
import json
import os
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

# Load characters from the JSON file
with open('characters.json', 'r') as file:
    characters_data = json.load(file)

# Extract the 'data' key from the JSON
characters = characters_data.get('data', [])


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='rand')
async def random_character(ctx):
    try:
        if not characters:
            await ctx.send("Error: Characters list is empty.")
            return

        # Choose a random character
        selected_character = random.choice(characters)

        # Create an embed
        embed = discord.Embed(title=selected_character["name"], description=selected_character["appearance"], color=0x7289DA)
        embed.set_image(url=selected_character["image_url"])
        embed.add_field(name="Species", value=selected_character.get("species", "Unknown"), inline=True)
        embed.add_field(name="Birthday", value=selected_character.get("birthday", "Unknown"), inline=True)
        embed.add_field(name="Gender", value=selected_character.get("gender", "Unknown"), inline=True)
        
        # Check if 'age' field is available
        age = selected_character.get("age", [])
        if age:
            embed.add_field(name="Age", value=f"{age[0]} years", inline=True)
        else:
            embed.add_field(name="Age", value="Unknown", inline=True)

        embed.add_field(name="Status", value=selected_character.get("status", "Unknown"), inline=True)
        embed.add_field(name="Grade", value=selected_character.get("grade", "Unknown"), inline=True)

        # Truncate the "Personality" field to 1024 characters
        personality = selected_character.get("personality", "Unknown")
        personality = personality[:1021] + '...' if len(personality) > 1024 else personality
        embed.add_field(name="Personality", value=personality, inline=False)

        # Send the embed
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        raise

@bot.command(name='lookup')
async def lookup_character(ctx, character_name: str):
    try:
        if not characters:
            await ctx.send("Error: Characters list is empty.")
            return

        # Find the character by name
        found_characters = [char for char in characters if char["name"].lower() == character_name.lower()]

        if not found_characters:
            await ctx.send(f"Character '{character_name}' not found.")
            return

        found_character = found_characters[0]

        # Create an embed
        embed = discord.Embed(title=found_character["name"], description=found_character["appearance"], color=0x7289DA)
        embed.set_image(url=found_character["image_url"])
        embed.add_field(name="Species", value=found_character.get("species", "Unknown"), inline=True)
        embed.add_field(name="Birthday", value=found_character.get("birthday", "Unknown"), inline=True)
        embed.add_field(name="Gender", value=found_character.get("gender", "Unknown"), inline=True)
        
        # Check if 'age' field is available
        age = found_character.get("age", [])
        if age:
            embed.add_field(name="Age", value=f"{age[0]} years", inline=True)
        else:
            embed.add_field(name="Age", value="Unknown", inline=True)

        embed.add_field(name="Status", value=found_character.get("status", "Unknown"), inline=True)
        embed.add_field(name="Grade", value=found_character.get("grade", "Unknown"), inline=True)

        # Truncate the "Personality" field to 1024 characters
        personality = found_character.get("personality", "Unknown")
        personality = personality[:1021] + '...' if len(personality) > 1024 else personality
        embed.add_field(name="Personality", value=personality, inline=False)

        # Send the embed
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        raise

@bot.command(name='title')
async def title_command(ctx, title_name):
    url = "https://gamepress.gg/dblegends/title-plates"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_elements = soup.find_all('a', hreflang="en")

        for title_element in title_elements:
            if title_name.lower() in title_element.text.lower():
                title_url = "https://gamepress.gg" + title_element['href']
                title_response = requests.get(title_url)
                
                if title_response.status_code == 200:
                    title_soup = BeautifulSoup(title_response.text, 'html.parser')
                    title_info = title_soup.find('div', class_='title-plate-info')
                    title_image = title_soup.find('div', class_='title-plate-image').find('img')['src']

                    embed = discord.Embed(title=title_element.text, description=title_info.text.strip(), color=0x00ff00)
                    embed.set_image(url=title_image)
                    await ctx.send(embed=embed)
                    return

    await ctx.send(f"Title '{title_name}' not found.")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
