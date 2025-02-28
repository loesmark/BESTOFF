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
import os
import emploe
import HUB

token = os.getenv('bot_token')


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
    try:
        x = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {user.id}").fetchone()

        await context.bot.send_message(chat_id='-1002364237348', text=f'''مستخدم جديد 
                   first name: {user.first_name}
                   username: {user.username}
                   user_id: {user.id}''')

        if x is None:
            button = cursor_obj.execute("SELECT USER_NAME FROM USER_HUB").fetchall()
            keyboard = [[InlineKeyboardButton("مخصص", callback_data=str(FOUR))]]
            for button_name in button:
                button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
                keyboard.append([button])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("الرجاء اختيار الموزع", reply_markup=reply_markup)
            return START_ROUTES_HUB
        else:
            button = cursor_obj.execute(
                "SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'main' and STATE = 1").fetchall()
            keyboard = [[InlineKeyboardButton("مخصص", callback_data=str(FOUR))]]
            for button_name in button:
                button = InlineKeyboardButton(button_name[0], callback_data=button_name[0])
                keyboard.append([button])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"القائمة الرئيسية رصيدك = {x[0]}", reply_markup=reply_markup)
            return START_ROUTES

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")
        return -1  # Indicate an error state



async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    querye = update.effective_user.id
    query = update.callback_query

    x = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {int(querye)}").fetchone()
    await query.answer()
    button = cursor_obj.execute("SELECT BUTTON_NAME FROM BUTTON WHERE BUTTON_TYPE = 'main' and STATE = 1").fetchall()
    keyboard = [[InlineKeyboardButton("مخصص", callback_data=str(FOUR))]]
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
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)

    try:
        # Database operation
        cursor_obj.execute(
            f'''INSERT INTO users(USER_NAME, First_Name, USER_ID, BALANCE, HUB) 
                VALUES ({user.username},{user.first_name}, {user.id}, 0, 'null')'''
        )
        connection_obj.commit()
        # Sending a message to the user
        await update.message.reply_text(text="/start ")

    except sqlite3.Error as db_error:
        logger.error("Database error occurred: %s", db_error)
        await update.message.reply_text(text="An error occurred while accessing the database. Please try again later.")

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        await update.message.reply_text(text="An unexpected error occurred. Please try again later.")



async def hub_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    user = update.message.from_user
    query = update.callback_query
    try:
        # Database operation
        cursor_obj.execute(
            f'''INSERT INTO users(USER_NAME, First_Name, USER_ID, BALANCE, HUB) 
                VALUES ('{str(user.username)}',' {str(user.first_name)}', {user.id}, 0, '{query.data}')''')
        connection_obj.commit()

        # Sending a message to the user
        await update.message.reply_text(text="/start ")

    except sqlite3.Error as db_error:
        logger.error("Database error occurred: %s", db_error)
        await update.message.reply_text(text="An error occurred while accessing the database. Please try again later.")

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        await update.message.reply_text(text="An unexpected error occurred. Please try again later.")


async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    message = update.message.from_user
    extra = context.user_data.get("extra_data")
    txt = update.message.text

    try:
        # Fetch user hub and balance
        hub = cursor_obj.execute(f"SELECT HUB FROM users WHERE USER_ID = {message.id}").fetchone()
        balance = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {message.id}").fetchone()
        price = cursor_obj.execute(f"SELECT price FROM BUTTON WHERE BUTTON_NAME = '{extra}'").fetchone()
        price_sy = cursor_obj.execute(f"SELECT price_sy FROM sy_price").fetchone()

        # Calculate total price
        price = float(price[0]) * float(price_sy[0])

        # Prepare keyboard for response
        keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Check if user has sufficient balance
        if float(balance[0]) >= price:
            await context.bot.send_message(chat_id='-1002364237348', text=f'''عملية شحن جديدة 
                {extra}
                {extra}
                player id : {txt}
                first name: {message.first_name}
                username: {message.username}
                user_id: {message.id}
                hub: {hub[0]}''')

            # Update user balance
            balance = float(balance[0] - price)
            cursor_obj.execute(f"UPDATE users SET BALANCE = {balance} WHERE USER_ID = {int(message.id)};")
            connection_obj.commit()
            await update.message.reply_text(
                f"لقد تم ارسال الطلب وخصم مبلغ {price} من رصيدك سوف يتم شحن حسابك في مدة اقصاها نصف ساعة",
                reply_markup=reply_markup)
        else:
            await update.message.reply_text("عذرا لاتملك رصيد كافي",
                                            reply_markup=reply_markup)

    except Exception as e:
        # Log the error for debugging
        logging.error(f"An error occurred: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")

    return START_ROUTES


async def submit_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    context.user_data['extra_data'] = query.data
    try:
        pricew = cursor_obj.execute(f"SELECT price FROM BUTTON WHERE BUTTON_NAME = '{query.data}'").fetchone()
        pricewt = cursor_obj.execute(f"SELECT price_sy FROM sy_price").fetchone()
        total = float(pricew[0] * float(pricewt[0]))
        keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"سعر هذه الخدمة {total} من اجل اكمال العملية ارسل id المراد شحنه",
                                      reply_markup=reply_markup)
        return PUBG_ROUTE

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")
        return START_ROUTES




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
    keyboard = [[InlineKeyboardButton("رجوع", callback_data=str(ONE))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        hub = cursor_obj.execute(f"SELECT HUB FROM users WHERE USER_ID = {user.id}").fetchone()
        await context.bot.send_message(chat_id='-1002364237348', text=f'''عملية شحن جديدة 
    {message}
    %%%%%%%
    first name: {user.first_name}
    usernaem: {user.username}
    user_id: {user.id}
    hub: {hub[0]}''')
        await update.message.reply_text("لقد تم ارسال الطلب سوف يتم شحن حسابك في مدة اقصاها نصف ساعة",reply_markup=reply_markup)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await update.message.reply_text(f"عذرا اعد المحاولة", reply_markup=reply_markup)

    return START_ROUTES



def main() -> None:
    application = Application.builder().token(token).build()
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
    conv_handler_HUB = ConversationHandler(
        entry_points=[CommandHandler("start_HUB", HUB.start)],
        states={
            HUB.START_ROUTES: [
                CallbackQueryHandler(HUB.spicefick_message, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(HUB.charge, pattern="^" + str(TWO) + "$"),
            ],
            HUB.SPICIFIC_MESSAGE_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, HUB.spicefick_message_id),
            ],
            HUB.SPICIFIC_MESSAGE_ROUTE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, HUB.spicefick_message_done),
            ],
            HUB.charge_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, HUB.charge_id),
            ],
            HUB.charge_ROUTE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, HUB.charge_done),
            ],
        },
        fallbacks=[CommandHandler("start_HUB", HUB.start)],
    )
    conv_handler_emp = ConversationHandler(
        entry_points=[CommandHandler("start_admin", emploe.start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(emploe.submet_top, pattern="^(submet)"),
                CallbackQueryHandler(emploe.submet_top, pattern="^(submet)"),
                CallbackQueryHandler(emploe.spicefick_message, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(emploe.all_message, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(emploe.charge, pattern="^(hub)"),
                CallbackQueryHandler(emploe.charge, pattern="^(user)"),
                CallbackQueryHandler(emploe.option, pattern="^" + str(emploe.SEVEN) + "$")
            ],
            emploe.SUBMET_TOP_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.submet_top_InFO),
            ],
            emploe.SUBMET_TOP_ROUTE_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.submet_top_done),
            ],

            emploe.ALL_MESSAGE_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.all_message_done),
            ],
            emploe.SPICIFIC_MESSAGE_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.spicefick_message_id),
            ],
            emploe.SPICIFIC_MESSAGE_ROUTE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.spicefick_message_done),
            ],
            emploe.charge_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.charge_id),
            ],
            emploe.charge_ROUTE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.charge_done),
            ],
            emploe.OPTION_ROUTE: [
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(emploe.FIVE) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(emploe.SIX) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(emploe.SEVEN) + "$"),
                CallbackQueryHandler(emploe.add_button, pattern="^" + str(emploe.EIGHT) + "$"),
                MessageHandler(filters.Regex("^(super)"), emploe.rimove_admin),
                MessageHandler(filters.Regex("^(dtatbasecopy)"), emploe.databasecopy),
            ],
            emploe.add_button_route: [MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.add_button_TYPE),
                               ],
            emploe.add_button_route_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.add_button_price),
            ],
            emploe.add_button_route_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.add_button_DONE),
            ],
            emploe.rimove_admin_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, emploe.rimove_admin_done),
            ],
        },
        fallbacks=[CommandHandler("start_admin", emploe.start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)
    application.add_handler(conv_handler_HUB)
    application.add_handler(conv_handler_emp)


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)




if __name__ == "__main__":

    main()




