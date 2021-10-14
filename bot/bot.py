from pyrogram import Client, filters , errors
import sqlite3
from pyrogram.types import ChatPermissions , ChatMember
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from os import path
from time import time
from pyrogram.types.messages_and_media import message
import requests
from pyrogram.types import (InlineQueryResultArticle, 
                            InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardMarkup)

from pyrogram import types                        
app = Client(
    session_name="DevBax",
    api_id="APIid",
    api_hash="Apihash",
    bot_token="TOKEN"

)
TARGET = "commit_zone"

@app.on_message(filters.command("start"))
def info(client , message):
        
    message.reply_text("""🌍ربات اوپن سورس دووبکس جهت اداره راحت تره گروه :))

اگه گروه داری میتونی از سورسش استفاده کنی :))


🏖 توسعه دهنده اصلی : @Mehranalam
🏪 اگه میخوای تویه توسعه اش به ما کمک کنی میتونی از لینک زیر اقدام کنی :)))

📎github.com/mehranalam/devbax-bot""")


@app.on_message(filters.command("help"))
def help(client , message):
    message.reply_text("""🗄برای اطلاع از نحوه کارکرد ربات و‌ آشنایی به دستورات میتوانید داکیومنت مربوطه را مطالعه کنید

🔗 https://mehranalam.github.io/DevBax-bot/""")

def admin():
    con = sqlite3.connect('UserBase.db')
    sql = 'DELETE FROM Admins'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    j = 0
    for i in app.get_chat_members(TARGET, filter="administrators"):
        con = sqlite3.connect('UserBase.db')
        cur = con.cursor()
        id = int(i["user"]["id"])
        name = str(i["user"]["first_name"])
        cur.execute("INSERT INTO Admins VALUES (?,?)",(id, name))
        con.commit()
        j += 1

    con.close()
    return j

def user():
    con = sqlite3.connect('UserBase.db')
    sql = 'DELETE FROM User'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    n = 0
    for member in app.iter_chat_members(TARGET):
        con = sqlite3.connect('UserBase.db')
        cur = con.cursor()
        id = int(member.user.id)
        name = str(member.user.first_name)
        cur.execute("INSERT INTO User VALUES (?,?)",(id, name))
        con.commit()
        n += 1
    
    con = sqlite3.connect('UserBase.db')
    sql = 'DELETE FROM Score'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    for member in app.iter_chat_members(TARGET):
        con = sqlite3.connect('UserBase.db')
        cur = con.cursor()
        id = int(member.user.id)
        name = str(member.user.first_name)
        cur.execute("INSERT INTO Score VALUES (?,?,?)",(id, name , 0))
        con.commit()
    con.close()

    con = sqlite3.connect('UserBase.db')
    sql = 'DELETE FROM Warn'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    for member in app.iter_chat_members(TARGET):
        con = sqlite3.connect('UserBase.db')
        cur = con.cursor()
        id = int(member.user.id)
        name = str(member.user.first_name)
        cur.execute("INSERT INTO Warn VALUES (?,?,?)",(id, name , 0))
        con.commit()
    con.close()
    return n

def scoreRate(id ,fistname ,score):
    finalScore = 0
    con = sqlite3.connect('UserBase.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Score ORDER BY Scorenumber'):
        if int(row[0]) == id:
            finalScore = row[2] + score
    cur.execute("UPDATE Score SET Scorenumber = ? WHERE id = ?",(finalScore , id))
    con.commit()
    con.close()
            

def warnRate(id ,fistname ,warn):
    warnrate = 0
    con = sqlite3.connect('UserBase.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Warn ORDER BY warnRate'):
        if int(row[0]) == id:
            warnrate = row[2] + warn
    cur.execute("UPDATE Warn SET warnRate = ? WHERE id = ?",(warnrate , id))
    con.commit()
    con.close()

def removeWarn(id ,fistname ,warn):
    warnrate = 0
    con = sqlite3.connect('UserBase.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Warn ORDER BY warnRate'):
        if int(row[0]) == id:
            warnrate = row[2] - warn
    cur.execute("UPDATE Warn SET warnRate = ? WHERE id = ?",(warnrate , id))
    con.commit()
    con.close()

def checkWarn(id):
    con = sqlite3.connect('UserBase.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Warn ORDER BY warnRate'):
        if int(row[0]) == id:
            if row[2] > 4:
                return True
            return False



# create tale for once
@app.on_message(filters.chat(TARGET) & filters.command("create"))
def createTable(client, message):
    chat_id = app.get_chat(TARGET)
    app.delete_messages(chat_id["id"],message.message_id)
    check = False
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break
    if check:
        if path.exists("UserBase.db"):
            os.remove("UserBase.db") 
        con = sqlite3.connect('UserBase.db')
        cur = con.cursor()
        # Create table
        cur.execute('''CREATE TABLE User
                (id text, name text)''')

        cur.execute('''CREATE TABLE Admins
                (id text, name text)''')

        cur.execute('''CREATE TABLE Score
                (id text, name text ,Scorenumber)''')
                
        cur.execute('''CREATE TABLE Warn
                (id text, name text ,warnRate)''')

        cur.execute('''CREATE TABLE newUser
                (id text, name text)''')
    
        message.reply_text("دیتابیس با موفقیت ساخته شد")
    

# Update data base to new user
@app.on_message(filters.chat(TARGET) & filters.command("update"))
def updatedatabase(client, message):
    chat_id = app.get_chat(TARGET)
    app.delete_messages(chat_id["id"],message.message_id)
    check = False
    
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break
    if check:
        app.send_message(chat_id["id"] , "این فرایند کمی طولانی است ... منتظر باشید")
        n = user()
        j = admin()
        app.edit_message_text(chat_id["id"] ,(message.message_id+1),f"""
    🪂دیتابیس آپدیت شد و به تعداد {n} کاریر ادد شد.
    👨🏽‍🎤و به تعداد {j} ادمین ثبت شد.""")
    

holog = list()
# CAPTChA
@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
def welcome(client, message):
    con = sqlite3.connect('UserBase.db')
    cur = con.cursor()
    holog.clear()
    mention = message.from_user.username
    firstnumber = random.randint(1 , 11)
    secondnumber = random.randint(1 , 11)
    thirdnumber = random.randint(1 , 11)
    chat_id = app.get_chat(TARGET)
    reply_to_message_id=message.from_user
    user_id = reply_to_message_id["id"]
    cur.execute("INSERT INTO User VALUES (?,?)",(user_id, message.from_user.first_name))
    cur.execute("INSERT INTO Score VALUES (?,?,?)",(user_id, message.from_user.first_name , 0))
    cur.execute("INSERT INTO Warn VALUES (?,?,?)",(user_id, message.from_user.first_name , 0))
    con.commit()
    con.close()
    messageid = message.message_id + 1
    app.delete_messages(chat_id["id"] , messageid-1)
    app.restrict_chat_member(chat_id["id"], user_id, ChatPermissions())
    finalanswer = secondnumber * thirdnumber + firstnumber
    key1 = InlineKeyboardButton(
                        f"{random.randint(1 , 11) * random.randint(11 , 15) + random.randint(-3 , 0)}",
                        callback_data=f"startVerify_{str(message.from_user.id)}_{messageid}"
                    )
    holog.append(key1)
    key2 = InlineKeyboardButton( 
                        f"{random.randint(-8 , -4) * random.randint(-11 , 1) + random.randint(12 , 16)}",
                        callback_data=f"startVerify_{str(message.from_user.id)}_{messageid}"
                    )
    holog.append(key2)    
    key3 = InlineKeyboardButton(
                        f"{random.randint(0 , 2) * random.randint(-3 , 0) + random.randint(15 , 19)}",
                        callback_data=f"startVerify_{str(message.from_user.id)}_{messageid}"
                    )
    holog.append(key3)
    key4 = InlineKeyboardButton(
                        f"{random.randint(0, 1) * random.randint(-14 , -11) + random.randint(1 , 11)}" ,
                        callback_data=f"startVerify_{str(message.from_user.id)}_{messageid}"
                    )
    holog.append(key4)
    data = holog[random.randint(0 , 3)]
    data.text = f"{finalanswer}"
    data.callback_data = f"startVerify_{str(message.from_user.id)}_{messageid}_correct"
    message.reply_text(
        f"""
🥳سلام @{mention} عزیز به جمع ما خوش آمدی :)) 
لطفا به جهت اطمینان از ربات نبودنتان به کپچا پاسخ دهید تا محدودیت ارسال پیام برایتان رفع شود :)
{secondnumber} * {thirdnumber} + {firstnumber}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    holog[0],holog[1]
                ],
                [  # Second row
                    holog[2],holog[3]
                ]
            ]
        )
    )
@app.on_callback_query()
def answer(client, callback_query):
    if callback_query.data.startswith("startVerify_"):
        chat_id = app.get_chat(TARGET)
        user_id_clicked = callback_query.from_user.id
        message_id = callback_query.data.split("_")[2]
        if callback_query.data.startswith("startVerify_"):
            __user = callback_query.data.split("_")[1]
            if user_id_clicked == int(__user):
                if callback_query.data == f"startVerify_{str(__user)}_{message_id}_correct":
                    callback_query.answer("""کاملا درست پاسخ دادی✅
        از حالا میتونی تو گروه با دوستان چت کنی :))""", show_alert=True)
                    app.restrict_chat_member(chat_id["id"], int(__user), ChatPermissions(can_send_messages=True,
                                                                                    can_send_media_messages=True,
                                                                                    can_send_stickers=True,
                                                                                    can_use_inline_bots=True,
                                                                                    can_send_animations=True))
                    app.delete_messages(chat_id["id"], int(callback_query.data.split("_")[2]))
                else:
                    callback_query.answer("""اشتباه پاسخ دادی❌
        شما توسط ربات , ربات تشخیص داده شدی و از گروه کیک میشی :))
        اگه ربات نیستی دوباره تلاش کن""", show_alert=True)
                    app.delete_messages(chat_id["id"], int(callback_query.data.split("_")[2]))
                    app.kick_chat_member(chat_id["id"], __user)
                    app.unban_chat_member(chat_id["id"], __user)
            else:
                callback_query.answer("❌این کپچا متعلق یه شما نیست❌", show_alert=True)
    elif callback_query.data.startswith("g"):
        chat_id = app.get_chat(TARGET)
        user_id_clicked = callback_query.from_user.id
        data = callback_query.data.split("_")
        if int(data[1]) == user_id_clicked or int(data[3]) == user_id_clicked:
            if f"g_{data[1]}_{data[2]}_{data[3]}_g" == callback_query.data:
                callback_query.message.edit(f"""🧛‍♂️پیام توسط یکی از طرف عمومی سازی شد.
متن پیام بدین شرح بود :

__{data[2]}__""")
                
            callback_query.answer(f"""{data[2]}""", show_alert=True)
        else:
            callback_query.answer("🛑این پیام متعلق به شما نیست🛑" , show_alert=True)

    else:
        if callback_query.data == "+":
            callback_query.answer("""با ریپلای این علامت میتوانید به صورت نمادین از افراد تشکر کنی""",  show_alert=True)
        elif callback_query.data == "!+":
            callback_query.answer("""آگاه کردن افرادی که بجای امتیاز دهی از عبارت هایی مثل ممنون و تشکر استفاده میکنن""" ,  show_alert=True)
        elif callback_query.data == "ban":
            callback_query.answer("""با ریپلای این پیام توسط سودو ها این شخص برای همیشه از گروه بن میشود""" , show_alert=True)
        elif callback_query.data == "unban":
            callback_query.answer("آزاد سازی فرد خاطی" , show_alert=True)
        elif callback_query.data == "haskel":
            callback_query.answer("""میتونید با مراجعه به پی وی ربات و ارسال این الگو (haskelhide^usernameWithOut@^text) یک پیام مخفی برای کاربر مدنظر در گروه ارسال میشود .""" , show_alert=True)
        elif callback_query.data == "del":
            callback_query.answer("حذف چند پیام اخیر گروه" , show_alert=True)
        elif callback_query.data == "mute":
            callback_query.answer("با ریپلای این پیام فرد برای همیشه خاموش خواهد ماند" , show_alert=True)
        elif callback_query.data == "mutet":
            callback_query.answer("میوت زماندار(تا الان برای ثانیه مقدور است)" , show_alert=True)
        elif callback_query.data == "unmute":
            callback_query.answer("آزاد سازی برای چت" , show_alert=True)
        elif callback_query.data == "promote":
              callback_query.answer("فرد تبدیل به یک ادمین با حداکثر 2 سطح خواهد شد" , show_alert=True)
        elif callback_query.data == "warn":
            callback_query.answer("اخطار به کاربر(اگر تعداد اخطار ها از مرز 4 عدد عبور کند برای همیشه از گروه بن خواهد شد)" , show_alert=True)       
        elif callback_query.data == "!m":
            callback_query.answer("تذکر یه افرادی که با منشن کردن افراد مزاحمت ایجاد میکنند" , show_alert=True)
        elif callback_query.data == "!doc":
            callback_query.answer("نمایش داکیومنت" , show_alert=True)
        elif callback_query.data == "!q":
            callback_query.answer("ریپلای روی کسانی که آداب سوال کردن را نمیدانند", show_alert=True)
        elif callback_query.data == "pin":
            callback_query.answer("برای پین کردن یک پیام به کار میرود" , show_alert=True)
        elif callback_query.data == "unpin":
            callback_query.answer("برای برداشتن پین یک پیام به کار میرود" , show_alert=True)
        elif callback_query.data == "stat":
            callback_query.answer("برای نمایش وضعیت کلی یک یوزر" , show_alert=True)
        elif callback_query.data == "lit":
            callback_query.answer("نمایش اطلاعات پابلیک یک یوزر در گیت هاب با احتساب تعداد فنجون قهوه های خورده شده و ساعات کد زنی" , show_alert=True)
        elif callback_query.data == "/c":
            callback_query.answer("ریست و ساخت دوباره دیتابیس", show_alert=True)
        elif callback_query.data == "/u":
            callback_query.answer("آپدیت کاربران یه صورت دستی ، این عمل در 24 ساعت یکبار انجام میشود به صورت اتوماتیک" , show_alert=True)
        elif callback_query.data == "command":
            callback_query.answer("دیدن دستورات کل ربات", show_alert=True)
        elif callback_query.data == "rmw":
            callback_query.answer("حذف اخطار یک کاربر", show_alert=True)
        elif callback_query.data == "repdel":
            callback_query.answer("با ریپلای این پیام رو پیام موردنظر آن پیام از چت پاک میشود", show_alert=True)
        elif callback_query.data == "captcha":
            callback_query.answer("تذکر به افرادی که پس از ورود به گروه هنوز کپتچای مورد نظر را حل نکردند", show_alert=True)      
        

# delete message for left the chat
@app.on_message(filters.chat(TARGET) & filters.left_chat_member)
def lefDeleteChat(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)

@app.on_message(filters.chat(TARGET) & filters.regex("mote"))
def promote(client, message):
    check = False
    if app.get_chat_member(TARGET , user_id=message.from_user.id).title == "sudo":
        check = True

    if check:
        data = message.text.split(" ")
        chat_id = app.get_chat(TARGET)
        reply_to_message_id=message.reply_to_message.from_user
        if message.text.startswith("promote"):
            if data[1] == "3":
                getwwarnId =  reply_to_message_id["first_name"]
                getwarnId = reply_to_message_id["id"]

                MENTIONGetter = f"[{getwwarnId}](tg://user?id={getwarnId})" 
                app.promote_chat_member(chat_id["id"], getwarnId , can_manage_voice_chats=True)
                app.set_administrator_title(chat_id["id"], getwarnId, "co-sudoer")
                message.reply_text(f"""📶کاربر {MENTIONGetter} الان یک **co-sudoer **است و سطح دسترسی 3 را دارد...

🕵🏻‍♂️برای فهمیدن سازوکار بات کلمه **!doc** را در گروه ارسال کنید""")
            elif data[1] == "2":
                getwwarnId =  reply_to_message_id["first_name"]
                getwarnId = reply_to_message_id["id"]

                MENTIONGetter = f"[{getwwarnId}](tg://user?id={getwarnId})" 
                app.promote_chat_member(chat_id["id"], getwarnId , can_change_info=True)
                app.set_administrator_title(chat_id["id"], getwarnId, "fSudo")
                message.reply_text(f"""📶کاربر {MENTIONGetter} الان یک **fSudo **است و سطح دسترسی 2 را دارد...

🕵🏻‍♂️برای فهمیدن سازوکار بات کلمه **dinfo** را در گروه ارسال کنید""")
        elif message.text == "demote":
            getwarnId = reply_to_message_id["id"]
            app.promote_chat_member(chat_id["id"], getwarnId , can_manage_chat=False)
            message.reply_text("کاربر مدنظر دیگر یک ادمین نیست")
    else:
        message.reply_text("🪐☄️سطح دسترسی را ندارید :: این امکان را فقط **sudo **میتواند اجرایی کند ::))")   
        
# mute with timer and mute and unmute
@app.on_message(filters.chat(TARGET) & filters.regex("mute"))
def muteAndUnmute(client, message):
    messsageText = message.text
    chat_id = app.get_chat(TARGET)
    reply_to_message_id=message.reply_to_message.from_user
    user_id = reply_to_message_id["id"]
    getwwarnId =  reply_to_message_id["first_name"]
    getwarnId = reply_to_message_id["id"]

    MENTIONGetter = f"[{getwwarnId}](tg://user?id={getwarnId})" 
    check = False
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break
    try:
        if check:
            if messsageText.count(" ") == 0:
                if message.text == "mute":
                    app.restrict_chat_member(chat_id["id"], user_id, ChatPermissions())
                    message.reply(f"""🪂این کاربر {MENTIONGetter} به صلاح دید یکی از ادمین ها میوت شد""")
                elif message.text == "unmute":
                    app.restrict_chat_member(chat_id["id"], user_id, ChatPermissions(can_send_messages=True,
                                                                                    can_send_media_messages=True,
                                                                                    can_send_stickers=True,
                                                                                    can_use_inline_bots=True,
                                                                                    can_send_animations=True))
                    message.reply("""🪂این کاربر {MENTIONGetter} به صلاح دید یکی از ادمین ها در دسترس قرار گرفت و قابلیت های زیر برای این کاربر فعال شد :
            1️⃣ارسال متن
            2️⃣ارسال محتوا 
            3️⃣ارسال استیکر و گیف
            4️⃣ارسال ربات اینلاین""")
            elif messsageText.count(" ") == 1:
                chat_id = app.get_chat(TARGET)
                reply_to_message_id=message.reply_to_message.from_user
                user_id = reply_to_message_id["id"]
                username = reply_to_message_id["username"]
                t = messsageText.split(" ")
                if t[0] == "mute":
                    hr24 = int(t[1])
                    app.restrict_chat_member(chat_id["id"], user_id, ChatPermissions())
                    message.reply_text(f"""
        ❌این کاربر با یوزرنیم @{username}  به صلاح دید یکی از ادمین ها  به مدت {hr24} ثانیه میوت شد  و از هرگونه چت و ارسال محتوا تا اتمام زمان منع شد.❌""")
                    app.restrict_chat_member(chat_id["id"], user_id, ChatPermissions() ,until_date=int(time() + hr24))
        else:
            message.reply_text("شما ادمین نیستید و سطح دسترسی را ندارید❌")
    except errors.exceptions.bad_request_400.UserAdminInvalid:
        message.reply_text("هیچ کس توان مقابله یا کاربر sudoer رو نداره")
        
# ban and unban user
@app.on_message(filters.chat(TARGET) & filters.regex("ban"))
def banAndunban(client, message):
    chat_id = app.get_chat(TARGET)
    reply_to_message_id=message.reply_to_message.from_user
    user_id = reply_to_message_id["id"]
    check = False
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break
    if check:
        if message.text == "unban":
            username = reply_to_message_id["username"]
            app.unban_chat_member(chat_id["id"], user_id)
            message.reply_text(f"""✅این کاربر با یوزرنیم @{username} صلاح دید یکی از ادمین ها توان عضویت مجدد در گروه دورهمی برنامه نویسان را دارد.""")
        
        elif message.text == "ban":
            username = reply_to_message_id["username"]
            app.kick_chat_member(chat_id["id"], user_id)
            message.reply_text(f"""❌این کاربر با یوزرنیم @{username} صورت کامل از گروه دورهمی برنامه نویسان حذف شد و تا تایید ادمین ها صورت نپزیرد توان عضو شدن مجدد را ندارد ..""")

    else:
        message.reply_text("❌شما ادمین نیستید و سطح دسترسی را ندارید❌")


@app.on_message(filters.chat(TARGET) & filters.regex("warn") & filters.reply)
def Warn(client , message):
    chat_id = app.get_chat(TARGET)
    reply_to_message_id=message.reply_to_message.from_user
    user_id = reply_to_message_id["id"]
    check = False
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break
    if check:
        if message.text == "warn":
            if message.from_user.id != user_id:
                AdminWarner = message.from_user.first_name
                warner = message.from_user.id

                getWarn =  reply_to_message_id["first_name"]
                getwarnId = reply_to_message_id["id"]

                MENTIONSender = f"[{AdminWarner}](tg://user?id={warner})" 
                MENTIONGetter = f"[{getWarn}](tg://user?id={getwarnId})"
                warnRate(user_id , reply_to_message_id["first_name"] , 1)
                if checkWarn(user_id):
                    app.kick_chat_member(chat_id["id"], getwarnId)
                    app.send_message(chat_id["id"] , f"""❌❌کاربر {MENTIONGetter} بدلیل داشتن __بیش از ۴ اخطار__ توسط بات از گروه اخراج میشید..""")
                text = f"🚫کاربر {MENTIONGetter} از کاربر {MENTIONSender} (سطح ادمین) یک اخطار دریافت کرد."
                message.reply_text(text)
        elif message.text == "removewarn":
            if message.from_user.id != user_id:
                AdminWarner = message.from_user.first_name
                warner = message.from_user.id

                getWarn =  reply_to_message_id["first_name"]
                getwarnId = reply_to_message_id["id"]

                MENTIONSender = f"[{AdminWarner}](tg://user?id={warner})" 
                MENTIONGetter = f"[{getWarn}](tg://user?id={getwarnId})"
                removeWarn(user_id , reply_to_message_id["first_name"] , 1)
                text = f"✅ کاربر {MENTIONSender} از کاربر {MENTIONGetter} (سطح ادمین) یک اخطار حذف کرد."
                message.reply_text(text)
    



@app.on_message(filters.chat(TARGET) & filters.regex("pin"))
def pin(client , message):
    AdminWarner = message.from_user.first_name
    warner = message.from_user.id
    check = False
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break
    if check:
        if message.text == "pin":
            MENTIONGetter = f"[{AdminWarner}](tg://user?id={warner})"
            message.reply_to_message.pin()
            message.reply_text(f"📌پیام مورد نظر یه صلاح دید ادمین {MENTIONGetter} پین شد.")
        elif message.text == "unpin":
            MENTIONGetter = f"[{AdminWarner}](tg://user?id={warner})"
            message.reply_to_message.unpin()
            message.reply_text(f"📍✂️پیام مورد نظر توسط ادمین {MENTIONGetter} آن پین شد")

    else:
        message.reply_text("❌شما ادمین نیستید و سطح دسترسی را ندارید❌")


@app.on_message(filters.chat(TARGET) & filters.regex("status"))
def Panel(client , message):
    if message.text == "status":
        con = sqlite3.connect('UserBase.db')
        cur = con.cursor()
        firstnameSennder = message.from_user.first_name
        sennderId = message.from_user.id
        MENTIONSender = f"[{firstnameSennder}](tg://user?id={sennderId})"
        warnTotal = 0
        scoreTotal = 0
        Sath = ""

        title = app.get_chat_member(TARGET , user_id=message.from_user.id).title
        if title == None:
            Sath = "سطح : notSudo"
        else:
            Sath = f"سطح : **{title}**"

        for row in cur.execute('SELECT * FROM Warn ORDER BY warnRate'):
            if int(row[0]) == sennderId:
                warnTotal = row[2]
               
        for row in cur.execute('SELECT * FROM Score ORDER BY Scorenumber'):
            if int(row[0]) == sennderId:
                scoreTotal = row[2]
                
        
        tex2t = f"""👨🏽‍🎤کاربر : {MENTIONSender}
شماره کاربری : {sennderId+22-46}

⛔️تعداد اخطار ها : {warnTotal}
✅تعداد امتیاز ها : {scoreTotal}

{Sath}"""
        message.reply_text(tex2t)

@app.on_message(filters.chat(TARGET) & filters.regex("github"))
def getInformation(client , message):
    messageText = message.text
    if messageText.count(" ") > 0:
        try:
            listOf = messageText.split(" ")
            response = requests.get(f"https://api.github.com/users/{listOf[1]}")
            result = response.json()
            coffee = result["public_repos"] - result["followers"] + 2
            hour = result["public_repos"] + result["following"] + 1
                       
            text = f"""📶github : github.com/{listOf[1]} & name is **{result["name"]}**

bio : 

__{result["bio"]}__

more information this user :

🧠followers : {result["followers"]}
🌍following : {result["following"]}


He has **{result["public_repos"]}** public repo so far. He also became a GitHub member on __{result["created_at"]}__ ...

So far, he has had ☕️ **{abs(coffee)}** cups of coffee and coded for ⏱ **{abs(hour)}** hours ...

More information in https://ug-search.herokuapp.com/user/{listOf[1]}"""
            message.reply_text(text)
        except:
            message.reply_text("🌍لطفا در وارد کردن یوزرنیم دقت کنید")
    

@app.on_message(filters.chat(TARGET) & filters.regex("infoscore"))
def whatScore(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)
    app.send_message(chat_id["id"] , """💡 برای تشکر از پیام یا کاربر مورد نظر کافیست عبارت + را در پیام کاربر مورد نظر ریپلای کنید 💡""")

@app.on_message(filters.chat(TARGET) & filters.regex("qinfo"))
def whatq(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)
    message.reply_text("""💡 لطفا سوال یا مشکل خود را به‌صورت دقیق‌تر و با جزئیات مطرح کنید تا بررسی بشه 💡

⭕️ برای اطلاعات بیشتر درمورد نحوه صحیح سوال پرسیدن، DontAskToAsk.ir را مطالعه کنید""" ,reply_to_message_id=message.reply_to_message.message_id)


@app.on_message(filters.chat(TARGET) & filters.regex("minfo"))
def whatmention(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)
    app.send_message(chat_id["id"] ,"""📵 لطفا از منشن کردن کاربران به‌جهت پاسخگویی به سوالات یا سایر موارد که منجر به ایجاد مزاحمت می‌شود خودداری کنید 📵""")


@app.on_message(filters.chat(TARGET) & filters.regex("dinfo"))
def whatdoc(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)
    message.reply_text("""🗄برای اطلاع از نحوه کارکرد ربات و‌ آشنایی به دستورات میتوانید داکیومنت مربوطه را مطالعه کنید

🔗 https://mehranalam.github.io/DevBax-bot/
""")

@app.on_message(filters.chat(TARGET) & filters.regex("captcha"))
def solveCaptcha(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)
    message.reply_text("""🏜لطفا به جهت جلوگیری از ریمو شدتان  اقدام به حل کپتچا فرمایید.""" ,reply_to_message_id=message.reply_to_message.message_id)
    
@app.on_message(filters.chat(TARGET) & filters.regex("off"))
def whatmention(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    app.delete_messages(chat_id["id"] , messageid)
    app.send_message(chat_id["id"] ,"""من خاموشم فعلا""")

@app.on_message(filters.chat(TARGET) & filters.reply)
def Score(client , message):
    chat_id = app.get_chat(TARGET)
    messageid = message.message_id
    reply_to_message_id=message.reply_to_message.from_user
    user_id = reply_to_message_id["id"]
    if reply_to_message_id["is_bot"] == False:
        if message.text == "+":
            app.delete_messages(chat_id["id"] , messageid)
            if message.from_user.id != user_id:
                firstnameSennder = message.from_user.first_name
                sennderId = message.from_user.id
                firstnamegetter =  reply_to_message_id["first_name"]
                getterId = reply_to_message_id["id"]
                MENTIONSender = f"[{firstnameSennder}](tg://user?id={sennderId})" 
                MENTIONGetter = f"[{firstnamegetter}](tg://user?id={getterId})" 
                scoreRate(user_id , reply_to_message_id["first_name"] , 1)
                message.reply_text(f"🧨کاربر {MENTIONGetter} از کاربر {MENTIONSender} به تعداد **یک امتیاز** دریافت کرد." , reply_to_message_id=message.reply_to_message.message_id)

@app.on_message(filters.chat(TARGET) & filters.regex("del"))
def del_msg(client ,message):
    chat_id = app.get_chat(TARGET)
    app.delete_messages(chat_id["id"],message.message_id)
    check = False
    for member in app.iter_chat_members(TARGET, filter="administrators"):
        if member.user.id == message.from_user.id:
            check = True
            break

    if check:
        if message.text.startswith("del"):
            counter = 0
            nums = message.text.split(' ')
            nums = abs(int(nums[1]))

            msg_id = message.message_id
            while counter != nums:
                if not client.delete_messages(message.chat.id, msg_id):
        
                    msg_id -= 1
                else:
                    counter += 1
            message.reply_text(f"""🔫به تعداد {counter} پیام از پیام های اخیر حذف شد""")
        elif message.text == "repdel":
            chat_id = app.get_chat(TARGET)
            app.delete_messages(chat_id["id"],message.reply_to_message.message_id)    


@app.on_message(filters.chat(TARGET) & filters.regex("commands"))
def showcommands(client, message):
    chat_id = app.get_chat(TARGET)
    app.delete_messages(chat_id["id"] , message.message_id)
    if message.text == "commands":
        app.send_message(chat_id["id"] ,
        """🌍دستورات فعال ربات بدین شرح است با کلیک روی هرکدام میتوانید از اعمال هرکدام آگاه شوید به بزرگی و کوچکی کلمات دقت کنید:)) 
 
🏪تعداد کل دستورات : 23 
🏟دستورات همگانی : 10 
🏰دستورات مدیر ها : 10""",  # Edit this
        reply_markup=InlineKeyboardMarkup(
            [
                [ 
                    InlineKeyboardButton(  
                        "+",
                        callback_data="+"
                    ),
                    InlineKeyboardButton(  
                        "infoscore",
                        callback_data="!+"
                    ),
                    InlineKeyboardButton(  
                        "ban",
                        callback_data="ban"
                    )
                ],
                [ 
                    InlineKeyboardButton(  
                        "unban",
                        callback_data="unban"
                    ),
                    InlineKeyboardButton(
                        "haskelhide",
                        callback_data="haskel"
                    ),
                    InlineKeyboardButton(  
                        "del COUNT",
                        callback_data="del"
                    )
                ],
                [ 
                    InlineKeyboardButton(
                        "mute",
                        callback_data="mute"
                    ),
                    InlineKeyboardButton( 
                        "mute time(second)",
                        callback_data="mutet"
                    ),
                    InlineKeyboardButton(  
                        "promote 2or3",
                        callback_data="promote"
                    )
                ],
                [ 
                    InlineKeyboardButton(  
                        "warn",
                        callback_data="warn"
                    ),
                    InlineKeyboardButton(
                        "minfo",
                        callback_data="!m"
                    ),
                    InlineKeyboardButton( 
                        "dinfo",
                        callback_data="!doc"
                    )
                ],
                [ 
                    InlineKeyboardButton(  
                        "qinfo",
                        callback_data="!q"
                    ),
                    InlineKeyboardButton(  
                        "pin",
                        callback_data="pin"
                    ),
                    InlineKeyboardButton(
                        "unpin",
                        callback_data="unpin"
                    )
                ],
                [ 
                    InlineKeyboardButton( 
                        "status",
                        callback_data="stat"
                    ),
                    InlineKeyboardButton(  
                        "github USERNAME",
                        callback_data="lit"
                    ),
                    InlineKeyboardButton( 
                        "removewarn",
                        callback_data="rmw"
                    )
                ],
                [
                    InlineKeyboardButton( 
                        "/create",
                        callback_data="/c"
                    ),
                    InlineKeyboardButton( 
                        "/update",
                        callback_data="/u"
                    ),
                    InlineKeyboardButton(
                        "unmute",
                        callback_data="unmute"
                    )
                ],
                [
                    InlineKeyboardButton( 
                        "commands",
                        callback_data="command"
                    )
                ],
                [
                    InlineKeyboardButton( 
                        "captcha",
                        callback_data="captcha"
                    )
                ]
                
            ]
        )
    )


@app.on_message(filters.regex("haskelhide"))
def hideChat(client , message):
    try:
        if message.text.startswith("haskelhide"):
            chat_id = app.get_chat(TARGET)
            message_text = message.text
            data_list = message_text.split("^")
            username_getter = data_list[1]
            Hide_data = data_list[2]
            id_user = app.get_users(username_getter)["id"]
            app.send_message(chat_id["id"], f"""🧛‍♂️یک پیام خصوصی از @{message.from_user.username} برای @{username_getter} میباشد.""",
            reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    "🔐 این یک پیام خصوصی است 🔐" ,
                                    callback_data=f"g_{id_user}_{Hide_data}_{message.from_user.id}"
                                )] ,
                                [InlineKeyboardButton(
                                    "🔓عمومی سازی" ,
                                    callback_data=f"g_{id_user}_{Hide_data}_{message.from_user.id}_g"
                                )]
                            ]
                        ))
    except errors.exceptions.bad_request_400.ButtonDataInvalid:
        message.reply_text("""🧛‍♂️ طول پیام حداکثر باید ۶۴ بایت باشد""")
    except errors.exceptions.bad_request_400.UsernameNotOccupied:
        message.reply_text("""🧛‍♂️ در وارد کردن یوزرنیم دفت به خرج دهید""")
    except errors.exceptions.bad_request_400.UsernameInvalid:
        message.reply_text("""🧛‍♂️ در وارد کردن یوزرنیم دفت به خرج دهید""")


app.run()
