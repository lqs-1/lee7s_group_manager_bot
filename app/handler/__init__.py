# CommandHandler:命令处理器
# MessageHandler:消息处理器
import logging

from telegram.ext import MessageHandler, filters, CommandHandler
from telegram import BotCommand
from telegram.ext._application import Application
from app.handler.commandHandler import auto_delete_bot_message, new_chat_members, set_timer, unset, clean_channel_message

def register_all_handler(application: Application):
    # 添加命令处理器
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("clean", clean_channel_message))




    # logging.warning("application register 'new_member_join' handler")
    # application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_members))

    # logging.warning("application register 'auto_delete_bot_message' handler")
    application.add_handler(MessageHandler(filters.TEXT, auto_delete_bot_message))





def new_chat_members_filter(update):
    return update.message.new_chat_members is not None