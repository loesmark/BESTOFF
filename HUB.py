import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import requests
import sqlite3
import os

token = os.getenv('bot_token_1')
token_2 = os.getenv('bot_token_2')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
START_ROUTES, SPICIFIC_MESSAGE_ROUTE, charge_ROUTE2, charge_ROUTE, SPICIFIC_MESSAGE_ROUTE2 = range(5)
ONE, TWO = range(2)
connection_obj = sqlite3.connect('geek.db')
cursor_obj = connection_obj.cursor()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    x = cursor_obj.execute(f"SELECT BALANCE FROM USER_HUB WHERE USER_ID = {user.id} ").fetchone()
    if x is None:
       pass
    else:
        keyboard = [
            [InlineKeyboardButton("رسالة خاصة", callback_data=str(ONE))],
            [InlineKeyboardButton("شحن تاجر", callback_data=str(TWO))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await update.message.reply_text(f'''لوحة التحكم رصيدك هو 
        {x[0]}
''', reply_markup=reply_markup)
        return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("رسالة خاصة", callback_data=str(ONE))],
        [InlineKeyboardButton("شحن تاجر", callback_data=str(TWO))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="القائمة الرئيسية", reply_markup=reply_markup)
    return START_ROUTES



async def spicefick_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="قم بارسال الرسالة المراد ارسالها للزبون"
    )

    return SPICIFIC_MESSAGE_ROUTE


async def spicefick_message_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text
    context.user_data["message"] = message
    await update.message.reply_text("ارسل id الزبون ")
    return SPICIFIC_MESSAGE_ROUTE2


async def spicefick_message_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    id = update.message.text
    message = context.user_data.get("message")
    URL = f'https://api.telegram.org/bot{token_2}/sendMessage'
    payload = {
        'chat_id': str(id),
        'text': message
    }

    try:
        response = requests.post(URL, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        await update.message.reply_text("تم اعلام الزبون بنجاح /start")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        await update.message.reply_text("Failed to notify the user. Please check the user ID and try again.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("An unexpected error occurred while notifying the user.")

    return SPICIFIC_MESSAGE_ROUTE2



async def charge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="ادخل القيمة"
    )
    return charge_ROUTE


async def charge_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text
    context.user_data["message"] = message
    await update.message.reply_text("ارسل id الزبون ")
    return charge_ROUTE2


async def charge_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    id = update.message.text
    user = update.message.from_user
    charge = context.user_data.get("message")

    try:
        my_balance = cursor_obj.execute(f"SELECT BALANCE FROM USER_HUB WHERE USER_ID = {int(user.id)};").fetchone()
        user_bal = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {int(id)};").fetchone()

        if my_balance is None or user_bal is None:
            await update.message.reply_text("User balance not found. Please try again.")
            return START_ROUTES

        if float(charge) <= float(my_balance[0]):
            balnce = float(user_bal[0]) + float(charge)
            my_balance = float(my_balance[0]) - float(charge)

            cursor_obj.execute(f"UPDATE USER_HUB SET BALANCE = {float(my_balance)} WHERE USER_ID = {int(user.id)};")
            connection_obj.commit()

            cursor_obj.execute(f"UPDATE users SET BALANCE = {float(balnce)} WHERE USER_ID = {int(id)};")
            updated_rows = cursor_obj.rowcount

            if updated_rows == 1:
                connection_obj.commit()
                await update.message.reply_text("تم شحن الزبون بنجاح /start")
                URL = f'https://api.telegram.org/bot{token_2}/sendMessage'
                payload = {
                    'chat_id': str(id),
                    'text': f"تم اضافة مبلغ {charge} الى رصيدك واصبح {balnce}"
                }
                # إرسال الطلب إلى API
                response = requests.post(URL, data=payload)
                # التحقق من نجاح الطلب
                if response.status_code == 200:
                    await update.message.reply_text("تم اعلام الزبون بنجاح /start")
                else:
                    await update.message.reply_text("حدث خطأ اثناء اعلام الزبون /start")
            else:
                await update.message.reply_text("حدث خطأ اعد المحاولة /start")
        else:
            await update.message.reply_text(f'''رصيدك لا يكفي لعملية الشحن ان رصيدك هو 
            {my_balance[0]}
            الكمية المراد شحنها هي
            {charge}''')

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        await update.message.reply_text("Database error occurred. Please try again later.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")

    return START_ROUTES



def main() -> None:
    application = Application.builder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(spicefick_message, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(charge, pattern="^" + str(TWO) + "$"),
            ],
            SPICIFIC_MESSAGE_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, spicefick_message_id),
            ],
            SPICIFIC_MESSAGE_ROUTE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, spicefick_message_done),
            ],
            charge_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, charge_id),
            ],
            charge_ROUTE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, charge_done),
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
