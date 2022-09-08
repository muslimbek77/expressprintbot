import asyncio
from keyboards.default.MenuKeyboard import menu
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp, db, bot
from keyboards.default.MenuKeyboard import admin

@dp.message_handler(user_id=ADMINS,text="/admin")
async def send_ad_command(message: types.Message, state: FSMContext):

    await message.answer("Admin panel", reply_markup=admin)

@dp.message_handler(user_id=ADMINS,text="Reklama")
async def send_ad_command(message: types.Message, state: FSMContext):
    print(ADMINS)
    await message.answer("Reklama yuborishingiz mumkin...")
    await state.set_state("advertisement")


@dp.message_handler(state = "advertisement", content_types=types.ContentType.ANY)
async def sending_advert(message: types.Message, state: FSMContext):
    await state.finish()
    users = await db.select_all_users()
    count = await db.count_users()
    
        
    for user in users:
        print(user)
        user_id = user[3]
        try:
            await bot.copy_message(user_id, message.chat.id, message.message_id, reply_markup=message.reply_markup)
            await asyncio.sleep(0.05)
        except:
            pass

    await message.answer(f"{count}ta foydalanuvchiga reklama yuborildi.")
    
    
    
    
#maxsulot qo'shish/ kategoriya
@dp.message_handler(text="Mahsulot qo'shish")
async def add_product(message: types.Message, state: FSMContext):
    await state.set_state("addcategory")
    category = await db.get_categories()
    keyboard_category=[]
    for i in category:
        keyboard_category.append([KeyboardButton(text=i[0])])
        
    category_markup = ReplyKeyboardMarkup(
    keyboard_category,
    resize_keyboard=True,
)
    await message.answer("Kategoriyani tanlang yoki kiriting...",reply_markup=category_markup)





@dp.message_handler(state = "addcategory", content_types=types.ContentType.TEXT)
async def add_category(message: types.Message, state: FSMContext):
    category = message.text.replace("'", '`')
    
    await state.set_state("addsubcategory")
    
    await state.update_data(
        {"category": category}
    )
    subcategory = await db.get_subcategories(category=category)
    keyboard_subcategory=[]
    for i in subcategory:
        keyboard_subcategory.append([KeyboardButton(text=i[0])])
        
    subcategory_markup = ReplyKeyboardMarkup(
    keyboard_subcategory,
    resize_keyboard=True,
)
    
    await message.answer("Subkategory kiriting...",reply_markup=subcategory_markup)
    


@dp.message_handler(state = "addsubcategory", content_types=types.ContentType.TEXT)
async def add_subcategory(message: types.Message, state: FSMContext):
    subcategory = message.text.replace("'", '`')
    await state.set_state("addproductname")

    await state.update_data(
        {"subcategory": subcategory}
    )
    await message.answer("Productnameni kiriting...",reply_markup=ReplyKeyboardRemove())
    

#new


@dp.message_handler(state = "addproductname", content_types=types.ContentType.TEXT)
async def add_addproductname(message: types.Message, state: FSMContext):
    productname = message.text
    await state.set_state("addproductphoto")
    await state.update_data(
        {"productname": productname}
    )
    await message.answer("Product photoni kiriting...")


@dp.message_handler(state = "addproductphoto", content_types=types.ContentType.PHOTO)
async def add_addproductphoto(message: types.Message, state: FSMContext):
    productphotoid = message.photo[-1].file_id
    
    await state.set_state("addproductprice")
    await state.update_data(
        {"productphotoid": productphotoid}
    )
    await message.answer("Product price kiriting...")


@dp.message_handler(state = "addproductprice", content_types=types.ContentType.TEXT)
async def add_addproductprice(message: types.Message, state: FSMContext):
    addproductprice = message.text
    await state.set_state("addproductdescription")
    await state.update_data(
        {"productprice": addproductprice}
    )
    await message.answer("Product description kiriting...")
    


@dp.message_handler(state = "addproductdescription", content_types=types.ContentType.TEXT)
async def add_addproductprice(message: types.Message, state: FSMContext):
    addproductdescription = message.text
    await state.update_data(
        {"productdescription": addproductdescription}
    )
    
    data = await state.get_data()
    category = data.get("category")
    sub_category = data.get("subcategory")
    product_name = data.get("productname")
    product_photo_id = data.get("productphotoid") 
    product_price = int(data.get("productprice"))
    product_description = data.get("productdescription") 
    await state.finish()
    
    await db.add_product(
        category,
        sub_category,
        product_name,
        product_photo_id,
        product_price,
        product_description,
    )
    
    
    await message.answer("Product muvaffaqiyatli qo'shildi",reply_markup=menu)

    






# @dp.message_handler(text="/products")
# async def send_ad_command(message: types.Message):
#     products = await db.get_products()
#     print(products)
    





    
    

