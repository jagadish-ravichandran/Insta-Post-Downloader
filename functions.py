from instagram_handler import InstaBot

async def start(update, context):
    chat_id = update.message.chat_id
    welcome_msg = f"Hello {update.effective_user.first_name}! \nI'm here to download instagram posts !"
    task_msg = "Send any instagram link !"
    await update.effective_message.reply_chat_action('typing')
    await context.bot.send_message(chat_id = chat_id, text = welcome_msg)
    await context.bot.send_message(chat_id = chat_id, text = task_msg)


# handling unexpected input from user
async def no_text(update, context):
    error_msg = "Only Instagram Links are allowed !"
    await update.effective_message.reply_chat_action('typing')
    await update.effective_message.reply_text(error_msg)


async def post_download(update, context):
    obj = InstaBot()
    url = update.message.text
    chat_id = update.effective_user.id
    result = obj.getPost(url)

    caption = result["caption"]
    await context.bot.send_message(chat_id=chat_id, text=caption)

    for media in result["resources"]:
        if media["type"] == "photo":
            await context.bot.send_photo(chat_id= chat_id, photo = media["download_url"])
        elif media["type"] == "video":
            await context.bot.send_video(chat_id= chat_id, video = media["download_url"])
    
    

    