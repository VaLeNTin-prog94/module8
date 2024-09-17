from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
kb.add(button1)
kb.add(button2)
kb.add(button3)

kbInline = InlineKeyboardMarkup(resize_keyboard=True)
button4 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
button5 = InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas')
kbInline.add(button4)
kbInline.add(button5)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


buy_Inline = InlineKeyboardMarkup(resize_keyboard=True)
pr1 = InlineKeyboardButton(text="Product1", callback_data='product_buying')
pr2 = InlineKeyboardButton(text="Product2", callback_data='product_buying')
pr3 = InlineKeyboardButton(text="Product3", callback_data='product_buying')
pr4 = InlineKeyboardButton(text="Product4", callback_data='product_buying')
buy_Inline.add(pr1)
buy_Inline.add(pr2)
buy_Inline.add(pr3)
buy_Inline.add(pr4)
@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for number in range(1,5):
        with open(f'module14/{number}.png',"rb") as img:
            await message.answer_photo(img,f"Название{number} | Описание: описание {number} | Цена {number*100}")
    await message.answer("Выберите продукт для покупки:",reply_markup=buy_Inline)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kbInline)


@dp.callback_query_handler(text='formulas')
async def infor(call):
    await call.message.answer("для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;"
                              "для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.")
    await call.answer()


@dp.message_handler(commands=['start'])
async def star_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:'")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ваша нома калорий  {10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}")
    await state.finish()


executor.start_polling(dp, skip_updates=True)
