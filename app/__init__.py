# ApplicationBuilder:简单立即为构建 bot 对象
import logging
from telegram.ext import ApplicationBuilder
from app.config import BotConfig
# Application为被创建的bot
from telegram.ext._application import Application
from app.handler import register_all_handler

session = None


def create_application() -> Application:
    global session
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    # 设置日志
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s:%(message)s',
                        level=logging.ERROR)


    logging.warning(f'''
    ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪
    ♪♪                                                                                                      ♪♪
    ♪♪       ll       eeeeeee   eeeeeee   77777777     sssssss    bb          oooooooo      ttttttttt       ♪♪
    ♪♪       ll       ee   ee   ee   ee         77     ss    s    bb          oo    oo          tt          ♪♪
    ♪♪       ll       eeeeeee   eeeeeee        77        ss       bbbbbbbbb   oo    oo          tt          ♪♪
    ♪♪       ll       ee        ee            77       s    ss    bb     bb   oo    oo          tt          ♪♪
    ♪♪       llllll   eeeeeee   eeeeeee      77        sssssss    bbbbbbbbb   oooooooo          tt          ♪♪
    ♪♪                                                                                                      ♪♪
    ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪
    ''')

    # application = ApplicationBuilder().token(BotConfig.TOKEN).proxy_url(BotConfig.PROXY_URL).get_updates_proxy_url(BotConfig.PROXY_URL).build()
    logging.warning("application create start")
    application = ApplicationBuilder().token(BotConfig.TOKEN).build()
    logging.warning("application create finish\n")

    # 注册处理器
    logging.warning("register handler start")
    register_all_handler(application)
    logging.warning("register handler finish\n")


    return application
