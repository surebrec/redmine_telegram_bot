def message_template(date, group_name, time_entries):
    if not time_entries:
        time_entries = '✅ Все заполнено!'
    return f'<u>{date}</u>\n\n<b>{group_name}</b>\n\n{time_entries}'
