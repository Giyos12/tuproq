import os
import pickle
from keras.models import load_model
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.utils import timezone
from rest_framework import views, permissions, response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from modul.models import Counter
from modul.serializers import CounterSerializer
from modul.service import bashorat
from modul.utils import namlik_predict
from tuproq.settings import BASE_DIR
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
            serialize.save()
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
                json = {}
                for i in os.listdir(new_directory_path):
                    json[i.split('.')[0]] = i
                object.file1 = os.path.join(data.get('name'), json.get('modul1'))
                object.file2 = os.path.join(data.get('name'), json.get('modul2'))
                object.file3 = os.path.join(data.get('name'), json.get('modul3'))
                object.file4 = os.path.join(data.get('name'), json.get('modul4'))
                object.file5 = os.path.join(data.get('name'), json.get('modul5'))
                object.file1norm = os.path.join(data.get('name'), json.get('modul1norm'))
                object.file2norm = os.path.join(data.get('name'), json.get('modul2norm'))
                object.file3norm = os.path.join(data.get('name'), json.get('modul3norm'))
                object.file4norm = os.path.join(data.get('name'), json.get('modul4norm'))
                object.file5norm = os.path.join(data.get('name'), json.get('modul5norm'))
                object.save()
            if data.get('file1'):
                os.remove(object.file1.path)
                object.file1 = data.get('file1')
                object.save()
            if data.get('file2'):
                os.remove(object.file2.path)
                object.file2 = data.get('file2')
                object.save()
            if data.get('file3'):
                os.remove(object.file3.path)
                object.file3 = data.get('file3')
                object.save()
            if data.get('file4'):
                os.remove(object.file4.path)
                object.file4 = data.get('file4')
                object.save()
            if data.get('file5'):
                os.remove(object.file5.path)
                object.file5 = data.get('file5')
                object.save()
            if data.get('file1norm'):
                os.remove(object.file1norm.path)
                object.file1norm = data.get('file1norm')
                object.save()
            if data.get('file2norm'):
                os.remove(object.file2norm.path)
                object.file2norm = data.get('file2norm')
                object.save()
            if data.get('file3norm'):
                os.remove(object.file3norm.path)
                object.file3norm = data.get('file3norm')
                object.save()
            if data.get('file4norm'):
                os.remove(object.file4norm.path)
                object.file4norm = data.get('file4norm')
                object.save()
            if data.get('file5norm'):
                os.remove(object.file5norm.path)
                object.file5norm = data.get('file5norm')
                object.save()
            if data.get('description'):
                object.description = data.get('description')
                object.save()
            if data.get('order'):
                object.order = data.get('order')
                object.save()
            ob = object
            if ob.order == 0:
                s1 = Model.objects.filter(order=0).first()
                if s1.is_dl:
                    preprocessing1 = pickle.load(open(s1.file1norm.path, 'rb'))
                    model1 = load_model(s1.file1.path)
                    preprocessing2 = pickle.load(open(s1.file2norm.path, 'rb'))
                    model2 = load_model(s1.file2.path)
                    preprocessing3 = pickle.load(open(s1.file3norm.path, 'rb'))
                    model3 = load_model(s1.file3.path)
                    preprocessing4 = pickle.load(open(s1.file4norm.path, 'rb'))
                    model4 = load_model(s1.file4.path)
                    preprocessing5 = pickle.load(open(s1.file5norm.path, 'rb'))
                    model5 = load_model(s1.file5.path)
                else:
                    preprocessing1 = pickle.load(open(s1.file1norm.path, 'rb'))
                    model1 = pickle.load(open(s1.file1.path, 'rb'))
                    preprocessing2 = pickle.load(open(s1.file2norm.path, 'rb'))
                    model2 = pickle.load(open(s1.file2.path, 'rb'))
                    preprocessing3 = pickle.load(open(s1.file3norm.path, 'rb'))
                    model3 = pickle.load(open(s1.file3.path, 'rb'))
                    preprocessing4 = pickle.load(open(s1.file4norm.path, 'rb'))
                    model4 = pickle.load(open(s1.file4.path, 'rb'))
                    preprocessing5 = pickle.load(open(s1.file5norm.path, 'rb'))
                    model5 = pickle.load(open(s1.file5.path, 'rb'))
                try:
                    if timezone.now().month > 1:
                        c = Counter.objects.filter(date__year=timezone.now().year,
                                                   date__month=int(timezone.now().month) - 1)
                    else:
                        c = Counter.objects.filter(date__year=int(timezone.now().year) - 1, date__month=12)
                except:
                    c = None

                if c.exists():

                    for i in c:
                        try:
                            i.gumus = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing1, model1,
                                               s1.is_dl)
                            i.fosfor = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing2, model2,
                                                s1.is_dl)
                            i.kaliy = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing3, model3,
                                               s1.is_dl)
                            i.mex = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing4, model4,
                                             s1.is_dl)
                            i.shorlanish = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10,
                                                    preprocessing5, model5, s1.is_dl)
                            i.namlik = namlik_predict(i.b5, i.b6)
                            i.model = s1
                            i.save()
                        except:
                            raise ValidationError({'error': 'bashoratda xatolik bor'})
            return Response(ModelSerializer(object).data, status=200)
        return Response(data=serializers.errors, status=400)

    def retrieve(self, request, *args, **kwargs):
        objects = Model.objects.filter(id=kwargs['pk']).first()
        return Response(ModelSerializer(objects).data, status=200)


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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data['order']
        s1 = Model.objects.filter(order=0).first()
        is_upt_order_0 = False
        for item in data:
            if s1.id == item['id'] and item['order'] != 0:
                is_upt_order_0 = True

            try:
                model = Model.objects.get(id=item['id'])
                model.order = item['order']
                model.save()
                if item['order'] == 0:
                    s1 = model
            except:
                pass
        if is_upt_order_0:
            if timezone.now().month > 1:
                c = Counter.objects.filter(date__year=timezone.now().year,
                                           date__month=int(timezone.now().month) - 1)
            else:
                c = Counter.objects.filter(date__year=int(timezone.now().year) - 1, date__month=12)

            if s1.is_dl:
                preprocessing1 = pickle.load(open(s1.file1norm.path, 'rb'))
                model1 = load_model(s1.file1.path)
                preprocessing2 = pickle.load(open(s1.file2norm.path, 'rb'))
                model2 = load_model(s1.file2.path)
                preprocessing3 = pickle.load(open(s1.file3norm.path, 'rb'))
                model3 = load_model(s1.file3.path)
                preprocessing4 = pickle.load(open(s1.file4norm.path, 'rb'))
                model4 = load_model(s1.file4.path)
                preprocessing5 = pickle.load(open(s1.file5norm.path, 'rb'))
                model5 = load_model(s1.file5.path)
            else:
                preprocessing1 = pickle.load(open(s1.file1norm.path, 'rb'))
                model1 = pickle.load(open(s1.file1.path, 'rb'))
                preprocessing2 = pickle.load(open(s1.file2norm.path, 'rb'))
                model2 = pickle.load(open(s1.file2.path, 'rb'))
                preprocessing3 = pickle.load(open(s1.file3norm.path, 'rb'))
                model3 = pickle.load(open(s1.file3.path, 'rb'))
                preprocessing4 = pickle.load(open(s1.file4norm.path, 'rb'))
                model4 = pickle.load(open(s1.file4.path, 'rb'))
                preprocessing5 = pickle.load(open(s1.file5norm.path, 'rb'))
                model5 = pickle.load(open(s1.file5.path, 'rb'))

            if c.exists():
                for i in c:
                    # try:
                    i.gumus = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing1, model1,
                                       s1.is_dl)
                    i.fosfor = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing2, model2,
                                        s1.is_dl)
                    i.kaliy = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing3, model3,
                                       s1.is_dl)
                    i.mex = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing4, model4, s1.is_dl)
                    i.shorlanish = bashorat(i.b1, i.b2, i.b3, i.b4, i.b5, i.b6, i.b7, i.b10, preprocessing5, model5,
                                            s1.is_dl)
                    i.namlik = namlik_predict(i.b5, i.b6)
                    i.model = s1
                    i.save()
                # except:
                #     raise ValidationError({'error': 'bashoratda xatolik bor'})
        return Response({'detail': 'success'}, status=200)


class ExportCounterDBToExel(ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def list(self, request):
        import pandas as pd
        try:
            a = pd.read_excel('media_root/export1.xlsx').to_dict('records')
            count1 = len(a)
            a = a[0]
        except:
            a = {}
        count_counter = Counter.objects.filter(date__year__gt=2021).count()
        c1 = Counter.objects.filter(id=a.get('id')).first()
        if c1:
            if count1 == count_counter and c1.gumus == a.get('gumus') and c1.fosfor == a.get(
                    'fosfor') and c1.kaliy == a.get(
                'kaliy') and c1.shorlanish == a.get('shorlanish') and c1.mex == a.get('mex') and c1.namlik == a.get(
                'namlik'):
                return Response(data={'url': 'media/export1.xlsx'}, status=200)
        serializer = CounterSerializer(Counter.objects.filter(date__year__gt=2021), many=True)
        df = pd.DataFrame(serializer.data)
        df.to_excel('export.xlsx', index=False)
        os.rename(os.path.join(BASE_DIR, 'export.xlsx'), os.path.join(BASE_DIR, 'media_root/export1.xlsx'))
        return Response(data={'url': 'media/export1.xlsx'}, status=200)


class ExampleView(APIView):
    def get(self, request):
        print(request.user)
        return Response(data={'detail': 'success'}, status=200)
