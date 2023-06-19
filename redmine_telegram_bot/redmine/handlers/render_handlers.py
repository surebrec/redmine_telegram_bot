import logging

from templates.redmine.message import message_template


def render_to_message(data, users_names, group_name, from_date, to_date):
    time_entries = {name: {'hours': 0, 'comments': 0} for name in
                    users_names}
    parsed_time_entries = parce_time_entries_data(data, time_entries)
    time_entries = ''.join(filter_time_sheets(name, **values)
                           for name, values in
                           parsed_time_entries.items() if name)
    date = f"{from_date}" + (
        f" - {to_date}" if to_date != from_date else '')
    return message_template(date, group_name, time_entries)


def parce_time_entries_data(data, time_entries):
    for values in data[-1]['time_entries']:
        user = values['user']['name']
        time_entries[user]['hours'] += values['hours']
        time_entries[user]['comments'] += len(values['comments'])
    return time_entries


def filter_time_sheets(name, hours, comments):
    if comments > 0 and hours > 6.5:
        return ''
    if comments == 0:
        c_text = "комментарии не заполнены;"
        symbol = "&#9999;"
        if hours == 0:
            h_text = "часы не заполнены;"
            symbol = "&#10060;"
        elif 0 < hours < 6.5:
            h_text = f"неполные часы ({hours});"
            symbol = "&#128337;"
        else:
            h_text = ""
    else:
        c_text = ""
        h_text = f"неполные часы ({hours});"
        symbol = "&#128337;"
    short_name = '{} {:.1}.{:.1}.'.format(*name.split())
    return f"{symbol} {short_name}: {h_text} {c_text}\n"
