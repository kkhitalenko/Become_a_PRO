from aiogram.fsm.state import State, StatesGroup


class BotStates(StatesGroup):
    """Describes all possible states of the bot."""

    starting = State()
    testing = State()
    studying = State()
    feedback = State()
