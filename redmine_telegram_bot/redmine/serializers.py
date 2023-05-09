from rest_framework import serializers

from redmine.models import RedmineUser, RedmineGroup


class RedmineUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user_id')
    name = serializers.CharField()

    class Meta:
        model = RedmineUser
        fields = ('id', 'name')


class RedmineGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='group_id')
    name = serializers.CharField()
    users = RedmineUserSerializer(many=True)

    class Meta:
        model = RedmineGroup
        fields = ('id', 'name', 'users')

    def update(self, instance, validated_data):
        users_data = validated_data.pop('users')
        super().update(instance, validated_data)
        if instance.users.all().exists():
            instance.users.all().delete()
        self.create_redmine_users(users_data, instance)
        return instance

    @staticmethod
    def create_redmine_users(users_data, instance):
        users = [RedmineUser(group=instance, **user_data, ) for user_data
                 in users_data]
        RedmineUser.objects.bulk_create(users)
