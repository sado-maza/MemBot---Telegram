import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message,PollAnswer
from aiogram.filters import Command
from sql.sqlMemBot import increase_points,append_player
from Membot_class.createGame import GameSession
from aiogram.enums import PollType

from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

games: dict[int,'GameSession'] ={}



@dp.message(Command("start_game"))
async def start_game(message: Message):
    chat_id = message.chat.id
    if chat_id in games:
        return await message.answer("Игра уже идёт!")
    games[chat_id] = GameSession()
    await bot.send_message(chat_id,"Игра началась! Используй /join чтобы присоединиться")




@dp.message(Command("join"))
async def join(message: Message):
    chat_id = message.chat.id
    user = message.from_user
    session = games.get(chat_id)
    if not session or session.state_game != 'waiting':
        return await message.answer("Нельзя присоединиться сейчас.")
    if user.id in session.players:
        return await message.answer("Ты уже в игре.")
    session.players[user.id] = user.full_name
    session.points[user.id] = 0
    await bot.send_message(chat_id,f"{user.full_name} присоединился к игре!")
    append_player(user.id,user.full_name)




@dp.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    poll_id = poll_answer.poll_id
    user_id = poll_answer.user.id
    option_ids = poll_answer.option_ids
    for chat_id, session in games.items():
        if session.current_poll_id == poll_id:
            session.votes[user_id] = option_ids[0] 
            


@dp.message(Command("go"))
async def go(message: Message):
    chat_id = message.chat.id
    session = games.get(chat_id)
    await bot.send_message(chat_id,"На каждый раунд у вас 1 минута")
    if not session or len(session.players) < 1:
        return await message.answer("Нужно минимум 2 игрока.")
    if not session.next_round():
        return await message.answer("Игра окончена!")
    
    
    for round_num in range(10):
        phrase = session.list_pharese[session.nunber_round]
        session.nunber_round +=1
        await bot.send_message(chat_id, f"Раунд {round_num+1}\n{phrase}\n")
        await asyncio.sleep(40)


        poll_message = await bot.send_poll(
            chat_id=chat_id,
            question="Кто лучший мемолог данного раунда?",
            options=[str(p) for p in session.players.values()], 
            is_anonymous=False,
            type=PollType.REGULAR,
            allows_multiple_answers=False,
            close_date=20
        )
        session.current_poll_id = poll_message.poll.id
        session.votes = {}
        await asyncio.sleep(20)        

        winners = {}
        
        for voter_id, voted_index in session.votes.items():
            voted_id = list(session.players.keys())[voted_index]
            session.points[voted_id] += winners.get(voted_id, 0) + 1
           
    
    await bot.send_message(chat_id,"Игра закончена")
    sorted_points= dict(sorted(session.points.items(), key=lambda item:item[1],reverse=True))
    results_text = ""
    for tg_id, points in sorted_points.items():
        results_text += f"{session.players[tg_id]}: {points}\n"
        increase_points(tg_id, points)
    await bot.send_message(chat_id, f'Результаты:\n{results_text}')
    
    
    del games[chat_id]



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
