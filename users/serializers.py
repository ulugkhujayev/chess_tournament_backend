from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)]
    )
    rating = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3000)]
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_admin", "age", "rating", "country")
        read_only_fields = ("is_admin",)

    def validate_username(self, value):
        if any(char.isspace() for char in value):
            raise serializers.ValidationError("Username cannot contain spaces.")
        return value

    def validate_country(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "Country name should only contain letters and spaces."
            )
        return value
