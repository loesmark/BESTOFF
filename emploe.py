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
BOT_TOKEN = "7411899807:AAFkj7LY7r-16w1LDX9WwRxMFFqlWEyvttY"

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
    typee = context.user_data.get('type')
    if typee == "submet ok":
        message = update.message.text

        id = context.user_data.get('extra_data')
        URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': str(id),
            'text': f"تم شحن الاعب {message}"
        }
        # إرسال الطلب إلى API
        response = requests.post(URL, data=payload)
        # التحقق من نجاح الطلب
        if response.status_code == 200:
            await update.message.reply_text("تم اعلام الزبون بنجاح /start")
        else:
            await update.message.reply_text("حدث خطاء اعد المحاولة /start")
        return START_ROUTES
    else:
        message = update.message.text
        id = context.user_data.get('extra_data')
        URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': str(id),
            'text': f"عذرا لم تنجح عملية الشحن الخاصة ب اللاعب{message}"
        }
        # إرسال الطلب إلى API
        response = requests.post(URL, data=payload)
        # التحقق من نجاح الطلب
        if response.status_code == 200:
            await update.message.reply_text("تم اعلام الزبون بنجاح /start")
        else:
            await update.message.reply_text("حدث خطاء /start")
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
    user = cursor_obj.execute(f"SELECT USER_ID FROM users").fetchall()
    URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    for i in user:
        payload = {
            'chat_id': str(i[0]),
            'text': message
        }
        # إرسال الطلب إلى API
        requests.post(URL, data=payload)

    await update.message.reply_text("تم الارسال اضغط /start")

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
    URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': str(id),
        'text': message
    }
    # إرسال الطلب إلى API
    response = requests.post(URL, data=payload)
    # التحقق من نجاح الطلب
    if response.status_code == 200:
        await update.message.reply_text("تم اعلام الزبون بنجاح /start")
    else:
        await update.message.reply_text("حدث خطاء اعد المحاولة /start")

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
    if typee == "hubb":
        id = update.message.text
        balncee = context.user_data.get("message")
        old_bal = cursor_obj.execute(f"SELECT BALANCE FROM USER_HUB WHERE USER_ID = {int(id)};").fetchone()
        try:
            balnce =float(balncee) + float(old_bal[0])
        except:
            await update.message.reply_text("erorr /start")
            return START_ROUTES

        cursor_obj.execute(f"UPDATE USER_HUB SET BALANCE = {float(balnce)} WHERE USER_ID = {int(id)};")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            await update.message.reply_text("تم شحن الزبون بنجاح /start")
            connection_obj.commit()
            URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': str(id),
                'text': f"تم اضافة مبلغ كموزع {balncee} الى رصيدك واصبح {balnce}"
            }
            # إرسال الطلب إلى API
            response = requests.post(URL, data=payload)
            # التحقق من نجاح الطلب
            if response.status_code == 200:
                await update.message.reply_text("تم اعلام الزبون بنجاح /start")
            else:
                await update.message.reply_text("حدث خطاء اثناء اعلام الزبون start/")
        else:
            await update.message.reply_text("حدث خطاء اعد المحاولة /start")

    else:
        id = update.message.text
        balncee = context.user_data.get("message")
        old_bal = cursor_obj.execute(f"SELECT BALANCE FROM users WHERE USER_ID = {int(id)};").fetchone()
        try:
            balnce =float(balncee) + float(old_bal[0])
        except:
            await update.message.reply_text("erorr /start")
            return START_ROUTES

        cursor_obj.execute(f"UPDATE users SET BALANCE = {float(balnce)} WHERE USER_ID = {int(id)};")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            await update.message.reply_text("تم شحن الزبون بنجاح /start")
            connection_obj.commit()
            URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': str(id),
                'text': f"تم اضافة مبلغ {balncee} الى رصيدك واصبح {balnce}"
            }
            # إرسال الطلب إلى API
            response = requests.post(URL, data=payload)
            # التحقق من نجاح الطلب
            if response.status_code == 200:
                await update.message.reply_text("تم اعلام الزبون بنجاح /start")
            else:
                await update.message.reply_text("حدث خطاء اثناء اعلام الزبون /start")
        else:
            await update.message.reply_text("حدث خطاء اعد المحاولة /start")

    return START_ROUTES


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
    if x == 0:
        await query.edit_message_text(text="ارسل اسم الزر")

    elif int(x) == 1:
        await query.edit_message_text(text="ارسل الزر المراد حذفه")

    elif int(x) == 2:
        await query.edit_message_text(text="ارسل الزر المراد تفعيل")

    elif int(x) == 3:
        await query.edit_message_text(text="ارسل الزر المراد الغاء تفعيله")

    elif int(x) == 4:
        await query.edit_message_text(text="ارسل id الموزع للاضافة")

    elif int(x) == 5:
        await query.edit_message_text(text="ارسل id الموزع للحذف")

    elif int(x) == 6:
        await query.edit_message_text(text="ارسل id الادمن")
    elif int(x) == 7:
        await query.edit_message_text(text="ارسل السعر")

    return add_button_route





async def add_button_TYPE(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    typee = context.user_data.get("what")
    print("asd")
    if int(typee) == 0:
        context.user_data["name"] = update.message.text
        await update.message.reply_text(text="ارسل القيمة الزر")
        return add_button_route_2
    elif int(typee) == 1:
        x = update.message.text
        cursor_obj.execute(f'DELETE FROM BUTTON WHERE BUTTON_NAME ={x} ;')
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok dn START/")
            return START_ROUTES

        await update.message.reply_text(text="erorr  START/")
    elif int(typee) == 2:
        x = update.message.text
        cursor_obj.execute(f"UPDATE BUTTON SET STATE = 1 WHERE BUTTON_NAME = '{x}';")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok START/")
            return START_ROUTES

        await update.message.reply_text(text="eroor START/")
    elif int(typee) == 3:
        x = update.message.text
        cursor_obj.execute(f"UPDATE BUTTON SET STATE = 0 WHERE BUTTON_NAME = '{x}';")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok START/")
            return START_ROUTES

        await update.message.reply_text(text="eroor START/")

    elif int(typee) == 4:
        x = update.message.text
        button = cursor_obj.execute(f"SELECT * FROM users WHERE USER_ID = {int(x)} ").fetchone()
        cursor_obj.execute(f'''INSERT INTO USER_HUB(USER_NAME, First_Name, USER_ID,BALANCE) 
            VALUES ('{str(button[0])}',' {str(button[1])}',{int(button[2])},0)''')
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok START/")
            return START_ROUTES

        await update.message.reply_text(text="eroor START/")

    elif int(typee) == 5:
        x = update.message.text
        cursor_obj.execute(f"DELETE FROM USER_HUB WHERE USER_ID ={int(x)} ")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok START/")
            return START_ROUTES

        await update.message.reply_text(text="eroor START/")
    elif int(typee) == 6:
        x = update.message.text
        cursor_obj.execute(f"UPDATE users SET HUB = 'admin' WHERE USER_ID = '{int(x)}';")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok START/")
            return START_ROUTES
        await update.message.reply_text(text="eroor START/")
    elif int(typee) == 7:
        x = update.message.text
        cursor_obj.execute(f"UPDATE sy_price SET price_sy = {int(x)};")
        updated_rows = cursor_obj.rowcount
        if updated_rows == 1:
            connection_obj.commit()
            await update.message.reply_text(text="ok START/")
            return START_ROUTES
        await update.message.reply_text(text="eroor START/")

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
    cursor_obj.execute(f'''INSERT INTO BUTTON(BUTTON_NAME, BUTTON_TYPE, STATE,price) 
            VALUES ('{str(Typee)}',' {str(name)}',1,)''')
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


def main() -> None:
    application = Application.builder().token("7233560953:AAFkQ-KRoRNjz8O93U4hVlF57b6XioZLl6w").build()
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
            ],
            add_button_route: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_button_TYPE),
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
