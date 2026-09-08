import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قاعدة بيانات مصغرة للتصاميم
COC_BASES = {
    "15": [
        {"title": "تصميم تاون 15 حرب (War)", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH15%3AWB%3AAAAAAQAAAA...", "image": "https://i.imgur.com/example1.jpg"},
    ],
    "16": [
        {"title": "تصميم تاون 16 حفظ موارد (Farm)", "link": "https://link.clashofclans.com/en?action=OpenLayout&id=TH16%3AHB%3AAAAAAQAAAA...", "image": "https://i.imgur.com/example2.jpg"},
    ]
}

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user}')

@bot.command(name="base")
async def get_base(ctx, th_level: str):
    if th_level in COC_BASES:
        base = COC_BASES[th_level][0]
        embed = discord.Embed(title=f"🏰 تصميم تاون هول {th_level}", description=base["title"], color=0xe74c3c)
        embed.add_field(name="🔗 رابط النسخ المباشر", value=f"[اضغط هنا لنسخ التصميم]({base['link']})")
        embed.set_image(url=base["image"])
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ اكتب رقم تاون هول صحيح (مثال: `!base 15`).")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
