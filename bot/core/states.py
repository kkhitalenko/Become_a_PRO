from aiogram.fsm.state import State, StatesGroup


class BotStates(StatesGroup):
    """Describes all possible states of the bot."""

    testing = State()
    studying = State()
    feedback = State()
