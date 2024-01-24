# Update:从Telegram获取更新
import logging

from telegram import Update
# ContextTypes:上下文类型
from telegram.ext import ContextTypes


# 新成员
async def new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)

    if bot_member.status == 'administrator':

        new_members = update.message.new_chat_members

        for member in new_members:
            # 执行您希望在新成员加入时进行的操作
            if context.bot.id == member.id:
                continue
            logging.warning(f"用户 {member.username} 进入群聊")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"@{member.username} 欢迎欢迎🎉🎉\n 关注频道 https://t.me/av_share_channel")



# 自动删除机器人消息
async def auto_delete_bot_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.channel_post.entities:
            await context.bot.delete_message(update.effective_chat.id, update.channel_post.message_id)

    except Exception as e:
        pass
