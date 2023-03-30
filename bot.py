from telegram.ext import Application, CommandHandler, MessageHandler, filters
from functions import start, post_download, no_text
from decouple import config


def main():
    TOKEN = config("BOT_TOKEN")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(MessageHandler(filters.Regex(r'^https://www.instagram.com/.*'),post_download))
    application.add_handler(MessageHandler(filters.ALL,no_text))
    application.run_polling()


if __name__ == "__main__":
    main()

