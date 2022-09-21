from telegram_bot_calendar import WYearTelegramCalendar


class MyStyleCalendar(WYearTelegramCalendar):
    "Класс календаря для кастомизации"
    prev_button = "⬅️"
    next_button = "➡️"
    empty_month_button = ""
    empty_year_button = ""
    empty_nav_button = ""
