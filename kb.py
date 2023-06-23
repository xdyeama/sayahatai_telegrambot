from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu = [
    [InlineKeyboardButton(text="🛫Generate trip", callback_data="generate_trip")],
    [InlineKeyboardButton(text="⚙️How it works", callback_data="how_it_works")],
    [InlineKeyboardButton(text="🔍Help", callback_data="help")],
]


menu = InlineKeyboardMarkup(inline_keyboard=menu)

exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Back to menu")]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="◀️ Go to menu", callback_data="menu")]]
)


cities_choice = [
    [
        InlineKeyboardButton(text="⛰️ Almaty", callback_data="Almaty"),
        InlineKeyboardButton(text="🏛️ Astana", callback_data="Astana"),
    ],
    [
        InlineKeyboardButton(text="🌊 Aqtau", callback_data="Aqtau"),
        InlineKeyboardButton(text="🛢️ Aqtobe", callback_data="Aqtobe"),
    ],
    [
        InlineKeyboardButton(text="🌞 Shymkent", callback_data="Shymkent"),
        InlineKeyboardButton(text="🕌 Turkestan", callback_data="Turkestan"),
    ],
    [InlineKeyboardButton(text="NEXT", callback_data="next_question")],
]

cities_kb = InlineKeyboardMarkup(inline_keyboard=cities_choice)

days_choice = [
    [
        InlineKeyboardButton(text="1 day", callback_data="1"),
        InlineKeyboardButton(text="2 days", callback_data="2"),
        InlineKeyboardButton(text="3 days", callback_data="3"),
    ],
    [
        InlineKeyboardButton(text="4 days", callback_data="4"),
        InlineKeyboardButton(text="5 days", callback_data="5"),
        InlineKeyboardButton(text="6 days", callback_data="6"),
    ],
    [
        InlineKeyboardButton(text="7 day", callback_data="7"),
        InlineKeyboardButton(text="8 days", callback_data="8"),
        InlineKeyboardButton(text="9 days", callback_data="9"),
    ],
]
days_kb = InlineKeyboardMarkup(inline_keyboard=days_choice)

travel_style_choice = [
    [InlineKeyboardButton(text="🏄‍♂️Active tourism", callback_data="active")],
    [InlineKeyboardButton(text="🌉Tourist sightseeing", callback_data="attraction")],
    [InlineKeyboardButton(text="🖼️Cultural and spiritual", callback_data="cultural")],
    [InlineKeyboardButton(text="🍲Foodie tour", callback_data="food")],
    [InlineKeyboardButton(text="Generate plan", callback_data="generate_text")],
]
travel_style_kb = InlineKeyboardMarkup(inline_keyboard=travel_style_choice)

final_kb_button = [
    [InlineKeyboardButton(text="Generate plan", callback_data="generate_text")],
]
final_kb = InlineKeyboardMarkup(inline_keyboard=final_kb_button)
