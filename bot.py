from telebot.async_telebot import AsyncTeleBot as atb
from Config import config

bot = atb(
    config.TOKEN,
    parse_mode="MarkdownV2"
)

Dev = [6239769036]
