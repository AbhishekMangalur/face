from rest_framework import serializers
from .models import User, CEO, HR, Manager, Employee, Admin
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        # Always hash password when creating
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Ensure password is hashed when updating too
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'role', 'is_staff']


class CEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = CEO
        fields = '__all__'

class HRSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class SuperUserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_superuser(
            email=validated_data['email'],
            password=validated_data['password'],
            role='admin'  # Default superuser role, adapt if needed
        )
        return user
