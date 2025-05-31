import selfcord as discord
from discord.ext import commands
import asyncio

TOKEN = 'NTcxNzA3NDAxNDE4NTcxNzc4.Gm70-W.sOQ_IQr0FH-FomIgz1Kb1d1DbHEJVT9QnySeLY'

intents = discord.Intents.default()  # Требование selfcord указывания интента.
intents.messages = True

client = commands.Bot(
    command_prefix='!',
    self_bot=True,
    intents=intents
)

CHANNEL_1_ID = 1181428134676013056
CHANNEL_2_ID = 1316481550858326116

CHANNEL_MESSAGES = {
    CHANNEL_1_ID: ["Versetti\nСерый"],
    CHANNEL_2_ID: ["Versetti\nСерый"]
}

@client.event
async def on_ready():
    print(f'Залогинились как {client.user}')

async def can_send_message(channel):
    try:
        permissions = channel.permissions_for(channel.guild.me)
        return permissions.send_messages
    except Exception as e:
        print(f"Ошибка проверки прав: {e}")
        return False

async def wait_and_send(channel, message_text, channel_id):
    while True:
        if await can_send_message(channel):
            try:
                await channel.send(message_text)
                print(f"Отправил: {message_text}\nКанал: {channel_id}")
                return True
            except Exception as e:
                if str(e).find("429") != -1:
                    retry_after = float(str(e).split("Retrying in ")[1].split(" seconds")[0]) if "Retrying in" in str(e) else 0.1
                    print(f"Лимит скорости, ждем {retry_after:.2f} секунд")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Ошибка при отправке: {e}")
                    return False
        else:
            await asyncio.sleep(0)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'open' in message.content.lower():
        channel_id = message.channel.id
        if channel_id in CHANNEL_MESSAGES:
            channel = client.get_channel(channel_id)
            for msg in CHANNEL_MESSAGES[channel_id]:
                await wait_and_send(channel, msg, channel_id)

client.run(TOKEN)