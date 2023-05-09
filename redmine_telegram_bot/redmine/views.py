from rest_framework import viewsets

from redmine.models import RedmineGroup
from redmine.serializers import RedmineGroupSerializer


class RedmineGroupViewSet(viewsets.ModelViewSet):
    queryset = RedmineGroup.objects.all()
    serializer_class = RedmineGroupSerializer
