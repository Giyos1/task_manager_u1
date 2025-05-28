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
    code = serializers.CharField(max_length=6,write_only=True)
    password = serializers.CharField(max_length=100,write_only=True)
    re_password = serializers.CharField(max_length=100,write_only=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise ValidationError('Password va Re_password togri kelmayapti')
        return attrs


    def validate_code(self,value):
       code = Code.objects.filter(code=value).first()
       if not code:
           raise ValidationError('Bunday code mavjud emas')

       if code.exp_date < timezone.now():
           raise ValidationError('Code ning vaqti otb ketdi qaytadan yuboring')
       user = code.objects.get('user')
       value['user']=user
       return value


    def save(self, attrs):
        user = attrs.get('user')
        user.set_password(attrs.get('password'))
        user.save()
        return user













