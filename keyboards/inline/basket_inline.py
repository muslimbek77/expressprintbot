from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db 

basket_item_action = CallbackData("buy", "item_action", "product")

async def basket_inline_keyboard(user_id):
    print("inline_basket1")

    inline_markup = InlineKeyboardMarkup(row_width=4)
    print("inline_basket2")
    products = await db.get_baskets(user_id)
    print(products)
    for i in products:
        
        inline_markup.row(InlineKeyboardButton(i[1]), 
            InlineKeyboardButton(text="+", callback_data=basket_item_action.new(item_action="plus", product=i[1])), 
            InlineKeyboardButton(text="-", callback_data=basket_item_action.new(item_action="minus", product=i[1])), 
            InlineKeyboardButton(text="x", callback_data=basket_item_action.new(item_action="delete", product=i[1])))
    inline_markup.row(InlineKeyboardButton(text="Заказать", callback_data=basket_item_action.new(item_action="order")))
        # inline_markup.row(InlineKeyboardButton(text=f"", callback_data="ok"))
    print("inline_basket3")

    return inline_markup




buy_item = CallbackData("buy", "item_id")
del_item = CallbackData("delete", "item_id")
def buy_item_inline(item_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text=f"🛒 Karzinkaga qo'shish", callback_data=buy_item.new(item_id=item_id))
        ) 
    return markup