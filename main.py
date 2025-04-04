from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from pyrogram import Client, filters
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from helper import get_drm_keys
from logger import logging
import time
import asyncio
from pyrogram.types import User, Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER, LOG
import sys
import os
import random
import re
import tempfile
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import datetime
import aiohttp

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
 
pwdl = os.environ.get("api")

processing_request = False  # Variable to track if a request is being processed

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

# Inline keyboard for busy status
Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

@bot.on_message(filters.command(["logs"]) )
async def send_logs(bot: Client, m: Message):
    try:
        
        # Assuming `assist.txt` is located in the current directory
         with open("Assist.txt", "rb") as file:
            sent= await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")


# List of image URLs
image_urls = [
    "https://tinypic.host/images/2025/02/07/IMG_20250207_224444_975.jpg",
    "https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png",
    # Add more image URLs as needed
]


@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Choose a random image URL from the list
    random_image_url = random.choice(image_urls)
    
    
    # Caption for the image
    caption = f"**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫  👋!\n\n➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️\n➠ Can Extract Videos & Pdf Form Your Text File and Upload to Telegram\n\n➠ 𝐔𝐬𝐞 /drm 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐅𝐫𝐨𝐦 𝐓𝐗𝐓 𝐅𝐢𝐥𝐞  \n\n➠𝐌𝐚𝐝𝐞 𝐁𝐲: 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 **\n"
    
    # Send the image with the caption
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    await m.reply_text("🦅ˢᵗᵒᵖᵖᵉᵈ ᵇᵃᵇʸ💞", True)
    os.execl(sys.executable, sys.executable, *sys.argv)  

@bot.on_message(filters.command(["drm"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"**➠ 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐓𝐗𝐓 𝐅𝐢𝐥𝐞 𝐢𝐧 𝐀 𝐏𝐫𝐨𝐩𝐞𝐫 𝐖𝐚𝐲 \n\n➠ TXT FORMAT : LINK : URL**")
    input: Message = await bot.listen(editable.chat.id)
    editable = await editable.edit(f"**⚙️PROCESSING INPUT.......**")

    if input.document:
        processing_request = True
        x = await input.download()        
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        path = f"./downloads/{m.chat.id}"

        try:
            links = []
            videocount = 0
            pdfcount = 0
            with open(x, "r", encoding="utf-8") as f:
                for line in f:
                    link = line.strip()
                    if isinstance(link, str):
                        link = link.split("://", 1)
                    links.append(link)
                    if isinstance(link, list) and len(link) > 1 and ".pdf" in link[1]:
                        pdfcount += 1 
                    else:
                        videocount += 1
            
        except Exception as e:
            await m.reply_text("Error occurred while processing the file.🥲")
            print("Error:", e)
            os.remove(x)
            processing_request = False  # Reset the processing flag
            return

    else:
        content = input.text
        content = content.split("\n")
        links = []
        videocount = 0
        pdfcount = 0

        for i in content:
            link = i.split("://", 1)
            links.append(link)
            if ".pdf" in link[1]:
                pdfcount += 1 
            else:
                videocount += 1
                
    await editable.edit(f"""**Total links found are : {len(links)}
┃
┠ Total Video Count : {videocount}
┠ Total Pdf Count: {pdfcount}  
┠ Send From where you want to download initial is  : `1` 
┃
┠ Send `stop` If don't want to Contine 
┖ Bot By : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎**""")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    if raw_text.lower() == "stop":
        await editable.edit(f"**Task Stoped ! **")
        await input0.delete(True)
        processing_request = False  # Reset the processing flag
        os.remove(x)
        return
    
    await editable.edit(f"**ENTER TILL WHERE YOU WANT TO DOWNLOAD \n┃\n┠ Starting Dowload Form : `{raw_text}`\n┖ Last Index Of Links is : `{len(links)}` **")
    input9: Message = await bot.listen(editable.chat.id)
    raw_text9 = input9.text
    
    if int(input9.text) > len(links) :
        await editable.edit(f"**PLZ ENTER NUMBER IN RANGE OF INDEX COUNT    **")
        processing_request = False  # Reset the processing flag
        await m.reply_text("**Exiting Task......  **")
        return
    else:
        await input9.delete(True)
    
    await editable.edit("**Enter Batch Name or send 1 for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '1':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution \n SEND 1080 720 480 360 240 144**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    quality = input2.text
    await input2.delete(True)
    
    await editable.edit("**Enter Your Name or send `1` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == '1':
        CR = "𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
    else:
        CR = raw_text3

    await editable.edit("**🖼 Send thumbnail url\n• If you don't want Send :  `no` **")  
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    thumb = input6.text
    thumb2 = input6.text

    await editable.edit("**Same thumb on pdf as video** : SEND `yes` \n\n**If don't want thumb on pdf** : SEND `no` \n\n**If you Want other thumbnail **: SEND `custom`")  
    input7 = message = await bot.listen(editable.chat.id)
    raw_text7 = input7.text.lower()  # Convert to lowercase
    await input7.delete(True)
    
    if raw_text7 == "custom":
        await editable.edit("**Send Pdf Thumb url **")  
        input8 = message = await bot.listen(editable.chat.id)
        raw_text8 = input8.text.lower()  # Convert to lowercase
        await input8.delete(True)
        await editable.delete()
        thumb3 = input8.text 
    else:
        await editable.delete()
    
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget {thumb} -O thumb1.jpg")
        thumb = "thumb1.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)
  
    try:
        for i in range(count - 1, int(input9.text)):
            V = links[i][1].replace("file/d/","uc?export=download&id=")\
               .replace("www.youtube-nocookie.com/embed", "youtu.be")\
               .replace("?modestbranding=1", "")\
               .replace("/view?usp=sharing","")\
               .replace("youtube.com/embed/", "youtube.com/watch?v=")

            url = "https://" + V

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'

            elif "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Language': 'en-US,en;q=0.9'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0luZGV4IjoxLCJleHAiOjE2MzI3NTg1Nzl9.7s2Pfl6A1q8UA5y7uZJ9sW-Jt7S-BZ5u9oa0Lvvji4Q'}).json()['url']

            # Fetch the DRM keys for the URL
            key = await get_drm_keys(url)
            
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "")
            name = f'{name1[:60]}'

            if "/master.mpd" in url :
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/","https://d1d34p8vz63oiq.cloudfront.net/")
                    print(url)
                
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "
                print("counted")
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"bestvideo.{quality}"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            if "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o ".mp4"'
            else: 
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o ".mp4"'
                print("counted 2 ")
            
            try:   
                cc = f' **➭ Index » {str(count)} /  {len(links)} **\n**➭ Title »  {name1}.mkv**\n\n**➭ 𝐁𝐚𝐭𝐜𝐡 » {b_name} **\n**➭ Quality » {raw_text2}**\n\n✨ **𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃 𝐁𝐘 » 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎**'
                cc1 = f'**➭ Index » {str(count)} /  {len(links)} **\n**➭ Title » {name1}.pdf** \n\n**➭ 𝐁𝐚𝐭𝐜𝐡 »  {b_name}**\n\n✨ **𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃 𝐁𝐘 » 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎**'
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e: 
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif ".pdf" in url:
                    try:
                        time.sleep(1)
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        time.sleep(1)
                        start_time = time.time()
                        reply = await m.reply_text(f"**⚡️ Starting Uploding ...** - `{name}`")
                        time.sleep(1)
                        if raw_text7 == "custom" :
                            subprocess.run(['wget', thumb3, '-O', 'pdfthumb.jpg'], check=True)  
                            thumbnail = "pdfthumb.jpg"
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                            os.remove(thumbnail)
                        elif thumb == "no" and raw_text7 == "no":
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, progress=progress_bar, progress_args=(reply, start_time))
                        elif raw_text7 == "yes" and thumb != "no":
                            subprocess.run(['wget', thumb2, '-O', 'thumb1.jpg'], check=True)  # Fixing this line
                            thumbnail = "thumb1.jpg"
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1,thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                        else:
                            subprocess.run(['wget', thumb2, '-O', 'thumb1.jpg'], check=True)  
                            thumbnail = "thumb1.jpg"
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                        await reply.delete (True)
                        os.remove(f'{name}.pdf')
                        count += 1
                        time.sleep(2)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    prog = await m.reply_text(f"📥 **Downloading **\n\n**➭ Index » {str(count)} /  {len(links)}**\n**➭ Title » ** `{name}`\n**➭ Quality** » `{raw_text2}`\n**➭ Thumbnail » ** `{thumb}`")
                    time.sleep(2)
                    res_file = await helper.drm_download_video(url,quality, name,key)
                    filename = res_file
                    await prog.delete(True)
                    time.sleep(1)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, thumb2)
                    count += 1
            except Exception as e:
                await m.reply_text(f"**This #Failed File is Counted**\n**Name** =>> `{name1}`\n\n ** Fail reason »** {e}")
                count += 1
                continue
    except Exception as e:
        await m.reply_text(e)
    time.sleep(2)

    await m.reply_text("🔰Done🔰")
    await m.reply_text("**✨Thanks for Choosing 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎**")
    processing_request = False  # Reset the processing flag  
    
processing_request = False  
bot.run()
