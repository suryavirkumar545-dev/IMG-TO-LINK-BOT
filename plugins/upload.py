# CantarellaBots
# Don't Remove Credit
# Telegram Channel @CantarellaBots
# Support group @rexbotschat

import os
import requests

from config import Config
from database import db
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# =========================================================
# CATBOX UPLOAD
# =========================================================

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"

    data = {
        "reqtype": "fileupload",
        "userhash": ""
    }

    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                url,
                data=data,
                files={
                    "fileToUpload": f
                },
                timeout=300
            )

        if response.status_code == 200:
            result = response.text.strip()

            if result.startswith("https://"):
                return result, None

            return None, f"Catbox Error: {result}"

        return None, (
            f"Catbox HTTP Error: "
            f"{response.status_code} - {response.text}"
        )

    except requests.exceptions.Timeout:
        return None, "Catbox upload timed out."

    except requests.exceptions.RequestException as e:
        return None, f"Catbox Connection Error: {str(e)}"

    except Exception as e:
        return None, f"Unexpected Catbox Error: {str(e)}"


# =========================================================
# LOG CHANNEL
# =========================================================

async def send_log_to_channel(
    client: Client,
    message: Message,
    link: str
):
    """
    Sends the original uploaded media to the LOG_CHANNEL
    and then sends upload information below it.
    """

    if not Config.LOG_CHANNEL:
        print("LOG_CHANNEL is not configured.")
        return

    try:
        log_channel = int(Config.LOG_CHANNEL)

        # -------------------------------------------------
        # 1. COPY ORIGINAL MEDIA TO LOG CHANNEL
        # -------------------------------------------------

        await client.copy_message(
            chat_id=log_channel,
            from_chat_id=message.chat.id,
            message_id=message.id
        )

        # -------------------------------------------------
        # 2. SEND UPLOAD INFORMATION
        # -------------------------------------------------

        user = message.from_user

        if user:
            username = user.username

            if username:
                user_text = f"@{username}"
            else:
                user_text = user.mention

            user_id = user.id
        else:
            user_text = "Unknown"
            user_id = "Unknown"

        log_text = (
            "**#Nᴇᴡ_Uᴘʟᴏᴀᴅ**\n\n"
            f"**👤 Uꜱᴇʀ:** {user_text}\n"
            f"**🆔 Uꜱᴇʀ ID:** `{user_id}`\n"
            f"**🔗 Lɪɴᴋ:** `{link}`\n"
            f"**🕒 Tɪᴍᴇ:** `{message.date}`"
        )

        await client.send_message(
            chat_id=log_channel,
            text=log_text,
            disable_web_page_preview=True
        )

        print(
            f"Successfully logged upload "
            f"from user {user_id}"
        )

    except Exception as e:
        print(
            f"Log Channel Error: {type(e).__name__}: {e}"
        )


# =========================================================
# MEDIA UPLOAD HANDLER
# =========================================================

@Client.on_message(
    filters.photo |
    filters.animation |
    filters.video
)
async def upload_media(
    client: Client,
    message: Message
):

    # -----------------------------------------------------
    # BAN CHECK
    # -----------------------------------------------------

    if db:
        try:
            if await db.is_banned(message.from_user.id):
                return await message.reply_text(
                    "**🚫 Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ "
                    "ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ!**"
                )
        except Exception as e:
            print(f"Ban Check Error: {e}")

    # -----------------------------------------------------
    # STATUS MESSAGE
    # -----------------------------------------------------

    status_msg = await message.reply_text(
        "Downloading media...",
        quote=True
    )

    file_path = None

    try:

        # -------------------------------------------------
        # DOWNLOAD MEDIA FROM TELEGRAM
        # -------------------------------------------------

        file_path = await message.download()

        if not file_path or not os.path.exists(file_path):
            return await status_msg.edit_text(
                "❌ Failed to download the media from Telegram."
            )

        # Get file size
        file_size = os.path.getsize(file_path)

        await status_msg.edit_text(
            "Uploading to Catbox..."
        )

        # -------------------------------------------------
        # UPLOAD TO CATBOX
        # -------------------------------------------------

        link, error = upload_to_catbox(file_path)

        # -------------------------------------------------
        # DELETE LOCAL FILE
        # -------------------------------------------------

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(
                    f"File Delete Error: {e}"
                )

        # -------------------------------------------------
        # UPLOAD FAILED
        # -------------------------------------------------

        if not link:

            await status_msg.edit_text(
                f"❌ **Failed to upload.**\n\n"
                f"**Reason:** `{error}`"
            )

            return

        # -------------------------------------------------
        # SUCCESS MESSAGE TO USER
        # -------------------------------------------------

        await status_msg.edit_text(
            text=(
                "**✅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ Uᴘʟᴏᴀᴅᴇᴅ!**\n\n"
                f"**> Lɪɴᴋ:** `{link}`\n\n"
                f"**> Dɪʀᴇᴄᴛ Lɪɴᴋ:** "
                f"[Cʟɪᴄᴋ Hᴇʀᴇ]({link})"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔗 Oᴘᴇɴ Lɪɴᴋ",
                            url=link
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True
        )

        # -------------------------------------------------
        # SAVE TO DATABASE
        # -------------------------------------------------

        if db:
            try:
                await db.add_upload(
                    message.from_user.id,
                    link
                )
            except Exception as e:
                print(
                    f"Database History Error: {e}"
                )

        # -------------------------------------------------
        # SEND FILE + DETAILS TO LOG CHANNEL
        # -------------------------------------------------

        await send_log_to_channel(
            client=client,
            message=message,
            link=link
        )

    # -----------------------------------------------------
    # GENERAL ERROR
    # -----------------------------------------------------

    except Exception as e:

        print(
            f"Upload Handler Error: "
            f"{type(e).__name__}: {e}"
        )

        try:
            await status_msg.edit_text(
                f"❌ **An error occurred.**\n\n"
                f"`{str(e)}`"
            )
        except Exception:
            pass

        # -------------------------------------------------
        # CLEANUP
        # -------------------------------------------------

        try:
            if (
                file_path
                and os.path.exists(file_path)
            ):
                os.remove(file_path)

        except Exception as cleanup_error:
            print(
                f"Cleanup Error: {cleanup_error}"
            )


# =========================================================
# END OF FILE
# =========================================================;0
