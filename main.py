import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
import sqlite3


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
START_ROUTES, PUBG_ROUTE, FREEFIRE_ROUTE, JOWAKER_ROUTE, BIGOLIVE_ROUTE, START_ROUTES_HUB, submit_W_route, charge_route = range(8)

ONE, TWO, THREE, FOUR  = range(4)

connection_obj = sqlite3.connect('geek.db')
cursor_obj = connection_obj.cursor()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    x = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {user.id}").fetchone()
    if x is None:
        button = cursor_obj.execute("SELECT USER_NAME FROM USER_HUB").fetchall()
        keyboard = [[InlineKeyboardButton("مخصص", callback_data=str(FOUR))]]
        for button_name in button:
            button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await update.message.reply_text("الرجاء اختيار الموزع", reply_markup=reply_markup)
        return START_ROUTES_HUB
    else:
        button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'main' and STATE = 1").fetchall()
        keyboard = [[InlineKeyboardButton("مخصص", callback_data=str(FOUR)),InlineKeyboardButton("شحن رصيد", callback_data=str(ONE))]]
        for button_name in button:
            button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await update.message.reply_text(f"القائمة الرئيسية رصيدك = {x[0]}", reply_markup=reply_markup)
        return START_ROUTES




async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    querye = update.effective_user.id
    query = update.callback_query

    x = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {int(querye)}").fetchone()
    await query.answer()
    button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'main' and STATE = 1").fetchall()
    keyboard = [[InlineKeyboardButton("مخصص", callback_data=str(FOUR)),InlineKeyboardButton("شحن رصيد", callback_data=str(ONE))]]
    for button_name in button:
        button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text=f"القائمة الرئيسية رصيدك = {x[0]}", reply_markup=reply_markup)
    return START_ROUTES


async def PUBG(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    await query.answer()
    button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'pubg' and STATE = 1").fetchall()
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    for button_name in button:
        button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="اختر الكمية", reply_markup=reply_markup)
    return PUBG_ROUTE


async def FREEFIRE(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'fire' and STATE = 1").fetchall()
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    for button_name in button:
        button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="اختر الكمية", reply_markup=reply_markup)
    return FREEFIRE_ROUTE


async def JOWAKER(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'jawaker' and STATE = 1").fetchall()
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    for button_name in button:
        button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="اختر الكمية", reply_markup=reply_markup)
    return JOWAKER_ROUTE


async def BIGOLIVE(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    await query.answer()
    button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'BIGO' and STATE = 1").fetchall()
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    for button_name in button:
        button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="اختر الكمية", reply_markup=reply_markup)
    return BIGOLIVE_ROUTE


async def no_hub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    cursor_obj.execute(
        f'''INSERT INTO users(USER_NAME, First_Name, USER_ID, BALANCE, HUB) 
            VALUES ('{str(user.username)}',' {str(user.first_name)}', {user.id}, 0,'null')''')
    connection_obj.commit()
    await update.message.reply_text(text="/start ")



async def hub_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    user = update.message.from_user
    query = update.callback_query
    logger.info("User %s started the conversation.", user.first_name)
    cursor_obj.execute(
        f'''INSERT INTO users(USER_NAME, First_Name, USER_ID, BALANCE, HUB) 
        VALUES ('{str(user.username)}',' {str(user.first_name)}', {user.id}, 0, '{query.data}')''')
    connection_obj.commit()
    await query.answer()
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="/start ")


async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    messsage = update.message.from_user
    extra = context.user_data.get("extra_data")
    txt = update.message.text
    hub = cursor_obj.execute(f"SELECT HUB FROM users WHERE USER_ID = {messsage.id}").fetchone()
    balnce = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {messsage.id}").fetchone()
    price = cursor_obj.execute(f"SELECT price FROM BUTTON WHERE BUTTON_NAME = '{extra}'").fetchone()
    price_sy = cursor_obj.execute(f"SELECT price_sy FROM sy_price").fetchone()
    price = float(price[0]) * float(price_sy[0])
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if float(balnce[0]) >= price:
        await context.bot.send_message(chat_id='-1002364237348', text=f'''عملية شحن جديدة 
            {extra}
            {extra}
            plyer id : {txt}
            first name: {messsage.first_name}
            usernaem: {messsage.username}
            user_id: {messsage.id}
            hub: {hub[0]}''')
        balnce = float(balnce[0] - price)
        cursor_obj.execute(f"UPDATE users SET BALANCE = {balnce} WHERE USER_ID = {int(messsage.id)};")
        connection_obj.commit()
        await update.message.reply_text(f"لقد تم ارسال الطلب وخصم مبلغ {price} من رصيدك سوف يتم شحن حسابك في مدة اقصاها نصف ساعة",
                                        reply_markup=reply_markup, )


    else:
        await update.message.reply_text("عذرا لاتملك رصيد كافي",
                                        reply_markup=reply_markup, )

    return START_ROUTES


async def submit_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    context.user_data['extra_data'] = query.data
    pricew = cursor_obj.execute(f"SELECT price FROM BUTTON WHERE BUTTON_NAME = '{query.data}'").fetchone()
    pricewt = cursor_obj.execute(f"SELECT price_sy FROM sy_price").fetchone()
    total = float(pricew[0]*float(pricewt[0]))
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"سعر هذه الخدمة {total} من اجل اكمال العملية ارسل id المراد شحنه",reply_markup=reply_markup)
    return PUBG_ROUTE


async def submit_W(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("ارسل المعلومات التي تريدها حول الخدمة مع كافة التفاصيل في رسالة واحدة",reply_markup=reply_markup)
    return submit_W_route


async def s_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    message = update.message.text
    user = update.message.from_user
    hub = cursor_obj.execute(f"SELECT HUB FROM users WHERE USER_ID = {user.id}").fetchone()
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await context.bot.send_message(chat_id='-1002152211375', text=f'''عملية شحن جديدة 
    {message}
    %%%%%%%
    first name: {user.first_name}
    usernaem: {user.username}
    user_id: {user.id}
    hub: {hub[0]}''')
        await update.message.reply_text("لقد تم ارسال الطلب سوف يتم شحن حسابك في مدة اقصاها نصف ساعة",reply_markup=reply_markup)
    except:
        await update.message.reply_text("عذرا اعد المحاولة",reply_markup=reply_markup)
    return START_ROUTES



def main() -> None:
    application = Application.builder().token("7411899807:AAFkj7LY7r-16w1LDX9WwRxMFFqlWEyvttY").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(PUBG, pattern="^(PUBG)"),
                CallbackQueryHandler(FREEFIRE, pattern="^(FREE)"),
                CallbackQueryHandler(JOWAKER, pattern="^(jawaker)"),
                CallbackQueryHandler(BIGOLIVE, pattern="^(BIGO)"),
                CallbackQueryHandler(submit_W, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
            ],
            START_ROUTES_HUB: [
                CallbackQueryHandler(hub_fun),
                MessageHandler(filters.TEXT & ~filters.COMMAND,no_hub),
            ],
            PUBG_ROUTE: [
                CallbackQueryHandler(submit_id, pattern="^(pubg)"),
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, submit),
            ],
            FREEFIRE_ROUTE: [
                CallbackQueryHandler(submit_id, pattern="^(free)"),
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, submit),
            ],
            JOWAKER_ROUTE: [
                CallbackQueryHandler(submit_id, pattern="^(jawaker)"),
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, submit),
            ],
            BIGOLIVE_ROUTE: [
                CallbackQueryHandler(submit_id, pattern="^(pubg)"),
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, submit),
            ],
            submit_W_route: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,s_submit),
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)




if __name__ == "__main__":
    main()




