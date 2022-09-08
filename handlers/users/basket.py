from aiogram import types
from loader import db, dp, bot
from keyboards.default.MenuKeyboard import menu 
from keyboards.inline.basket_inline import basket_inline_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext



basket_item_action = CallbackData("buy", "item_action", "product")


@dp.message_handler(text="🛒 Savatcha")
async def show_bascket(message: types.Message):
    user_id=message.from_user.id
    idw = await db.get_baskets(user_id=user_id)
    a=''
    print(idw)
    idw.sort()
    inline_markup = InlineKeyboardMarkup(row_width=4)
    jami=0
    for i in idw:
        try:
            product = await db.product_for_basket(item_id=i[1])
        except:
            continue
        
        name = product[3]
        pr_count = await db.get_count(user_id,i[1])
        jami=jami+product[5]*pr_count
        a+=f'{name}\n{product[5]} so\'m x {pr_count} = {product[5]*pr_count} so\'m\n\n'

        inline_markup.add(InlineKeyboardButton(text=name, callback_data="1"), 
        InlineKeyboardButton(text="-", callback_data=basket_item_action.new(item_action="minus", product=i[1])), 
        InlineKeyboardButton(text="+", callback_data=basket_item_action.new(item_action="plus", product=i[1])), 
        InlineKeyboardButton(text="x", callback_data=basket_item_action.new(item_action="delete", product=i[1]))),
    a=a+f'Jami: {jami} so\'m'
    inline_markup.add(InlineKeyboardButton(text="Buyurtma berish!", callback_data=basket_item_action.new(item_action="order",product='')))
    if a=='':
        await message.answer(text='mahsulot yo\'q', reply_markup=menu)
    else:
        await message.answer(a, reply_markup=inline_markup)

@dp.callback_query_handler(basket_item_action.filter())
async def basket_actions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):

    item_action=callback_data.get("item_action")
    item_id=callback_data.get("product")
    user_id=call.from_user.id

    
    if item_action=="plus":
        await db.plus_count(user_id=user_id, item_id=item_id)
    elif item_action=="minus":
        await db.minus_count(user_id=user_id, item_id=item_id)
    elif item_action=='delete':
        await db.del_count(user_id=user_id,item_id=item_id)
    idw = await db.get_baskets(user_id=user_id)
    idw.sort()
    print("idw",idw)
    inline_markup = InlineKeyboardMarkup(row_width=4)
    if idw:
        a=''
        for i in idw:
            product = await db.product_for_basket(item_id=i[1])
            print(product)
            name = product[3]
            pr_count = await db.get_count(user_id,i[1])
            if pr_count==0:
                await db.del_count(user_id=user_id,item_id=item_id)
                continue
            a+=f'{name}\n{product[5]} x {pr_count} = {product[5]*pr_count}\n\n'
            jami=jami+product[5]*pr_count

            inline_markup.add(InlineKeyboardButton(text=name, callback_data="1"), 
            InlineKeyboardButton(text="-", callback_data=basket_item_action.new(item_action="minus", product=i[1])), 
            InlineKeyboardButton(text="+", callback_data=basket_item_action.new(item_action="plus", product=i[1])), 
            InlineKeyboardButton(text="x", callback_data=basket_item_action.new(item_action="delete", product=i[1])))
        a=a+f'Jami: {jami} so\'m'
        inline_markup.add(InlineKeyboardButton(text="Buyurtma berish!", callback_data=basket_item_action.new(item_action="order",product=i[1])))

        if a=='':
            await call.message.delete()
            await call.message.answer(text='mahsulot yo\'q', reply_markup=menu)     
        else: 
            await call.message.edit_text(text=a, reply_markup=inline_markup)    
    else:
        await call.message.delete()
        await call.message.answer(text='mahsulot yo\'q', reply_markup=menu)    
     
        