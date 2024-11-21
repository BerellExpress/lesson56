import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = ''  #@BerellExpressLearningBot
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


@dp.message_handler(text="Calories")
async def set_age(massage):
    await massage.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(massage, state):
    data = await state.update_data(age=float(massage.text))
    await massage.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(massage, state):
    data = await state.update_data(growth=float(massage.text))
    await massage.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_sex(massage, state):
    data = await state.update_data(weight=float(massage.text))
    await massage.answer('Введите свой пол')
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def send_calories(massage, state):
    await state.update_data(sex=massage.text.lower())
    data = await state.get_data()
    if data['sex'] == 'мужчина':
        await massage.answer(
            f"Ваша норма калорий {10.0 * data['weight'] + 6.25 * data['growth'] - 5.0 * data['age'] + 5}")
    elif data['sex'] == 'женщина':
        await massage.answer(
            f"Ваша норма калорий {10.0 * data['weight'] + 6.25 * data['growth'] - 5.0 * data['age'] - 161}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
