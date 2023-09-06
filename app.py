import random

from aiogram import executor
import logging

from loader import dp, db, scheduler
import handlers
# from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    await db.create_tables()
    scheduler.start()
    scheduler.add_job(db.delete_all_from_saturday, "cron", day_of_week="sun", hour=0)
    await set_default_commands(dispatcher)
    # await on_startup_notify(dispatcher)


if __name__ == '__main__':
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO,
                        # filename="bot.log"
                        )
    executor.start_polling(dp, on_startup=on_startup)
