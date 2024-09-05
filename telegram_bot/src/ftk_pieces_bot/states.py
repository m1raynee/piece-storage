from aiogram.fsm.state import State, StatesGroup


class SetActiveStudentState(StatesGroup):
    name = State()


class InlinePieceSearch(StatesGroup):
    type_choosing = State()
    search = State()
