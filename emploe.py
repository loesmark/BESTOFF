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
START_ROUTES, add_button_route_2, OPTION_ROUTE, charge_ROUTE2, charge_ROUTE = range(5)
ALL_MESSAGE_ROUTE,add_button_route,rimove_admin_ROUTE, add_button_route_3 = range(5, 9)
SPICIFIC_MESSAGE_ROUTE, SPICIFIC_MESSAGE_ROUTE2, SUBMET_TOP_ROUTE, SUBMET_TOP_ROUTE_2, submet_pop_ROUTE= range(9, 14)
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT = range(8)

connection_obj = sqlite3.connect('geek.db')
cursor_obj = connection_obj.cursor()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    x = cursor_obj.execute(f"SELECT * FROM users WHERE USER_ID = {user.id} AND HUB = 'admin'").fetchone()
    if x is None:
       pass
    else:
        keyboard = [
            [InlineKeyboardButton("تاكيد عملية", callback_data="submet ok")],
            [InlineKeyboardButton(" رفض عملية", callback_data="submet no")],
            [InlineKeyboardButton("رسالة خاصة", callback_data=str(THREE))],
            [InlineKeyboardButton("رسالة عامة", callback_data=str(FOUR))],
            [InlineKeyboardButton("شحن موزع", callback_data="hubb")],
            [InlineKeyboardButton("شحن مستخدم", callback_data="user")],
            [InlineKeyboardButton("تعديل معلومات", callback_data=str(SEVEN))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        await update.message.reply_text("لوحة التحكم", reply_markup=reply_markup)
        return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("تاكيد عملية", callback_data="submet ok")],
        [InlineKeyboardButton(" رفض عملية", callback_data="submet no")],
        [InlineKeyboardButton("رسالة خاصة", callback_data=str(THREE))],
        [InlineKeyboardButton("رسالة عامة", callback_data=str(FOUR))],
        [InlineKeyboardButton("شحن موزع", callback_data="hubb")],
        [InlineKeyboardButton("شحن مستخدم", callback_data="user")],
        [InlineKeyboardButton("تعديل معلومات", callback_data=str(SEVEN))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="القائمة الرئيسية", reply_markup=reply_markup)
    return START_ROUTES





async def submet_top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    context.user_data['type'] = query.data
    await query.answer()
    await query.edit_message_text(
        text="قم ب ارسال  ID المستخدم"
    )
    return SUBMET_TOP_ROUTE


async def submet_top_InFO(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text
    context.user_data['extra_data'] = message

    await update.message.reply_text(
        text="قم بارسال معلومات اللاعب"
    )
    return SUBMET_TOP_ROUTE_2


async def submet_top_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        typee = context.user_data.get('type')
        message = update.message.text
        id = context.user_data.get('extra_data')

        if not id:
            await update.message.reply_text("Error: No chat ID found. Please try again.")
            return START_ROUTES

        URL = f'https://api.telegram.org/bot{token_2}/sendMessage'
        payload = {
            'chat_id': str(id),
            'text': f"تم شحن الاعب {message}" if typee == "submet ok" else f"عذرا لم تنجح عملية الشحن الخاصة ب اللاعب {message}"
        }

        # Sending the request to the API
        response = requests.post(URL, data=payload)

        # Check for successful request
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        await update.message.reply_text("تم اعلام الزبون بنجاح /start")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        await update.message.reply_text("حدث خطاء في الاتصال بالخادم. حاول مرة اخرى /start")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        await update.message.reply_text("حدث خطاء في الطلب. حاول مرة اخرى /start")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        await update.message.reply_text("حدث خطاء غير متوقع. حاول مرة اخرى /start")

    return START_ROUTES


async def all_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="قم ب ارسال الرسالة المراد ارسالها للجميع"
    )
    return ALL_MESSAGE_ROUTE


async def all_message_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text
    try:
        # Fetch user IDs from the database
        user = cursor_obj.execute("SELECT USER_ID FROM users").fetchall()
    except Exception as e:
        logger.error(f"Database error: {e}")
        await update.message.reply_text("An error occurred while accessing the database. Please try again later.")
        return START_ROUTES

    URL = f'https://api.telegram.org/bot{token_2}/sendMessage'

    for i in user:
        payload = {
            'chat_id': str(i[0]),
            'text': message
        }
        try:
            # Send the request to the Telegram API
            response = requests.post(URL, data=payload)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for user {i[0]}: {e}")
            await update.message.reply_text(f"Failed to send message to user {i[0]}.")
            continue  # Skip to the next user

    await update.message.reply_text("Message sent successfully to all users.")
    return START_ROUTES


async def spicefick_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="قم ب ارسال الرسالة المراد ارسالها للزبون"
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
    context.user_data["type"] = query.data
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
    typee = context.user_data.get("type")
    id = update.message.text
    balncee = context.user_data.get("message")

    try:
        # Fetch the old balance
        if typee == "hubb":
            old_bal = cursor_obj.execute(f"SELECT BALANCE FROM USER_HUB WHERE USER_ID = {int(id)};").fetchone()
        else:
            old_bal = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {int(id)};").fetchone()

        # Check if old balance is None
        if old_bal is None:
            await update.message.reply_text("User not found. Please try again /start")
            return START_ROUTES

        # Calculate new balance
        try:
            balnce = float(balncee) + float(old_bal[0])
        except ValueError as ve:
            logging.error(f"ValueError: {ve}")
            await update.message.reply_text("Error: Invalid balance input. Please start over /start")
            return START_ROUTES

        # Update the balance in the database
        if typee == "hubb":
            cursor_obj.execute(f"UPDATE USER_HUB SET BALANCE = {float(balnce)} WHERE USER_ID = {int(id)};")
        else:
            cursor_obj.execute(f"UPDATE users SET BALANCE = {float(balnce)} WHERE USER_ID = {int(id)};")

        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            await update.message.reply_text("Customer charged successfully /start")
            connection_obj.commit()
            x = await notify_user(id, balncee, balnce)
            await update.message.reply_text( "تم اعلام الزبون" if x == 0 else "لم يتم اعلام الزبون"
)

        else:
            await update.message.reply_text("Error: Update failed. Please try again /start")

    except sqlite3.Error as db_error:
        logging.error(f"Database error: {db_error}")
        await update.message.reply_text("Error: Database operation failed. Please try again /start")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again /start")

    return START_ROUTES

async def notify_user(user_id: str, balncee: str, balnce: float):
    URL = f'https://api.telegram.org/bot{token_2}/sendMessage'
    payload = {
        'chat_id': str(user_id),
        'text': f"Added amount {balncee} to your balance. New balance is {balnce}"
    }
    response = requests.post(URL, data=payload)
    if response.status_code == 200:
        return 0
    else:
        logging.error(f"Failed to notify user: {response.status_code} - {response.text}")
        return 1


async def option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("تعديل سعر الصرف", callback_data=str(EIGHT))],
        [InlineKeyboardButton("اضافة زر", callback_data=str(ONE))],
        [InlineKeyboardButton("حذف زر", callback_data=str(TWO))],
        [InlineKeyboardButton("تفعيل زر", callback_data=str(THREE))],
        [InlineKeyboardButton("الغاء تفعيل زر", callback_data=str(FOUR))],
        [InlineKeyboardButton("اضافة موزع", callback_data=str(FIVE))],
        [InlineKeyboardButton("حذف موزع", callback_data=str(SIX))],
        [InlineKeyboardButton("اضافة admin", callback_data=str(SEVEN))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="control", reply_markup=reply_markup)
    return OPTION_ROUTE


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    x = query.data
    context.user_data["what"] = x
    await query.answer()

    try:
        # Attempt to convert x to an integer
        x_int = int(x)

        if x_int == 0:
            await query.edit_message_text(text="ارسل اسم الزر")
        elif x_int == 1:
            await query.edit_message_text(text="ارسل الزر المراد حذفه")
        elif x_int == 2:
            await query.edit_message_text(text="ارسل الزر المراد تفعيل")
        elif x_int == 3:
            await query.edit_message_text(text="ارسل الزر المراد الغاء تفعيله")
        elif x_int == 4:
            await query.edit_message_text(text="ارسل id الموزع للاضافة")
        elif x_int == 5:
            await query.edit_message_text(text="ارسل id الموزع للحذف")
        elif x_int == 6:
            await query.edit_message_text(text="ارسل id الادمن")
        elif x_int == 7:
            await query.edit_message_text(text="ارسل السعر")
        else:
            await query.edit_message_text(text="Invalid option selected.")

    except ValueError:
        # Handle the case where x cannot be converted to an integer
        await query.edit_message_text(text="Error: Invalid input. Please select a valid option.")
    except Exception as e:
        # Handle any other exceptions
        await query.edit_message_text(text=f"An unexpected error occurred: {str(e)}")

    return add_button_route


async def add_button_TYPE(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    typee = context.user_data.get("what")

    try:
        if typee is None:
            await update.message.reply_text(text="Error: No action specified.")
            return START_ROUTES

        typee = int(typee)  # Validate typee is an integer
        x = update.message.text

        if typee == 0:
            context.user_data["name"] = x
            await update.message.reply_text(text="Please send the button value.")
            return add_button_route_2

        elif typee in [1, 2, 3, 5, 6, 7]:
            # Common operation for delete/update
            if typee == 1:
                cursor_obj.execute(f'DELETE FROM BUTTON WHERE BUTTON_NAME ={x} ;')
            elif typee == 2:
                cursor_obj.execute(f"UPDATE BUTTON SET STATE = 1 WHERE BUTTON_NAME = '{x}';")
            elif typee == 3:
                cursor_obj.execute(f"UPDATE BUTTON SET STATE = 0 WHERE BUTTON_NAME = '{x}';")
            elif typee == 5:
                cursor_obj.execute(f"DELETE FROM USER_HUB WHERE USER_ID ={int(x)} ")
            elif typee == 6:
                cursor_obj.execute(f"UPDATE users SET HUB = 'admin' WHERE USER_ID = '{int(x)}';")
            elif typee == 7:
                cursor_obj.execute(f"UPDATE sy_price SET price_sy = {int(x)};")

            updated_rows = cursor_obj.rowcount
            if updated_rows == 1:
                connection_obj.commit()
                await update.message.reply_text(text="Operation successful.")
            else:
                await update.message.reply_text(text="Error: No rows affected.")

        elif typee == 4:
            button = cursor_obj.execute(f"SELECT * FROM users WHERE USER_ID = {int(x)};").fetchone()
            if button:
                cursor_obj.execute(f'''INSERT INTO USER_HUB(USER_NAME, First_Name, USER_ID, BALANCE) 
                    VALUES ({str(button[0])}, {str(button[1])}, {int(button[2])}, 0)''')
                updated_rows = cursor_obj.rowcount
                if updated_rows == 1:
                    connection_obj.commit()
                    await update.message.reply_text(text="User added successfully.")
                else:
                    await update.message.reply_text(text="Error: User not added.")
            else:
                await update.message.reply_text(text="Error: User not found.")

        else:
            await update.message.reply_text(text="Error: Invalid action type.")

    except ValueError as ve:
        await update.message.reply_text(text=f"Input error: {str(ve)}")
    except Exception as e:
        await update.message.reply_text(text="An unexpected error occurred.")
        print(f"Error: {str(e)}")  # Log the error for debugging

    return START_ROUTES


async def add_button_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    context.user_data["price"] = update.message.text
    await update.message.reply_text(text="ارسل نوع الزر")
    return add_button_route_3


async def add_button_DONE(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    Typee = update.message.text
    name = context.user_data.get("name")
    price = context.user_data.get("price")
    cursor_obj.execute(f'''INSERT INTO BUTTON(BUTTON_NAME, BUTTON_TYPE, STATE,price) 
            VALUES ('{str(Typee)}',' {str(name)}',1,{float(price)})''')
    updated_rows = cursor_obj.rowcount
    if updated_rows == 1:
        connection_obj.commit()
        await update.message.reply_text(text="ok START/")

    await update.message.reply_text(text="eroor START/")
    return START_ROUTES


async def rimove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    await update.message.reply_text(text="ارسل id الادمن المراد حذفه")
    return rimove_admin_ROUTE


async def rimove_admin_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    x = update.message.text
    cursor_obj.execute(f"UPDATE users SET HUB = 'null' WHERE USER_ID = '{int(x)}';")
    updated_rows = cursor_obj.rowcount
    if updated_rows == 1:
        connection_obj.commit()
        await update.message.reply_text(text="ok START/")

    await update.message.reply_text(text="eroor START/")
    return START_ROUTES


async def databasecopy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    file_path = 'geek.db'  # Update this path to your database file

    try:
        # Send the database file
        await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        await update.message.reply_text("Database file has been sent successfully.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await update.message.reply_text("Failed to send the database file.")

    return START_ROUTES




def main() -> None:
    application = Application.builder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(submet_top, pattern="^(submet)"),
                CallbackQueryHandler(submet_top, pattern="^(submet)"),
                CallbackQueryHandler(spicefick_message, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(all_message, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(charge, pattern="^(hub)"),
                CallbackQueryHandler(charge, pattern="^(user)"),
                CallbackQueryHandler(option, pattern="^" + str(SEVEN) + "$")
            ],
            SUBMET_TOP_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, submet_top_InFO),
            ],
            SUBMET_TOP_ROUTE_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, submet_top_done),
            ],

            ALL_MESSAGE_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, all_message_done),
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
            OPTION_ROUTE: [
                CallbackQueryHandler(add_button, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(SIX) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(SEVEN) + "$"),
                CallbackQueryHandler(add_button, pattern="^" + str(EIGHT) + "$"),
                MessageHandler(filters.Regex("^(super)"), rimove_admin),
                MessageHandler(filters.Regex("^(dtatbasecopy)"), databasecopy),
            ],
            add_button_route: [                MessageHandler(filters.TEXT & ~filters.COMMAND, add_button_TYPE),
            ],
            add_button_route_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_button_price),
            ],
            add_button_route_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_button_DONE),
            ],
            rimove_admin_ROUTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, rimove_admin_done),
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
