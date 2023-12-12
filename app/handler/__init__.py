# CommandHandler:命令处理器
# MessageHandler:消息处理器
import logging

from telegram.ext import MessageHandler, filters
from telegram.ext._application import Application
from app.handler.commandHandler import new_chat_members


def register_all_handler(application: Application):
    # 添加命令处理器

    logging.warning("application register 'new_member_join' handler")
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_members))




def new_chat_members_filter(update):
    return update.message.new_chat_members is not None