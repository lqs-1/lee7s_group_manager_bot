# Update:从Telegram获取更新
import logging

import requests
from telegram import Update, BotCommand
from telegram.constants import ParseMode
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


# 清空消息
async def clean_channel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_name = context.args[0]
    message_id = int(context.args[1])

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"频道 {channel_name} 正在清空...")
    # 删除消息
    while True:
        try:
            message_id -= 1
            await context.bot.delete_message(chat_id=channel_name, message_id=message_id)
            if message_id == 0:
                break
        except Exception as e:

            pass

    await context.bot.delete_message(update.effective_chat.id, update.effective_message.id + 1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"频道 {channel_name} 已清空")
    # while True:
        # context.bot.delete_message(chat_id=channel_name, message_id=)




# 自动删除机器人消息
async def auto_delete_bot_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.channel_post.entities:
            # 发起获取字典的请求
            response = requests.get("https://nobibibi.top/back/sysDict/requestDictByParent/telegram_copy_dict")
            response_data = response.json().get("parentDictAllSonDict")

            # 不删除的互推机器人
            ignore_delete_bot_name_list = response_data.get('ignore_delete_bot_name').split(":")

            # 默认都要删除
            flag = True

            if len(ignore_delete_bot_name_list) > 0:

                for ignore_delete_bot_name in ignore_delete_bot_name_list:
                    if ignore_delete_bot_name in update.effective_message.text_html:
                        flag = False
            else:
                # 删除消息
                await context.bot.delete_message(update.effective_chat.id, update.channel_post.message_id)

            if flag:
                await context.bot.delete_message(update.effective_chat.id, update.channel_post.message_id)


    except Exception as e:
        pass


# 定时任务逻辑
async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """定时任务回调函数"""
    job = context.job

    # 发起获取字典的请求
    response = requests.get("https://nobibibi.top/back/sysDict/requestDictByParent/telegram_copy_dict")
    response_data = response.json().get("parentDictAllSonDict")

    # 获取有权执行命令的用户id 发送到这些id
    bot_member_count_send_ids = response_data.get('bot_member_count_send_ids').split(":")
    # 被统计的频道名
    bot_member_count_names = response_data.get('bot_member_count_channel_names').split(":")

    result = str()

    for bot_member_count_name in bot_member_count_names:
        chat_data = await context.bot.get_chat(chat_id=bot_member_count_name)
        chat_count = await context.bot.get_chat_member_count(chat_id=bot_member_count_name)
        result += f"[{chat_data.title}]({chat_data.link}): `{chat_count}`\n\n"


    for send_id in bot_member_count_send_ids:
        await context.bot.send_message(chat_id=send_id, text=result, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


# 如果定时任务存在就删除
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """删除定时任务"""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# 设置定时任务时间
async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """添加一个定时任务"""

    # commands = [
    #     BotCommand("start", "Start the bot"),
    #     BotCommand("help", "Get help")
    # ]
    #
    # await context.bot.set_my_commands(commands)

    # 发起获取字典的请求
    response = requests.get("https://nobibibi.top/back/sysDict/requestDictByParent/telegram_copy_dict")
    response_data = response.json().get("parentDictAllSonDict")

    # 获取有权执行命令的用户id 这些id可以控制
    bot_member_count_send_ids = response_data.get('bot_member_count_send_ids').split(":")
    send_ids = list()
    for send_id in bot_member_count_send_ids:
        send_ids.append(int(send_id))

    # 如果是开发者就返回机器人信息 如果是其他就返回错误信息
    if update.message.chat.id in send_ids:
        chat_id = update.effective_chat.id
        try:
            # 获取定时间隔时间
            timer = float(context.args[0])
            if timer < 0:
                await update.effective_message.reply_text("定时时间不能小于1秒")
                return

            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_repeating(alarm, interval=timer, first=1, name=str(chat_id))

            text = "定时任务设置成功"
            if job_removed:
                text += " 且删除了旧任务"
            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("设置失败 请重新设置")

    else:
        logging.info(f"用户 {update.message.chat.username} 妄图设置定时任务")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="无权限")


# 取消定时任务
async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """取消定时任务."""

    # 发起获取字典的请求
    response = requests.get("https://nobibibi.top/back/sysDict/requestDictByParent/telegram_copy_dict")
    response_data = response.json().get("parentDictAllSonDict")

    # 获取有权执行命令的用户id 这些id可以控制
    bot_member_count_send_ids = response_data.get('bot_member_count_send_ids').split(":")
    send_ids = list()
    for send_id in bot_member_count_send_ids:
        send_ids.append(int(send_id))

    if update.message.chat.id in send_ids:
        chat_id = update.effective_chat.id
        job_removed = remove_job_if_exists(str(chat_id), context)
        text = "任务取消成功" if job_removed else "你没有任务可以取消"
        await update.message.reply_text(text)

    else:
        logging.info(f"用户 {update.message.chat.username} 妄图取消定时任务")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="无权限")
