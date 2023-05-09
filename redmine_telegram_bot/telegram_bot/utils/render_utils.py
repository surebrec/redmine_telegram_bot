from redmine.serializers import RedmineGroupSerializer


def render_groups_to_message(groups_queryset):
    res = []
    for group in groups_queryset:
        serializer = RedmineGroupSerializer(instance=group)
        res.append(render(serializer.data))
    return '\n\n'.join(res)


def render(data):
    res = [data['name']]
    template = '{} {:1.1}.{:1.1}.'
    for user in data['users']:
        res.append(template.format(*user['name'].split()))
    return '\n'.join(res)
