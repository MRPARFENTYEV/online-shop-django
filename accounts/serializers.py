from rest_framework import serializers
from managers import UserManager
class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManager
        fields = "__all__"