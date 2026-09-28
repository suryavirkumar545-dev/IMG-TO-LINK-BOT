# CantarellaBots
# Don't Remove Credit
# Telegram Channel @CantarellaBots
#Supoort group @rexbotschat
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import Config
from database import db
# CantarellaBots
# Don't Remove Credit
# Telegram Channel @CantarellaBots
#Supoort group @rexbotschat
async def check_sub(client, user_id):
    if not Config.FORCE_SUB_CHANNEL:
        return True
    try:
        await client.get_chat_member(Config.FORCE_SUB_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return True # Fail safe
# CantarellaBots
# Don't Remove Credit
# Telegram Channel @CantarellaBots
#Supoort group @rexbotschat
@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    # Sticker Animation
    sticker_msg = await message.reply_sticker("CAACAgUAAxkBAAEQcXpphjJqNeJJJFUdGvlKwz7-TZJFVQACMhwAAtNIIFX3hUNroWBUqTgE")
    import asyncio
    await asyncio.sleep(1)
    await sticker_msg.delete()

    if db:
        is_new = await db.add_user(message.from_user.id)
        if is_new and Config.LOG_CHANNEL:
             try:
                log_text = (
                    f"**#Nᴇᴡ_Uꜱᴇʀ**\n\n"
                    f"**👤 Uꜱᴇʀ:** {message.from_user.mention} (`{message.from_user.id}`)\n"
                    f"**📅 Dᴀᴛᴇ:** {message.date}"
                )
                await client.send_message(
                    chat_id=int(Config.LOG_CHANNEL),
                    text=log_text
                )
             except Exception as e:
                print(f"Log Error: {e}")

        if await db.is_banned(message.from_user.id):
            return await message.reply_text("**🚫 Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ!**")

    # Force Subscription Check
    is_subscribed = await check_sub(client, message.from_user.id)
    if not is_subscribed:
        try:
            invite_link = await client.export_chat_invite_link(Config.FORCE_SUB_CHANNEL)
        except:
             # Fallback: If username (starts with @ or no -100), construct link. If ID, we can't guess.
             if str(Config.FORCE_SUB_CHANNEL).startswith("-100"):
                 
                 invite_link = "https://t.me/CARTOONFUNNY04" # Fallback to updates channel if specific fail
             else:
                 invite_link = f"https://t.me/{Config.FORCE_SUB_CHANNEL.replace('@', '')}"
        
        btn = [[InlineKeyboardButton("📢 Jᴏɪɴ Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url=invite_link)]]
        return await message.reply_text(
            text="**⚠️ Yᴏᴜ Mᴜꜱᴛ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ Tᴏ Uꜱᴇ Tʜɪꜱ Bᴏᴛ!**\n\n"
                 "> Pʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(btn)
        )

    # Main Start UI
    txt = (
        f"**👋 Hᴇʟʟᴏ {message.from_user.mention},**\n\n"
        f"**> I ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ Iᴍᴀɢᴇ ᴛᴏ Lɪɴᴋ Uᴘʟᴏᴀᴅᴇʀ Bᴏᴛ.**\n\n"
        f"**🛠 Fᴇᴀᴛᴜʀᴇꜱ:**\n"
        f"**> ⚡ Fᴀꜱᴛ Uᴘʟᴏᴀᴅꜱ (Cᴀᴛʙᴏx)**\n"
        f"**> 🔗 Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋꜱ**\n"
        f"**> 🛡️ Sᴇᴄᴜʀᴇ & Pʀɪᴠᴀᴛᴇ**"
    )

    btn = [
        [
            InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇꜱ", url="https://t.me/CARTOONFUNNY04"),
            InlineKeyboardButton("👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/skanime04")
        ],
        [
            InlineKeyboardButton("➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ", url=f"https://t.me/{client.me.username}?startgroup=true")
        ]
    ]

    if Config.START_PIC:
        await message.reply_photo(
            photo=Config.START_PIC,
            caption=txt,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    else:
        await message.reply_text(
            text=txt,
            reply_markup=InlineKeyboardMarkup(btn),
            disable_web_page_preview=True
        )
# CantarellaBots
# Don't Remove Credit
# Telegram Channel @CantarellaBots
#Supoort group @rexbotschat


# CantarellaBots
# Don't Remove Credit
# Telegram Channel @CantarellaBots
#Supoort group @rexbotschat
