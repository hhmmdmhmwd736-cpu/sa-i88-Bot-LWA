import os
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask

# --- إعداد خادم الويب لإبقاء الخدمة متصلة 24/7 ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot is active'


def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.daemon = True
  t.start()


keep_alive()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# قاعدة بيانات التصاميم (يمكنك زيادة أرقام التاونات ورابط كل تاون هنا)
COC_BASES = {
    '15': [{
        'title': 'تصميم تاون 15 حرب (War)',
        'link': (
            'https://link.clashofclans.com/en?action=OpenLayout&id=TH15%3AWB%3AAAAAAQAAAAK'
        ),
    }],
    '16': [{
        'title': 'تصميم تاون 16 حفظ موارد (Farm)',
        'link': (
            'https://link.clashofclans.com/en?action=OpenLayout&id=TH16%3AFB%3AAAAAAQAAAAK'
        ),
    }],
    '17': [{
        'title': 'تصميم تاون 17 احترافي',
        'link': 'ضع_رابط_التصميم_هنا',
    }],
    '18': [{
        'title': 'تصميم تاون 18 احترافي',
        'link': 'ضع_رابط_التصميم_هنا',
    }],
}


@bot.event
async def on_ready():
  print(f'تم تشغيل البوت بنجاح باسم {bot.user}')


@bot.command(name='base')
async def get_base(ctx, th_level: str):
  if th_level in COC_BASES:
    base = COC_BASES[th_level][0]
    embed = discord.Embed(
        title=f'🏰 تصميم تاون هول {th_level}',
        description=base['title'],
        color=0xE74C3C,
    )
    embed.add_field(
        name='🔗 رابط النسخ المباشر',
        value=f"[اضغط هنا لنسخ التصميم]({base['link']})",
    )
    if 'image' in base:
      embed.set_image(url=base['image'])
    await ctx.send(embed=embed)
  else:
    await ctx.send('❌ اكتب رقم تاون هول صحيح (مثال: `!base 15`).')


TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
