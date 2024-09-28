import asyncio, logging
import sys

from ModelQA import question_response, sbert_embeddings
from app.models.dialogs import Dialogs
from app.models.users import Users
from app.dao.dialogs import DialogsDAO
from app.dao.users import UsersDAO
from app.config import settings, APP_SCHEDULER

from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.filters import Command

from ai_yandex import NNBot

from utils_bot.utils import check_user, update_token

FOLDER_ID = 'b1g34c8hqja7kb5c93ci'

form_router = Router()
TOKEN = '7520967884:AAFcK4c8wfxpLNPKwkQSIXLnm0kiag0DhHU'
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.include_router(form_router)

aibot = NNBot(gpt_model="yandexgpt")

dialogs = dict()
users_data = {}


class Form(StatesGroup):
    state1 = State()


@form_router.business_message(Form.state1)
async def handle_fio(message: Message, state: FSMContext):
    await state.update_data(state1=message.text)
    await bot.send_chat_action(business_connection_id=message.business_connection_id,
                               chat_id=message.from_user.id, action='typing')
    await asyncio.sleep(3)
    await message.answer("Спасибо, дополнительно вам еще напишу и напомню. Если будут изменения также сообщу вам.")
    data = await state.get_data()
    print(data)
    await message.answer(f"Это будет в админ панели. \n {data}")


@form_router.message()
async def echo_handler(message: Message, state: FSMContext) -> None:

    try:
        user: Users = (await check_user(
            user_id=message.chat.id,
            business_id=message.business_connection_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        ))

        print(user)

        if message.chat.id not in dialogs.keys():
            dialogs[message.chat.id] = [{"role": "user",
                                             "text": message.text}]
        else:
            dialogs[message.chat.id].append({"role": "user",
                                         "text": message.text})

        dialog: Dialogs | None = await DialogsDAO.get_dialog(user.id)

        print(dialogs[message.chat.id])

        if dialog:
            dialog_info = aibot.analyze_dialog(FOLDER_ID, settings.IAM_TOKEN, dialogs[message.chat.id])

            await DialogsDAO.update(
                id_model=dialog.id,
                rating=dialog_info["rating"],
                comment=dialog_info["comment"],
                feedback_user=message.text
            )
            await message.answer("Спасибо за вашу оценку 😍! С каждым днем мы стараемся быть лучше для вас 💎")
        else:

            # sbert -> question_response(sbert_embeddings, inp_question)
            # yandex -> aibot.semantic_search(folder_id, iam_token)

            answer = aibot(FOLDER_ID, settings.IAM_TOKEN, dialogs[message.chat.id])

            if answer.get('flag') == 'call_manager':
                await message.answer(answer["text"])
                await UsersDAO.update(
                    id_model=user.id,
                    need_manager=True
                )
            elif answer.get('flag') == 'stop_dialog':
                await message.answer(answer["text"])
                pass
            else:
                if user.model_name == "sbert":
                    answer = question_response(sbert_embeddings, message.text)
                else:
                    answer = aibot.semantic_search(FOLDER_ID, settings.IAM_TOKEN, message.text)
                await message.answer(answer)
                await message.answer('Понравился ли вам ответ специалиста️️?')
                dialogs[message.chat.id].append({
                    "role": "assistant",
                    "text": answer
                })
                await DialogsDAO.add(
                    user_id=message.chat.id,
                    question=message.text,
                    answer=answer
                )
    except Exception as e:
            print(e)




@form_router.business_message()
async def echo_handler(message: Message, state: FSMContext) -> None:
    try:
        user: Users = (await check_user(
            user_id=message.chat.id,
            business_id=message.business_connection_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        ))

        print(user)

        if message.chat.id not in dialogs.keys():
            dialogs[message.chat.id] = [{"role": "user",
                                         "text": message.text}]
        else:
            dialogs[message.chat.id].append({"role": "user",
                                             "text": message.text})

        dialog: Dialogs | None = await DialogsDAO.get_dialog(user.id)

        print(dialogs[message.chat.id])

        if dialog:
            dialog_info = aibot.analyze_dialog(FOLDER_ID, settings.IAM_TOKEN, dialogs[message.chat.id])

            await DialogsDAO.update(
                id_model=dialog.id,
                rating=dialog_info["rating"],
                comment=dialog_info["comment"],
                feedback_user=message.text
            )
            await message.answer("Спасибо за вашу оценку 😍! С каждым днем мы стараемся быть лучше для вас 💎")
        else:

            # sbert -> question_response(sbert_embeddings, inp_question)
            # yandex -> aibot.semantic_search(folder_id, iam_token)

            answer = aibot(FOLDER_ID, settings.IAM_TOKEN, dialogs[message.chat.id])

            if answer.get('flag') == 'call_manager':
                await message.answer(answer["text"])
                await UsersDAO.update(
                    id_model=user.id,
                    need_manager=True
                )
            elif answer.get('flag') == 'stop_dialog':
                await message.answer(answer["text"])
                pass
            else:
                if user.model_name == "sbert":
                    answer = question_response(sbert_embeddings, message.text)
                else:
                    answer = aibot.semantic_search(FOLDER_ID, settings.IAM_TOKEN, message.text)
                await message.answer(answer)
                await message.answer('Понравился ли вам ответ специалиста️️?')
                dialogs[message.chat.id].append({
                    "role": "assistant",
                    "text": answer
                })
                await DialogsDAO.add(
                    user_id=message.chat.id,
                    question=message.text,
                    answer=answer
                )
    except Exception as e:
        print(e)


# @dp.message(lambda message: message.text in ["Да", "Нет"])
# async def handle_answer(message: Message):
#     """
#     Обработка ответа "Да" или "Нет"
#     """
#     if message.text == "Да":
#         await message.reply("Отлично! Вы выбрали модель с использованием RAG.")
#         users_data[message.chat.id] = 1
#     else:
#         await message.reply("Хорошо! Останемся на модели SBERT")


@dp.message(Command('sbert'))
async def start_message(message: Message):
    await message.answer("Отлично! Вы выбрали модель sbert!")
    # в бд модель
    user: Users = (await check_user(
        user_id=message.chat.id,
        business_id=message.business_connection_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    ))
    await UsersDAO.update(
        id_model=user.id,
        model_name="sbert"
    )
    #users_data[message.chat.id] = 1


@dp.message(Command('yandex'))
async def start_message(message: Message):
    # в бд модель
    await message.answer("Отлично! Вы выбрали модель yandex!")
    user: Users = (await check_user(
        user_id=message.chat.id,
        business_id=message.business_connection_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    ))
    await UsersDAO.update(
        id_model=user.id,
        model_name="yandex"
    )
    #users_data[message.chat.id] = 0


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет👋, {html.bold(message.from_user.full_name)}! Я виртуальный помощник и готов ответить на любые ваши вопросы! Чем могу помочь?")

    users_data[message.chat.id] = 0

async def main() -> None:
    # And the run events dispatching
    APP_SCHEDULER.start()
    await update_token()
    APP_SCHEDULER.add_job(
        update_token, trigger="interval", hours=6
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())