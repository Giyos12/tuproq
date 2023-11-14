from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from uath.models import Model


class ModelSerializer(serializers.ModelSerializer):
    file1_size = serializers.SerializerMethodField()
    file2_size = serializers.SerializerMethodField()
    file3_size = serializers.SerializerMethodField()
    file4_size = serializers.SerializerMethodField()
    file5_size = serializers.SerializerMethodField()
    file1norm_size = serializers.SerializerMethodField()
    file2norm_size = serializers.SerializerMethodField()
    file3norm_size = serializers.SerializerMethodField()
    file4norm_size = serializers.SerializerMethodField()
    file5norm_size = serializers.SerializerMethodField()

    def get_file1_size(self, obj):
        return obj.file1.size

    def get_file2_size(self, obj):
        return obj.file2.size

    def get_file3_size(self, obj):
        return obj.file3.size

    def get_file4_size(self, obj):
        return obj.file4.size

    def get_file5_size(self, obj):
        return obj.file5.size

    def get_file1norm_size(self, obj):
        return obj.file1norm.size

    def get_file2norm_size(self, obj):
        return obj.file2norm.size

    def get_file3norm_size(self, obj):
        return obj.file3norm.size

    def get_file4norm_size(self, obj):
        return obj.file4norm.size

    def get_file5norm_size(self, obj):
        return obj.file5norm.size

    class Meta:
        model = Model
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        try:
            role = obj.groups.all()[0].name
        except:
            role = None
        return role

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role')


class RegisterationSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        try:
            role = obj.groups.all()[0].name
        except:
            role = None
        return role

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'role')
        model = User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        User.objects.filter(username=attrs['username'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


