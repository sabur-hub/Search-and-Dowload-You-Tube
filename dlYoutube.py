from youtube_search import YoutubeSearch
from aiogram import *
from config import bot_token
import hashlib
from pytube import YouTube
import os

bot = Bot(bot_token)
dp = Dispatcher(bot)


def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res


@dp.message_handler(commands=["start"])
async def startmessage(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "hi i can download video with youtube\n you can send me link with video\n or "
                                    "write @dowloaderWithYoutubeBot and you video name")


@dp.inline_handler()
async def inline_handler(query : types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id =hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title = f'{link["title"]}',
        url = f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url = f'{link["thumbnails"][0]}',
        input_message_content = types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)


@dp.message_handler()
async def textMessage(message: types.Message):
    chat_id = message.chat.id
    url = message.text
    yt = YouTube(url)
    if message.text.startswith == 'https://www.youtube.com/' or 'https://youtu.be/':
        await bot.send_message(chat_id, f"Start dowloding: {yt.title}\n with this blog : [{yt.author}]({yt.channel_url}"
                               , parse_mode="Markdown")
        await dlVideo(url, message, bot)
    else:
        print('Your link not correct')


async def dlVideo(url, message, bot):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4")
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{yt.title}')
    with open(f"{message.chat.id}/{message.chat.id}_{yt.title}", 'rb') as video:
        await bot.send_video(message.chat.id, video, caption="this is your video", parse_mode='Markdown')
        os.remove(f"{message.chat.id}/{message.chat.id}_{yt.title}")


if __name__ == '__main__':
    executor.start_polling(dp)
