from aiogram.fsm.state import State, StatesGroup


class BotStates(StatesGroup):
    """Describes all possible states of the bot."""

    studying = State()
    repeating = State()
    feedback = State()
