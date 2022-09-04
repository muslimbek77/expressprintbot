from keyboards.default.MenuKeyboard import menu
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart,Text, Regexp
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS,lang,PhoneRegx,regions
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove






@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    # await db.drop_users()
    try:
        user = await db.select_user(telegram_id=message.from_user.id)
    except:
        user = None
    
    print(user)
    if not user:

        await state.set_state('fullname')
        # await state.update_data({"full_name": message.from_user.full_name})
        await state.update_data({"username": message.from_user.username})
        await state.update_data({"telegram_id": message.from_user.id})

        await message.answer(f"Assalomu alaykum\nExpress print service rasmiy botiga xush kelibsiz!\nBotimizdan to'liq foydalanish uchun ro'yhatdan o'ting.")
        await message.answer('Ismingizni kiriting')
    else:
        await message.answer("Express print service rasmiy botiga xush kelibsiz!",reply_markup=menu)


@dp.message_handler(state = "fullname", content_types=types.ContentType.TEXT)
async def addname(message: types.Message, state: FSMContext):
    ru = list(lang.keys())[0]
    uz = list(lang.keys())[1]
    languages = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=ru),
            KeyboardButton(text=uz),
            
        ],
    ],
    resize_keyboard=True,
)
    full_name=message.text
    await state.set_state('language')
    await state.update_data({"full_name": full_name})
    
    await message.answer("Tilni tanlang.", reply_markup=languages)



@dp.message_handler(Text(list(lang.keys())),state = "language", content_types=types.ContentType.TEXT)
async def addlanguage(message: types.Message, state: FSMContext):
    user_language=lang[message.text]
    
    contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='☎️Telefon raqamni yuborish',request_contact=True)
            
        ],
    ],
    resize_keyboard=True,
)
    
    await state.set_state('phone_number')
    await state.update_data({"language": user_language})
    
    await message.answer("Telefon raqamingizni kiriting./Masalan: +9981234567",reply_markup=contact)

@dp.message_handler(state='phone_number',content_types='contact')
async def addpassword(message: types.Message, state: FSMContext):
    # print()
    phone_number = message.contact['phone_number']
    await state.update_data({"phone_number": phone_number})
    await state.set_state('address')
    address =  ReplyKeyboardMarkup(row_width=2)
    for i in regions:
        address.insert(
            KeyboardButton(text=i)
        )
    
    await message.answer("Yashash manzilingizni tanlang",reply_markup=address)
    

@dp.message_handler(Text(regions),state = "address", content_types=types.ContentType.TEXT)
async def addaddress(message: types.Message, state: FSMContext):
    myaddress = message.text
    data = await state.get_data()
    full_name = data.get("full_name")
    username = data.get("username")
    telegram_id = data.get("telegram_id")
    mylanguage = data.get("language")
    phone_number = data.get("phone_number")
    
    user = await db.add_user(telegram_id=telegram_id,
    full_name=full_name,username=username,mylanguage=mylanguage,myaddress=myaddress,phone_number=phone_number)
    print(user)
    await state.finish()
    
    await message.answer("Xush kelibsiz\nBotimizdan foydalanishingiz mumkin\n\n",reply_markup=menu)


# @dp.message_handler(state=['phone_number','address','language'])
# async def errorr(message: types.Message, state: FSMContext):
    
#     await message.answer("Noto\'g\'ri ma\'lumot kiritdingiz")
#     # try:
        
#     #     # user = await db.add_user(telegram_id=message.from_user.id,
#     #     #                          full_name=message.from_user.full_name,
#     #     #                          username=message.from_user.username)
#     # except asyncpg.exceptions.UniqueViolationError:
#     #     pass
#     #     # user = await db.select_user(telegram_id=message.from_user.id)

#     # await message.answer("Express print service rasmiy botiga xush kelibsiz.!")
    

#     # ADMINGA xabar beramiz
#     # count = await db.count_users()
#     # msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
#     # await bot.send_message(chat_id=ADMINS[0], text=msg)