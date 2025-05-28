from django.utils import timezone

from django.contrib.auth import authenticate
from pyexpat.errors import messages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import User
from accounts.models import Code
from accounts.service import send_email


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )






class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=200,write_only=True)
    class Meta:
        model =  User
        fields =[
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            're_password'
        ]

        extra_kwargs ={
            'password':{'write_only':True}
        }



    def validate(self,attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise ValidationError('password va re_password togri kelmadi')
        attrs.pop('re_password')
        return attrs


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


    def validate(self, attrs):
        username =attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username,password=password)

        if not user:
            raise ValidationError('User doesn\'t exists')
        return {'user':user}




class CheckUserSerializer(serializers.Serializer):
    email =serializers.EmailField()


    def validate(self,attrs):
        email = attrs.get('email')
        user=User.objects.filter(email=email).first()
        if not user:
            raise ValidationError('Bunday email mavjud emas')
        print(attrs)
        attrs['user'] = user
        return attrs


    def save(self, **kwargs):
        user = self.validated_data['user']
        code= Code.objects.create(user=user)

        send_email(
            subject= "Parolni tiklash code",
            message = f'Maxfiy code{code.code} foydalanuvchi usernname {user.username}',
            to_email = user.email
            )
        return code



class RestoreSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,write_only=True)
    code = serializers.CharField(max_length=6,write_only=True)
    password = serializers.CharField(max_length=100,write_only=True)
    re_password = serializers.CharField(max_length=100,write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        code = attrs.get('code')

        if password != re_password:
            raise ValidationError('Passworqd va Re_password togri kelmayapti')


        user =User.objects.filter(username=username).first()

        if not user:
            raise ValidationError('bunday user mavjud emas')
        attrs['user'] = user

        cod_obj = Code.objects.filter(code=code).first()

        if not cod_obj:
            raise ValidationError('Bunday code mavjud emas')

        if cod_obj.exp_date < timezone.now():
            raise ValidationError('Boshqatdan yuboring')
        return attrs




    def save(self):
        user = self.validated_data['user']
        password = self.validated_data['password']
        user.set_password(password)
        user.save()













