from aiogram.fsm.state import StatesGroup, State


class GenStateGroup(StatesGroup):
    generate_trip_state = State()
    chat_state = State()


class ChoiceStateGroup(StatesGroup):
    cities_choice_state = State()
    num_days_choice_state = State()
    travel_style_choice_state = State()
