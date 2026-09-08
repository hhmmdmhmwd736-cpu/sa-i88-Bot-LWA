import os
import random
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask
import requests
from bs4 import BeautifulSoup

# --- إعداد سيرفر الويب للتشغيل المستمر 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is active 24/7"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

# --- إعدادات ديسكورد ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- بنك تصاميم احتياطي عشوائي (في حال تعذر الجلب من الموقع) ---
FALLBACK_BASES = {
    "18": [
        {"title": "تصميم حرب احترافي (CWL Anti-3)", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH18%3AWB%3A1"},
        {"title": "تصميم حفظ موارد (Farm Defense)", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH18%3AFB%3A2"},
        {"title": "تصميم رفع كؤوس (Trophy Rush)", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH18%3ATB%3A3"},
        {"title": "تصميم محكم ضد النجمتين (Anti 2-Star)", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH18%3AWB%3A4"}
    ],
    "17": [
        {"title": "تصميم حرب تاون 17", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH17%3AWB%3A1"},
        {"title": "تصميم فارم تاون 17", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH17%3AFB%3A1"}
    ],
    "16": [
        {"title": "تصميم حرب تاون 16", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH16%3AWB%3A1"}
    ]
}

# --- دالة كشط وجلب التصاميم حياً من الموقع ---
def fetch_live_base(th_level):
    try:
        url = f"https://clashofclans-layouts.com/plan/th_{th_level}/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # البحث عن الروابط الخاصة بـ clashofclans.com داخل الصفحة
            links = []
            for a in soup.find_all('a', href=True):
                if 'link.clashofclans.com' in a['href']:
                    links.append(a['href'])
            if links:
                return random.choice(links), "🌐 جلب مباشر متجدد من الموقع"
    except Exception as e:
        print(f"Error scraping site: {e}")
    
    return None, None

@bot.command(name="base")
async def get_base(ctx, th_level: str):
    # 1. المحاولة الأولى: جلب حي ومباشر من الموقع
    live_link, source_label = fetch_live_base(th_level)
    
    if live_link:
        embed = discord.Embed(
            title=f"🏰 تصميم متجدد لتاون هول {th_level}",
            description=f"**المصدر:** {source_label}",
            color=0x2ecc71
        )
        embed.add_field(
            name="🔗 رابط النسخ المباشر", 
            value=f"[اضغط هنا لنسخ التصميم]({live_link})"
        )
        embed.set_footer(text="💡 اطلب الأمر مرة أخرى للحصول على تصميم جديد أوتوماتيكياً!")
        await ctx.send(embed=embed)
        return

    # 2. المحاولة الثانية: الاختيار العشوائي من البنك الاحتياطي
    if th_level in FALLBACK_BASES:
        selected = random.choice(FALLBACK_BASES[th_level])
        embed = discord.Embed(
            title=f"🏰 تصميم عشوائي لتاون هول {th_level}",
            description=f"**النمط:** {selected['title']}",
            color=0xe74c3c
        )
        embed.add_field(
            name="🔗 رابط النسخ المباشر", 
            value=f"[اضغط هنا لنسخ التصميم]({selected['link']})"
        )
        embed.set_footer(text="💡 اطلب الأمر مرة أخرى للحصول على تصميم مختلف!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ اكتب رقم تاون هول صحيح (مثال: `!base 18`).")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
