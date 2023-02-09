from MessageStore.helper import get_data, set_language, language, get_device, set_alarm, get_group
from django.core.management.base import BaseCommand
import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

TOKEN = os.environ.get('TOKEN')
# TOKEN = '1998485541:AAHhj2MOxxzvhPvluPmOfqYokmCTde1jKvA'

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, CALL_BACK, SET_LANG = range(5)

reply_keyboard = [
    ["Group", "Device", "Type", ],
    ["Language", 'Get id', "Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(update.effective_user.id, reply_markup=ReplyKeyboardRemove(),)

    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f'Typing: <i>menu</i> to show Menu\r\n Typing: <i>/help</i> if there is any error\r\nTyping: <i>/alarm</i> for activate or deactivate alarm',
                                    reply_markup=ReplyKeyboardRemove(),
                                    parse_mode='HTML')


async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f'Typing: <i>menu</i> to show Menu\r\n Typing: <i>/help</i> if there is any error\r\nTyping: <i>/alarm</i> for activate or deactivate alarm',
                                    reply_markup=ReplyKeyboardRemove(),
                                    parse_mode='HTML')
    return ConversationHandler.END


async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    languages = await language()
    keyboard = []
    for item in languages:
        keyboard.append([InlineKeyboardButton(f"{item}", callback_data=item)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Set Language:", reply_markup=reply_markup)

    return SET_LANG


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await set_language(update.effective_user.id, query.data)
    await query.message.reply_text("ok", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Menu",
        reply_markup=markup,
    )

    return CHOOSING


async def select_device(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    try:
        if context.user_data['Group']:
            devices = await get_device(context.user_data['Group'])
            keyboard = []
            for device in devices:
                keyboard.append([InlineKeyboardButton('{0} ({1})'.format(
                    device[0], device[1]), callback_data=device[2])])
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text("Select device:", reply_markup=reply_markup)

            return CALL_BACK
    except:
        pass
    await update.message.reply_text("Please choose <b>Group</b>!", reply_markup=markup, parse_mode='HTML')
    return CHOOSING


async def select_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    groups = await get_group(update.effective_user.id)
    keyboard = []
    for group in groups:
        keyboard.append([InlineKeyboardButton('{0}({1})'.format(
            group[0], group[1]), callback_data=group[2])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select Group:", reply_markup=reply_markup)

    return CALL_BACK


async def select_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    keyboard = [
        [InlineKeyboardButton('General state ', callback_data="1")],
        [InlineKeyboardButton('Temperature ', callback_data="2")],
        [InlineKeyboardButton('Wind ', callback_data="3")],
        [InlineKeyboardButton('Gas', callback_data="4")],
        [InlineKeyboardButton('Machine state', callback_data="5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Select Type:", reply_markup=reply_markup)

    return CALL_BACK


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        'Done',
        reply_markup=markup,
    )

    return CHOOSING


async def _callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_data = context.user_data
    text = query.data
    category = user_data["choice"]
    user_data[category] = text
    try:
        if context.user_data['Device'] and context.user_data['Type']:
            await query.message.reply_text("Please choose <b>Done</b>!", reply_markup=markup, parse_mode='HTML')
            return CHOOSING
    except:
        pass
    try:
        if context.user_data['Device']:
            await query.message.reply_text("Please choose <b>Type</b>!", reply_markup=markup, parse_mode='HTML')
            return CHOOSING
    except:
        pass
    try:
        if context.user_data['Type']:
            await query.message.reply_text("Please choose <b>Device</b>!", reply_markup=markup, parse_mode='HTML')
            return CHOOSING
    except:
        pass
    try:
        if context.user_data['Group']:
            await query.message.reply_text("Please choose <b>Device</b>!", reply_markup=markup, parse_mode='HTML')
            return CHOOSING
    except:
        pass


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    try:
        result = await get_data(update.effective_user.id, user_data['Device'], user_data['Type'])
    except:
        result = 'Error'
    if "choice" in user_data:
        del user_data["choice"]
    await update.message.reply_text(
        f'{result}',
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML'
    )

    user_data.clear()
    return ConversationHandler.END

# set alarm


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Alarm ON", callback_data="ON"),
            InlineKeyboardButton("Alarm OFF", callback_data="OFF"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Alarm Set:", reply_markup=reply_markup)


async def button_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()
    await set_alarm(update.effective_user.id, query.data)
    if query.data == "ON":
        reply = "Alarm ON"
        await query.edit_message_text(text=f"{reply}")
    if query.data == "OFF":
        reply = "Alarm OFF"
        await query.edit_message_text(text=f"{reply}")

# end alarm


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex(
                "^(menu|Menu)$"), menu
        )],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        "^(Device)$"), select_device
                ),
                MessageHandler(
                    filters.Regex(
                        "^(Type)$"), select_type
                ),
                MessageHandler(
                    filters.Regex(
                        "^(Group)$"), select_group
                ),
                MessageHandler(
                    filters.Regex(
                        "^(Language)$"), lang
                ),
                MessageHandler(
                    filters.Regex(
                        "^(Get id)$"), get_id
                ),
                CommandHandler('help', help_menu)
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    received_information,
                ),
                CommandHandler('help', help_menu)
            ],
            CALL_BACK: [
                CallbackQueryHandler(_callback),
                CommandHandler('help', help_menu)
            ],
            SET_LANG: [
                CallbackQueryHandler(button),
                CommandHandler('help', help_menu)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done), ],
    )
    application.add_handler(conv_handler, group=1)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler("alarm", alarm), group=0)
    application.add_handler(CallbackQueryHandler(button_alarm), group=0)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        main()
