from rest_framework import serializers

from users.models import User, UserChoices


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, allow_null=False)
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True)
    user_status = serializers.ChoiceField(
        choices=UserChoices.choices,
        default=UserChoices.STUDENT,
        allow_null=True,
    )
    is_superuser = serializers.BooleanField(write_only=True, default=False)

    def get_user_status(self, obj):
        if obj != "student" or None:
            obj = "colaborator"
            return self

    def create(self, validated_data: dict):
        user_status = validated_data.get("user_status")
        if user_status == "colaborator":
            validated_data["is_superuser"] = True
        return User.objects.create_user(**validated_data)
