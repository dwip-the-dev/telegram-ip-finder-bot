import requests
import html
import subprocess
import socket
import whois
import dns.resolver
import datetime
import asyncio
from picarta import Picarta
import aiohttp
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# API KEYS
TOKEN = "7542368975:**....**"  # Replace with your bot token
NUMVERIFY_API_KEY = "7893c25c**....**"  # Replace with your Numverify API key
LOG_CHANNEL_ID = "-100**...***"  # Replace with your log channel ID
OPENCAGE_API_KEY = "4585d**...**"
# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Logging Function
async def log_command(user, command, details):
    log_message = (
        f"📌 *User Log*\n👤 User: [{user.full_name}](tg://user?id={user.id})\n"
        f"🆔 User ID: `{user.id}`\n📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🔎 Command: `{command}`\n📜 Details: {details}"
    )
    await bot.send_message(LOG_CHANNEL_ID, log_message, parse_mode="Markdown")

# Start Command
@router.message(Command("start"))
async def start(message: types.Message):
    await log_command(message.from_user, "/start", "Started bot")
    response = """🎉 *Welcome!*  
🔎 Use this bot to fetch detailed **IP, phone, and country** information.  

✅ *Commands:*  
- `/ip <address>` – Full IP details 🌍  
- `/phone <number>` – Lookup phone carrier 📞   
- `/country <code>` – Get country details 🌎
- `/portscan <address>` – Get openports 🛜
- `/dns <address>` – Get DNS report 📃
- `/whois <address>` – Get domain report 📋
- `/help` – How to use this bot ❓  

🔥 Let's begin!"""
    await message.answer(response, parse_mode="Markdown")

# Help Command
@router.message(Command("help"))
async def help_command(message: types.Message):
    await log_command(message.from_user, "/help", "Asked for help")
    response = """🔍 *How to Use?*  

📌 *IP Lookup:*  
`/ip 42.27.18.19` → Get ISP, location, timezone, etc.  

📌 *Phone Lookup:*  
`/phone +14155552671` → Carrier, location, line type.   

📌 *Country Info:*  
`/country US` → Currency, language, population, etc.

📌 *WHOIS Lookup:*  
`/whois google.com` → Get domain WHOIS info.  

📌 *DNS Lookup:*
`/dns google.com` → Get DNS records.  

📌 *Port Scan:*  
`/portscan 1.1.1.1` → Scan open ports.
"""
    await message.answer(response, parse_mode="Markdown")

# Fetch IP Details (Using ip-api.com)
async def get_ip_details(ip):
    url = f"http://ip-api.com/json/{ip}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    
    if data.get("status") == "fail":
        return None
    
    return {
        "city": data.get("city", "Unknown"),
        "region": data.get("regionName", "Unknown"),
        "country": data.get("country", "Unknown"),
        "country_code": data.get("countryCode", "Unknown"),
        "latitude": data.get("lat", "Unknown"),
        "longitude": data.get("lon", "Unknown"),
        "isp": data.get("isp", "Unknown"),
        "timezone": data.get("timezone", "Unknown"),
        "zip": data.get("zip", "Unknown"),
        "asn": data.get("as", "Unknown"),
    }

# IP Lookup Command
@router.message(Command("ip"))
async def fetch_ip(message: types.Message):
    try:
        # Extract IP address from message
        ip = message.text.split(" ")[1]
        
        # Fetch IP details
        data = await get_ip_details(ip)
        if not data:
            await message.answer("⚠️ Invalid IP address or unable to fetch details.")
            return

        # Create Google Maps URL for location
        map_url = f"https://www.google.com/maps/search/?api=1&query={data['latitude']},{data['longitude']}"
        google_map_btn = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🌍 Open Google Maps", url=map_url)]]
        )

        # Prepare response message (escape potential Markdown conflicts)
        response = f"""🔎 *IP Lookup Results*    
📍 *Location:* {html.escape(data['city'])}, {html.escape(data['region'])}, {html.escape(data['country'])}  
📍 *Coordinates:* {html.escape(str(data['latitude']))}, {html.escape(str(data['longitude']))}  
🕒 *Timezone:* {html.escape(data['timezone'])}  
📡 *ISP:* {html.escape(data['isp'])}  
🔢 *ASN:* {html.escape(data['asn'])}  
📮 *ZIP Code:* {html.escape(data['zip'])}  
"""
        
        # Send response
        await message.answer(response, parse_mode="Markdown", reply_markup=google_map_btn)
        
        # Log the command (Optional)
        await log_command(message.from_user, "/ip", f"Looked up {ip}")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

# Fetch Country Details (Using REST Countries)
async def get_country_details(country_code):
    url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    response = requests.get(url)
    data = response.json()
    
    if not data:
        return None
    
    country_data = data[0]
    return {
        "name": country_data.get("name", {}).get("common", "Unknown"),
        "region": country_data.get("region", "Unknown"),
        "subregion": country_data.get("subregion", "Unknown"),
        "capital": ", ".join(country_data.get("capital", ["Unknown"])),
        "currency": ", ".join([currency for currency in country_data.get("currencies", {}).keys()]) if country_data.get("currencies") else "Unknown",
        "languages": ", ".join([lang for lang in country_data.get("languages", {}).values()]) if country_data.get("languages") else "Unknown",
        "population": country_data.get("population", "Unknown"),
        "area": country_data.get("area", "Unknown"),
        "timezone": ", ".join(country_data.get("timezones", ["Unknown"])),
        "borders": ", ".join(country_data.get("borders", [])) if country_data.get("borders") else "None",
    }

# Country Lookup Command
@router.message(Command("country"))
async def fetch_country(message: types.Message):
    try:
        parts = message.text.split(" ")
        if len(parts) < 2:
            await message.answer("⚠️ Please provide a valid country code. Example: `/country US`")
            return
        
        country_code = parts[1].upper()
        data = await get_country_details(country_code)
        if not data:
            await message.answer("⚠️ Invalid country code or unable to fetch details.")
            return

        response_text = f"""🌎 *Country Info*  
🏴 *Country:* {data['name']}  
📍 *Region:* {data['region']} → {data['subregion']}  
🏛 *Capital:* {data['capital']}  
💰 *Currency:* {data['currency']}  
🗣 *Languages:* {data['languages']}  
👥 *Population:* {data['population']}  
📏 *Area:* {data['area']} km²  
🕒 *Timezone:* {data['timezone']}  
🔗 *Borders:* {data['borders']}  
"""
        await message.answer(response_text, parse_mode="Markdown")
        await log_command(message.from_user, "/country", f"Looked up {country_code}")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

# Phone Lookup Command
async def get_phone_details(phone):
    """Fetches phone details from NumVerify API"""
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone}&format=1"
    response = requests.get(url)
    data = response.json()
    
    if data.get("valid"):
        country = data.get("country_name", "Unknown")
        country_code = data.get("country_code", "Unknown")
        carrier = data.get("carrier", "Unknown")
        line_type = data.get("line_type", "Unknown")
        international_format = data.get("international_format", "Unknown")
        local_format = data.get("local_format", "Unknown")

        # Fetch city and zip code using OpenCage API
        location_data = get_location_details(country)

        return {
            "valid": data.get("valid"),
            "country_name": country,
            "country_code": country_code,
            "carrier": carrier,
            "line_type": line_type,
            "international_format": international_format,
            "local_format": local_format,
            **location_data  # Merge location data
        }
    return None

def get_location_details(country):
    """Fetches zip code, city, and coordinates based on country name"""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={country}&key={OPENCAGE_API_KEY}"
    response = requests.get(url).json()

    if response.get("results"):
        data = response["results"][0]["components"]
        return {
            "location": data.get("city", data.get("state", "Unknown")),
            "zip": data.get("postcode", "Unknown"),
            "latitude": response["results"][0]["geometry"]["lat"],
            "longitude": response["results"][0]["geometry"]["lng"],
            "timezone": response["results"][0].get("annotations", {}).get("timezone", {}).get("name", "Unknown"),
        }

    return {"location": "Unknown", "zip": "Unknown", "latitude": "Unknown", "longitude": "Unknown", "timezone": "Unknown"}

# Phone Lookup Command
@router.message(Command("phone"))
async def fetch_phone(message: types.Message):
    try:
        phone = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else None
        if not phone:
            await message.answer("⚠️ Please provide a phone number in the correct format. Example: `/phone +919064582007`")
            return

        data = await get_phone_details(phone)
        if not data:
            await message.answer("⚠️ Invalid phone number or unable to fetch details.")
            return

        response_text = f"""📞 *Phone Lookup Results*  
✅ *Valid:* {data['valid']}  
🌎 *Country:* {data['country_name']} ({data['country_code']})  
📱 *Carrier:* {data['carrier']}  
📞 *Line Type:* {data['line_type']}  
🌆 *Location:* {data['location']}  
📌 *Zip Code:* {data['zip']}  
⏰ *Timezone:* {data['timezone']}  
🌍 *Coordinates:* {data['latitude']}, {data['longitude']}  
📌 *International Format:* {data['international_format']}  
🔢 *Local Format:* {data['local_format']}  
"""

        await message.answer(response_text, parse_mode="Markdown")
        await log_command(message.from_user, "/phone", f"Looked up {phone}")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")
        # WHOIS Lookup
@router.message(Command("whois"))
async def whois_lookup(message: types.Message):
    try:
        domain = message.text.split(" ", 1)[1]
        info = whois.whois(domain)
        response_text = f"""🔍 <b>WHOIS Lookup Results</b>  
🌐 <b>Domain:</b> <code>{domain}</code>  
📅 <b>Creation Date:</b> {info.creation_date}  
📅 <b>Expiration Date:</b> {info.expiration_date}  
📝 <b>Registrar:</b> {info.registrar}  
📧 <b>Emails:</b> {', '.join(info.emails) if info.emails else 'N/A'}  
"""
        await message.answer(response_text, parse_mode="HTML")
        await log_command(message.from_user, "/whois", f"Looked up {domain}")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

# DNS Lookup
@router.message(Command("dns"))
async def dns_lookup(message: types.Message):
    try:
        domain = message.text.split(" ", 1)[1]
        records = dns.resolver.resolve(domain, "A")
        response_text = f"""🌐 <b>DNS Lookup Results</b>  
🔗 <b>Domain:</b> <code>{domain}</code>  
📜 <b>Records:</b>  
"""
        for record in records:
            response_text += f"- {record}\n"
        
        await message.answer(response_text, parse_mode="HTML")
        await log_command(message.from_user, "/dns", f"Looked up {domain}")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")


       # Port Scanner
@router.message(Command("portscan"))
async def port_scan(message: types.Message):
    try:
        ip = message.text.split(" ", 1)[1]
        open_ports = []
        for port in range(1, 1025):  # Scan common ports
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        
        response_text = f"""🚪 <b>Port Scan Results</b>  
🌐 <b>IP:</b> <code>{ip}</code>  
🔓 <b>Open Ports:</b> {', '.join(map(str, open_ports)) if open_ports else 'None'}  
"""
        await message.answer(response_text, parse_mode="HTML")
        await log_command(message.from_user, "/portscan", f"Scanned {ip}")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")
       

@router.message(Command("info"))
async def get_info(message: types.Message, bot: Bot):
    try:
        # Extract username or ID
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return await message.reply("⚠️ Please specify a username or ID!\nExample: `/info @username`", parse_mode="Markdown")

        target = args[1].strip()
        response = ""

        try:
            chat = await bot.get_chat(target)

            # Basic chat details
            response = f"🔍 *Chat Information*"

            if chat.type in ["channel", "supergroup", "group"]:
                # Group/Channel Info
                response += f"""
📛 *Title:* {html.escape(chat.title if chat.title else 'N/A')}
🆔 *ID:* `{chat.id}`
📌 *Username:* @{chat.username if chat.username else 'N/A'}
🔒 *Type:* {chat.type.capitalize()}"""

                if chat.description:
                    response += f"\n📝 *Description:* {html.escape(chat.description)}"

                if chat.invite_link:
                    response += f"\n🔗 *Invite Link:* {chat.invite_link}"

            elif chat.type == "private":
                # User Info
                response += f"""
👤 *Name:* {html.escape(chat.first_name)} {html.escape(chat.last_name if chat.last_name else '')}
🆔 *ID:* `{chat.id}`
📌 *Username:* @{chat.username if chat.username else 'N/A'}
🤖 *Bot:* {'Yes' if chat.is_bot else 'No'}"""

                if chat.bio:
                    response += f"\n📝 *Bio:* {html.escape(chat.bio)}"

            # Fetch profile photo if available
            if chat.photo:
                photo = await bot.get_file(chat.photo.big_file_id)
                await message.answer_photo(photo.file_id, caption=response, parse_mode="Markdown")
            else:
                await message.reply(response, parse_mode="Markdown")

        except TelegramBadRequest as e:
            if "chat not found" in str(e).lower():
                await message.reply("❌ Error: The chat or user was not found. Make sure the username is correct and the bot has access to the chat.")
            else:
                await message.reply(f"❌ Error: {str(e)}")

    except Exception as e:
        await message.reply(f"⚠️ Unexpected Error: {str(e)}")

# Start Bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
