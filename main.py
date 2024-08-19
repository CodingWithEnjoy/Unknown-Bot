from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = '7407944412:AAGkvS0eVPxk1pW0shpWN8lkA0bbGqbZWmI'
ADMIN_CHAT_ID = '956251226'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! You can send messages or files, and I will forward them to the admin.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    message = update.message.text or 'Sent a file.'

    if update.message.text:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Message from {user.username or user.first_name}:\n{message}")
    elif update.message.document:
        document = update.message.document
        await context.bot.send_document(chat_id=ADMIN_CHAT_ID, document=document.file_id, caption=f"Document from {user.username or user.first_name}")
    elif update.message.photo:
        photo = update.message.photo[-1]
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo.file_id, caption=f"Photo from {user.username or user.first_name}")
    else:
        await update.message.reply_text("Unsupported message type.")

    await update.message.reply_text('Your message has been sent to the admin.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
