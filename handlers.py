from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import flags


from states import GenStateGroup, ChoiceStateGroup


import texts
import kb
import utils
import db


global_cities_choice = []
global_num_days_choice: int = 0
global_travel_style_choice: str = ""


router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    global global_cities_choice
    global_cities_choice = []
    await db.add_user(message.from_user.id)
    await message.answer(texts.intro, reply_markup=kb.menu)


@router.message(F.text == "Menu")
@router.message(F.text == "◀️ Back to menu")
@router.message(F.text == "◀️ Go to menu")
async def menu(msg: Message):
    await msg.answer(texts.menu, reply_markup=kb.menu)


@router.message(F.data == "help")
async def handle_help_command(message: Message) -> None:
    help_command_message = """
        <b>/help</b> - List of available commands.
        <b>/start</b> - Start bot.
        <b>/make_trip</b> - Generate a trip.
        <b>/how_it_works</b> - Bot description
        <b>/balance</b> - Balance of user.
    """
    await message.answer(help_command_message, parse_mode=ParseMode.HTML)


@router.message(Command("my_balance"))
async def my_balance_handler(message: Message):
    cur_balance = await db.get_balance(message.from_user.id)
    await message.answer("Your current balance is: {} tokens".format(cur_balance))


@router.callback_query(F.data == "generate_trip")
async def handle_make_trip_command(cb: CallbackQuery, state: FSMContext) -> None:
    # await message.answer(texts.cities_input_text, reply_markup=kb.cities_kb)
    await state.set_state(ChoiceStateGroup.cities_choice_state)
    curr_state = await state.get_state()
    print(curr_state)
    await cb.message.answer(texts.cities_input_text, reply_markup=kb.cities_kb)


@router.callback_query(ChoiceStateGroup.cities_choice_state)
async def handle_cities_choice_state(cb: CallbackQuery, state: FSMContext) -> None:
    global global_cities_choice
    global_cities_choice.append(cb.data)
    print(global_cities_choice)
    await state.set_state(ChoiceStateGroup.num_days_choice_state)
    curr_state = await state.get_state()
    print(curr_state)
    await cb.message.answer(texts.num_days_input_text, reply_markup=kb.days_kb)


@router.callback_query(ChoiceStateGroup.num_days_choice_state)
async def handle_num_days_choice_state(cb: CallbackQuery, state: FSMContext) -> None:
    global global_num_days_choice
    global_num_days_choice = int(cb.data)
    print(global_num_days_choice)
    await state.set_state(ChoiceStateGroup.travel_style_choice_state)
    curr_state = await state.get_state()
    print(curr_state)
    await cb.message.answer(
        texts.travel_style_input_text, reply_markup=kb.travel_style_kb
    )


@router.callback_query(ChoiceStateGroup.travel_style_choice_state)
async def handle_travel_style_choice_state(
    cb: CallbackQuery, state: FSMContext
) -> None:
    global global_travel_style_choice
    global_travel_style_choice = cb.data
    print(global_travel_style_choice)
    curr_state = await state.get_state()
    print(curr_state)
    await state.set_state(GenStateGroup.generate_trip_state)
    await cb.message.answer("Do you want to generate a trip?", reply_markup=kb.final_kb)


@router.callback_query(F.data == "generate_text")
@router.callback_query(GenStateGroup.generate_trip_state)
async def handle_final_state(cb: CallbackQuery, state: FSMContext) -> None:
    check = await db.check_balance(cb.from_user.id)
    if not check:
        return await cb.message.answer(texts.balance_error, reply_markup=kb.iexit_kb)
    context = await db.get_request_response(cb.from_user.id)
    cities_inp = ", ".join(global_cities_choice)
    message = texts.main_prompt.format(
        cities=cities_inp,
        num_days=global_num_days_choice,
        travel_style=global_travel_style_choice,
    )
    print(message)
    prompt = texts.prompt_template.format(
        prev_request=context[0], prev_response=context[1], message=message
    )
    res = await utils.generate_text(prompt)
    if not res:
        return await cb.message.answer(texts.gen_error, reply_markup=kb.iexit_kb)
    await db.update_request_response(cb.from_user.id, cb.message.text, res[0])
    await cb.message.answer(
        res[0], disable_web_page_preview=True, reply_markup=kb.exit_kb
    )
    await db.update_balance(cb.from_user.id, res[1])
    await cb.message.answer(texts.suggestions_text)
    await state.set_state(GenStateGroup.chat_state)


@router.callback_query(F.data == "how_it_works")
async def handle_how_it_works_command(message: Message) -> None:
    await message.answer(texts.how_it_works, reply_markup=kb.menu)


@router.message(GenStateGroup.chat_state)
@flags.chat_action("typing")
async def handle_chat_message(msg: Message, state: FSMContext):
    check = await db.check_balance(msg.from_user.id)
    if not check:
        return await msg.answer(texts.balance_error, reply_markup=kb.iexit_kb)
    context = await db.get_request_response(msg.from_user.id)
    prompt = texts.prompt_template.format(
        prev_request=context[0], prev_response=context[1], message=msg.text
    )
    res = await utils.generate_text(prompt)
    if not res:
        return await msg.answer(texts.gen_error, reply_markup=kb.iexit_kb)
    await db.update_request_response(msg.from_user.id, msg.text, res[0])
    await msg.answer(res[0], disable_web_page_preview=True, reply_markup=kb.exit_kb)
    await db.update_balance(msg.from_user.id, res[1])
