def message_template(date, group_name, time_entries):
    return (f'<u>{date}</u>\n\n<b>{group_name}</b>'
            f'\n\n{time_entries or "✅ Все заполнено!"}')
