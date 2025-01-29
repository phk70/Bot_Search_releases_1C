from aiogram import Bot, Dispatcher









async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=os.getenv('URL'))