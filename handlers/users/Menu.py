from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp,db
from keyboards.default.MenuKeyboard import menu
from keyboards.inline.basket_inline import buy_item_inline,buy_item,del_item

def shop_markup(category):
    markup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    for i in category:
        i=i[0]
        markup.insert(KeyboardButton(text=f"{i}")) 
    markup.row(KeyboardButton(text='ortga')) 
    markup.row(KeyboardButton(text='asosiy menu'))
        
    return markup


@dp.message_handler(text='🛍 Buyurtma berish',state=None)
async def bot_categories(message: types.Message, state: FSMContext):    
    category = await db.get_categories()
    await state.set_state("category")
    await message.answer(text='Kategoriyani tanlang.',reply_markup=shop_markup(category))

@dp.message_handler(state='category',)
async def product(message: types.Message, state: FSMContext):
    if message.text =='ortga' or message.text =='asosiy menu':
        await state.finish()
        await message.answer(text='Menu',reply_markup=menu)
    else:
        category = message.text
        await state.set_state("subcategory")
        await state.update_data({"category": category})
        try:
            subcategories = await db.get_subcategories(category=category)
        except:
            pass  
        await message.answer(text='subkategoryani tanlang.',reply_markup=shop_markup(subcategories))

@dp.message_handler(state='subcategory',)
async def product(message: types.Message, state: FSMContext):
    if message.text =='asosiy menu':
        await state.finish()
        await message.answer(text='Menu',reply_markup=menu)
    elif message.text =='ortga':
            await state.set_state("category")
            category = await db.get_categories()
            await message.answer(text='Kategoriyani tanlang.',reply_markup=shop_markup(category))
    
    else:
        subcategory = message.text
        data = await state.get_data()
        category = data.get("category")
        await state.update_data({"subcategory": subcategory})
        await state.set_state("product")
        subcategory = await db.get_product_names(category,subcategory)
        await message.answer(text='mahsulotni tanlang.',reply_markup=shop_markup(subcategory))


@dp.message_handler(state='product')
async def product(message: types.Message, state: FSMContext):
    if message.text =='asosiy menu':
        await state.finish()
        await message.answer(text='Menu',reply_markup=menu)
    elif message.text =='ortga':
        
        data = await state.get_data()
        category = data.get("category")
        await state.set_state("subcategory")
        subcategories = await db.get_subcategories(category)
        await message.answer(text='subkategoryani tanlang.',reply_markup=shop_markup(subcategories))
    else:
        
        productname = message.text
        data = await state.get_data()
        subcategory = data.get("subcategory")
        category = data.get("category")
        product = await db.get_product(category,subcategory,productname)
        print(product)
        photo = product[4]
        item_id = product[0]
        caption=f"{product[3]}\n{product[6]}\n{product[5]}"
        markup = buy_item_inline(item_id)
        print("ADMINS",ADMINS)
        print(message.from_user.id)
        if str(message.from_user.id) in ADMINS:
            print('Kalbak')
            markup.row(InlineKeyboardButton(text='O\'chirish',callback_data=del_item.new(item_id=item_id)))
        await message.answer_photo(photo=photo,caption=caption,reply_markup=markup)
        
        



@dp.callback_query_handler(buy_item.filter(),state=['product','find'])
async def buy(call: types.CallbackQuery, callback_data: dict):
    item_id=callback_data.get("item_id")
    try:
        await db.add_basket(
            user_id=call.from_user.id,
            item_id=item_id,
            product_count=1
        )
        
        await call.answer('Mahsulot korzinkaga qo\'shildi')
        await call.message.delete()
    except:
        await call.answer('Mahsulot korzinkaga qo\'shilgan')
        await call.message.delete()


@dp.callback_query_handler(del_item.filter(),state=['product','find'])
async def buy(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id=callback_data.get("item_id")
    await db.delete_product(item_id=item_id)
    await db.delete_basket(item_id=item_id)
    await call.answer('Mahsulot o\'chirildi')
    await call.message.delete()
    await state.finish()
    await call.message.answer(text='Menu',reply_markup=menu)
    
    

@dp.message_handler(text='🔎Qidirish',state=None)
async def find_product(message: types.Message, state: FSMContext):    
    await state.set_state("find")
    menus = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="asosiy menu"),
        ],
    ],
    resize_keyboard=True,
)
    await message.answer(text=' Qidirish uchun mahsulot id kiriting.',reply_markup=menus)
    

@dp.message_handler(state='find')
async def product_find(message: types.Message, state: FSMContext):
    if message.text =='asosiy menu':
        await state.finish()
        await message.answer(text='Menu',reply_markup=menu)
    product = await db.product_for_basket(item_id=message.text)
    
    if product==None:
       await message.answer(text='Id bo\'yicha mahsulot topilmadi') 
    else:
        # await state.set_state("product")
        print(product)
        photo = product[4]
        item_id = product[0]
        caption=f"{product[3]}\n{product[6]}\n{product[5]}"
        markup = buy_item_inline(item_id)
        print("ADMINS",ADMINS)
        print(message.from_user.id)
        if str(message.from_user.id) in ADMINS:
            print('Kalbak')
            markup.row(InlineKeyboardButton(text='O\'chirish',callback_data=del_item.new(item_id=item_id)))
        await message.answer_photo(photo=photo,caption=caption,reply_markup=markup)

    



    

    
    