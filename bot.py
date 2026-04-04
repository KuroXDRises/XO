from telebot.async_telebot import AsyncTeleBot as atb
from Config import config
class main(atb):
    def __init__():
        super().__init__(
            config.TOKEN,
            parse_mode="Markdown"
        )
bot = main
