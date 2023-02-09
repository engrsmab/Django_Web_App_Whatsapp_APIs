import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Select Device", "Query Type"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Menu",
        reply_markup=markup,
    )

    return CHOOSING


async def regular_choice(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"{text.lower()}?")

    return TYPING_REPLY


async def regular_choice_test(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"{text.lower()} from choice test?")

    return TYPING_REPLY


async def custom_choice(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def received_information(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(
        "1998485541:AAHhj2MOxxzvhPvluPmOfqYokmCTde1jKvA").build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        "^(Select Device)$"), regular_choice
                ),
                MessageHandler(
                    filters.Regex(
                        "^(Query Type)$"), regular_choice_test
                )
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Done$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
