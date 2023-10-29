import os

from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.utils import timezone
from rest_framework import views, permissions, response
from rest_framework.decorators import action
from rest_framework.response import Response

from modul.models import Counter
from modul.service import bashorat
from uath.models import Model
from uath.authentication import CsrfExemptSessionAuthentication
from uath.serializers import LoginSerializer, UserSerializer, ModelSerializer, RegisterationSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from uath.permissions import IsAdmin, IsPowerUser


class AuthModelViewSet(ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user)
            return response.Response(data=serializer.data)
        else:
            return response.Response(data={'message': 'user not authenticated'}, status=401)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return response.Response(data={'message': 'logout success'}, status=200)
        return response.Response(data={'message': 'user not authenticated'}, status=401)

    def update(self, request, *args, **kwargs):
        return response.Response(data={'message': 'method not allowed'}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return response.Response(data={'message': 'method not allowed'}, status=405)

    @action(detail=True, methods=['post', 'put', 'patch', 'delete'])
    def custom_action(self, request, pk=None):
        return Response({'detail': 'Method Not Allowed'}, status=405)


class ModelAdminViewSet(ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ModelSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({'detail': 'Bad Request'}, status=400)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        serialize = ModelSerializer(data=request.data, instance=self.get_object())
        if serialize.is_valid():
            s1 = serialize.save()
            if s1.order == 0:
                c = Counter.objects.filter(date__year=timezone.now().year, date__month=timezone.now().month)
                if c.exists():
                    for i in c:
                        i.gumus = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, s1.file1, s1.file1norm)
                        i.fosfor = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, s1.file2, s1.file2norm)
                        i.kaliy = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, s1.file3, s1.file3norm)
                        i.mex = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, s1.file4, s1.file4norm)
                        i.shorlanish = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, s1.file5, s1.file5norm)
                        i.model = s1
                        i.save()
            return Response(serialize.data, status=200)
        return Response({'detail': 'Bad Request'}, status=400)

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        directory_path = os.path.dirname(object.file1.path)

        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(directory_path)
        except Exception as e:
            return Response({'detail': 'Internal Server Error'}, status=500)
        object.delete()
        return Response({'detail': 'Deleted'}, status=204)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        serializers = ModelSerializer(data=request.data, instance=self.get_object(), partial=True)
        if serializers.is_valid():
            data = serializers.validated_data
            object = self.get_object()
            if data.get('name'):
                # filelar bilan ishlash uchun kerak bo'lgan kodlar
                directory_path = os.path.dirname(object.file1.path)
                os.chdir(directory_path)
                os.chdir('..')
                cd = os.getcwd()
                new_directory_path = os.path.join(cd, data.get('name'))
                os.rename(directory_path, new_directory_path)
                object.name = data.get('name')

                # filelar bilan ishlash uchun kerak bo'lgan kodlar
                object.file1 = os.path.join(data.get('name'), os.listdir(new_directory_path)[0])
                object.file2 = os.path.join(data.get('name'), os.listdir(new_directory_path)[2])
                object.file3 = os.path.join(data.get('name'), os.listdir(new_directory_path)[4])
                object.file4 = os.path.join(data.get('name'), os.listdir(new_directory_path)[6])
                object.file5 = os.path.join(data.get('name'), os.listdir(new_directory_path)[8])
                object.file1norm = os.path.join(data.get('name'), os.listdir(new_directory_path)[1])
                object.file2norm = os.path.join(data.get('name'), os.listdir(new_directory_path)[3])
                object.file3norm = os.path.join(data.get('name'), os.listdir(new_directory_path)[5])
                object.file4norm = os.path.join(data.get('name'), os.listdir(new_directory_path)[7])
                object.file5norm = os.path.join(data.get('name'), os.listdir(new_directory_path)[9])
                object.save()
            if data.get('file1'):
                os.remove(object.file1.path)
                object.file1 = data.get('file1')
            if data.get('file2'):
                os.remove(object.file2.path)
                object.file2 = data.get('file2')
            if data.get('file3'):
                os.remove(object.file3.path)
                object.file3 = data.get('file3')
            if data.get('file4'):
                os.remove(object.file4.path)
                object.file4 = data.get('file4')
            if data.get('file5'):
                os.remove(object.file5.path)
                object.file5 = data.get('file5')
            if data.get('file1norm'):
                os.remove(object.file1norm.path)
                object.file1norm = data.get('file1norm')
            if data.get('file2norm'):
                os.remove(object.file2norm.path)
                object.file2norm = data.get('file2norm')
            if data.get('file3norm'):
                os.remove(object.file3norm.path)
                object.file3norm = data.get('file3norm')
            if data.get('file4norm'):
                os.remove(object.file4norm.path)
                object.file4norm = data.get('file4norm')
            if data.get('file5norm'):
                os.remove(object.file5norm.path)
                object.file5norm = data.get('file5norm')
            if data.get('description'):
                object.description = data.get('description')
            if data.get('order'):
                object.order = data.get('order')
            object.save()
            return Response(ModelSerializer(object).data, status=200)
        return Response(data=serializers.errors, status=400)


class AddPowerUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterationSerializer

    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.filter(groups__name__in=['power_user'])

    # def list(self, request, *args, **kwargs):
    #     list1 = []
    #     for user in self.get_queryset():
    #         dict1 = {}
    #         dict1 = UserSerializer(user).data
    #         # dict1['password'] =
    #         list1.append(UserSerializer(user).data  )

    @transaction.atomic
    def create(self, request):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            user.groups.add(1)
            return response.Response(UserSerializer(user).data, status=201)
        return response.Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        serializer = RegisterationSerializer(data=request.data, instance=self.get_object())
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, *args, **kwargs):
        serializer = RegisterationSerializer(data=request.data, instance=self.get_object(), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ModelOrderUpdateViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        data = request.data['order']
        for item in data:
            try:
                model = Model.objects.get(pk=item['id'])
                model.order = item['order']
                model.save()
            except:
                pass
        return Response({'detail': 'success'}, status=200)
