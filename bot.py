import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 PUT YOUR BOT TOKEN HERE
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"


class IPTool:
    def __init__(self):
        self.session = requests.Session()

    def lookup(self, ip):
        try:
            d1 = self.session.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            d2 = self.session.get(f"https://ipinfo.io/{ip}/json", timeout=5).json()
            d3 = self.session.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
        except:
            return None

        if d1.get("status") != "success":
            return None

        # Best coordinates
        lat = d1.get("lat") or (d2.get("loc", "").split(",")[0] if "loc" in d2 else None)
        lon = d1.get("lon") or (d2.get("loc", "").split(",")[1] if "loc" in d2 else None)

        return {
            "ip": ip,
            "country": d1.get("country"),
            "region": d1.get("regionName"),
            "city": d1.get("city"),
            "zip": d1.get("zip"),
            "lat": lat,
            "lon": lon,
            "map": f"https://maps.google.com/?q={lat},{lon}" if lat else "N/A",
            "isp": d1.get("isp"),
            "org": d2.get("org"),
            "asn": d1.get("as"),
            "timezone": d1.get("timezone"),
            "currency": d3.get("currency"),
            "languages": d3.get("languages"),
            "proxy": d1.get("proxy"),
            "hosting": d1.get("hosting"),
            "mobile": d1.get("mobile")
        }


tool = IPTool()


# ▶️ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send IP address 🌍\nExample: 8.8.8.8")


# 📩 Handle IP input
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip = update.message.text.strip()

    data = tool.lookup(ip)

    if not data:
        await update.message.reply_text("❌ Invalid IP or failed")
        return

    msg = f"""
🌍 IP DETAILS

IP: {data['ip']}
Country: {data['country']}
Region: {data['region']}
City: {data['city']}
ZIP: {data['zip']}

📍 LOCATION
Lat: {data['lat']}
Lon: {data['lon']}
Map: {data['map']}

🌐 NETWORK
ISP: {data['isp']}
ORG: {data['org']}
ASN: {data['asn']}

🛡️ STATUS
Proxy: {data['proxy']}
Hosting: {data['hosting']}
Mobile: {data['mobile']}

🌎 EXTRA
Timezone: {data['timezone']}
Currency: {data['currency']}
Languages: {data['languages']}
"""

    await update.message.reply_text(msg)


# 🚀 RUN BOT
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("Bot running 24/7 🚀")
    app.run_polling()
