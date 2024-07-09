START = '''
Привет! Тебя приветствует Telegram бот для изучения языков программирования.
Что тебя интересует?
'''

HELP = '''
/start - начать обучение
/continue - продолжить обучение
/switch_mode - переключиться между режимами
доступны режимы повторения и изучения новых тем
/switch_language - переключиться на другой язык
/feedback - предложить автору идею или сообщить об ошибке
/github - посмотреть код Become_a_PRO на github и поставить ⭐️
'''

FEEDBACK = 'Напиши мне, что думаешь'

THANKS_FOR_FEEDBACK = 'Спасибо за фидбэк, мы передали его автору'

FINISH = 'Поздравляю, на этом все! Пока!😎'

GITHUB_URL = 'https://github.com/kkhitalenko/Become_a_PRO'

TRY_AGAIN = 'Неверно, попробуй ещё раз'

LETS_START = 'Кажется, продолжать нечего. Может начнём сначала?'

WHICH_LANGUAGE = 'Какой язык ты хочешь продолжить изучать?'


def get_message_to_admin(user_id: int, text: str) -> str:
    return f'Пользователь с id={user_id} написал "{text}"'


def already_learned_the_language(language: str) -> str:
    return f'Ты уже начал учить {language.title()}, что ты хочешь?'


def have_you_already_learned(language: str) -> str:
    return f'Ты изучал ранее {language.title()}?'
