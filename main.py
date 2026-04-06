from dotenv import load_dotenv
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import openai
import sys

load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class Reference:

    '''
    A class to store previouly response from the open API

    '''

    def __init__(self) -> None:
        self.response = ""

reference = Reference()

model_name = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()




def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dp.message(Command('clear'))
async def clear(message: Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dp.message(Command('start'))
async def welcome(message: Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\n"
    "I am Tele Bot!\n"
    "Created by Yoosuf.\n"
    "How can I assist you?")


@dp.message(Command('help'))
async def helper(message: Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm Telegram bot created by Yoosuf! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)



@dp.message()
async def chatgpt(message: Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = model_name,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)



# Run the bot
async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())