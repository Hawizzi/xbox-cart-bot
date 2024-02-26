import re
import discord
import requests
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_data = {}

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
 
    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1181194926902497300))
        self.synced = True
        print("Bot is online")

bot = abot()

tree = app_commands.CommandTree(bot)

def extract_header(data_string):
    extracted_values = {}
    headers = {}

    keys_to_extract = ["authorization", "ms-cv", "x-authorization-muid", "x-ms-vector-id", "x-validation-field-1","riskSessionId"]

    for key in keys_to_extract:
        pattern = rf'"{key}":\s*"(.*?)"'
        match = re.search(pattern, data_string)
        if match:
            extracted_values[key] = match.group(1)

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": extracted_values.get("authorization"),
        "ms-cv": extracted_values.get("ms-cv"),
        "sec-ch-ua": "\"Not A(Brand\";v=\"99\",\"Google Chrome\";v=\"121\",\"Chromium\";v=\"121\"",
        "x-authorization-muid": extracted_values.get("x-authorization-muid"),
        "x-ms-vector-id": extracted_values.get("x-ms-vector-id"),
        "x-validation-field-1": extracted_values.get("x-validation-field-1"),
        "riskSessionId": extracted_values.get("riskSessionId"),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "content-type": "application/json",
        "content-length": "340",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "referer": "https://www.xbox.com/",
        "origin": "https://cart.production.store-web.dynamics.com"
    }

    return headers

def generate_combination_and_items(quantity):
    values = [2000, 1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 900, 800, 700, 600, 500, 400, 300, 200, 100]

    def find_closest_combination(target, current_combination, remaining_values):
        closest_combination = current_combination
        closest_difference = abs(target - sum(current_combination))

        for value in remaining_values:
            new_combination = current_combination + [value]
            new_difference = abs(target - sum(new_combination))

            if new_difference < closest_difference and sum(new_combination) <= target:
                closest_combination = new_combination
                closest_difference = new_difference

        return closest_combination

    remaining_quantity = quantity
    selected_values = []

    for value in values:
        if remaining_quantity >= value:
            selected_values.append(value)
            remaining_quantity -= value

    if remaining_quantity != 0:
        print("No exact combination found. Remaining quantity:", remaining_quantity)
        selected_values = find_closest_combination(quantity, selected_values, values)

    id_mapping = {
        2000: {"productId": "9NBKVWFCXFDJ", "availabilityId": "9NBKVWFCXFDJ"},
        1900: {"productId": "9NLLNCGKW2BW", "availabilityId": "9NLLNCGKW2BW"},
        1800: {"productId": "9P0462L70KQQ", "availabilityId": "9P0462L70KQQ"},
        1700: {"productId": "9P15QMWK2KQC", "availabilityId": "9P15QMWK2KQC"},
        1600: {"productId": "9PFDDRKM07C4", "availabilityId": "9PFDDRKM07C4"},
        1500: {"productId": "9PLP33H5GSD3", "availabilityId": "9PLP33H5GSD3"},
        1400: {"productId": "9P5WH95SBC1Q", "availabilityId": "9P5WH95SBC1Q"},
        1300: {"productId": "9P1M9BGF0FSG", "availabilityId": "9P1M9BGF0FSG"},
        1200: {"productId": "9P8FDFWTP9MJ", "availabilityId": "9P8FDFWTP9MJ"},
        1100: {"productId": "9P8K4RJ5XV39", "availabilityId": "9P8K4RJ5XV39"},
        900: {"productId": "9N6LNP106BP3", "availabilityId": "9N6LNP106BP3"},
        800: {"productId": "9PDF7RTW3HN6", "availabilityId": "9PDF7RTW3HN6"},
        700: {"productId": "9NCQ0LZSXNBK", "availabilityId": "9NCQ0LZSXNBK"},
        600: {"productId": "9NP8DJCQKQQG", "availabilityId": "9NP8DJCQKQQG"},
        500: {"productId": "9PD4G3T4LP6P", "availabilityId": "9PD4G3T4LP6P"},
        400: {"productId": "9N9J6BBHXRK4", "availabilityId": "9N9J6BBHXRK4"},
        300: {"productId": "9MV7N0D707L5", "availabilityId": "9MV7N0D707L5"},
        200: {"productId": "9PD1G688WD0V", "availabilityId": "9PD1G688WD0V"},
        100: {"productId": "9NRFP18VHR2F", "availabilityId": "9NRFP18VHR2F"}
    }

    items = []
    for value in selected_values:
        product_id = id_mapping[value]["productId"]
        availability_id = id_mapping[value]["availabilityId"]

        items.append({
            "productId": product_id,
            "skuId": "0010",
            "availabilityId": availability_id,
            "quantity": 1,
            "campaignId": "xboxcomct"
        })

    return items

class cartbutton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Open cart", url="https://www.xbox.com/es-AR/cart"))


@tree.command(name="cart", guild=discord.Object(id=1181194926902497300))
@app_commands.checks.has_any_role("cart")
async def test_command(interaction: discord.Interaction, fetch_values: str, quantity: app_commands.Range[int, 100, 20000]):
    await interaction.response.send_message("Starting to add vbucks", ephemeral=True)

    headers = extract_header(fetch_values)

    if quantity > 20000:
        await interaction.response.send_message("Quantity cannot be greater than 20000.", ephemeral=True)
        return
    items = generate_combination_and_items(quantity)

    url = "https://cart.production.store-web.dynamics.com/cart/v1.0/cart/loadCart?cartType=consumer&appId=XboxWeb"
    payload = {
        "market": "AR",
        "locale": "es-AR",
        "riskSessionId": "b98a7cd5-6a00-4a9b-8176-2345bdc6100d",
        "catalogClientType": "storeWeb",
        "clientContext": {"client": "XboxCom", "deviceFamily": "web"},
        "friendlyName": "cart-AR",
        "itemsToAdd": {"items": items}
    }

    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        embed = discord.Embed(title=f"Success!", description=f"{quantity} V-Bucks added to cart!", color=discord.Color.blurple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/823937235186352128/1209834803776585828/1182702554665201734.png?ex=65e85d76&is=65d5e876&hm=f25b2cd866e64d520e8216185575959ab5e77e0722b0a7dd4a0e3ad501c1d6ed&")
        embed.set_footer(text=f"Cart bot used by: {interaction.user.name}")
        await interaction.followup.send(embed=embed, view=cartbutton())
    else:
       await interaction.followup.send(f"Failed with status code {response.status_code}. please try again by removing all stuff from cart and then taking new fetch", ephemeral=True)


bot.run("token here")
