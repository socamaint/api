from rest_framework import serializers
from .models import Vehicules, NewUser, UserSheet
from rest_framework import serializers, validators
from .models import NewUser
from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework.exceptions import AuthenticationFailed
# from Materiel_Roulant.serializer_matrlt import VehiculeSerializer
from django.contrib.auth.hashers import make_password



class VehiculeSerializer(serializers.ModelSerializer):
   class Meta:
      model = Vehicules
      fields = ["id", "region", "nparc", "noptim", "immat", "nature", "type", "marque", "modele", "serie", "energie", "puissance", "type_compt", "annee_mes", "statut", "affectation", "site", "responsable_sabc", "alert_compt"]



class ImportEnginSerializer(serializers.Serializer):
   file = serializers.FileField()





class NewuserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewUser
        fields = ['id_newuser', 'region', 'email',  'first_name', 'last_name', 'username', 'mobile', 'address', 'type', 'fonction', 'site', 'password']





class userRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only = True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only = True)
    staff = serializers.BooleanField(default=True)
    active = serializers.BooleanField(default=True)
    superuser = serializers.BooleanField(default=False)

    class Meta:
        model = NewUser
        fields = ['region', 'email',  'first_name', 'last_name', 'username', 'mobile', 'address', 'type', 'fonction', 'site', 'password','password2','staff','active','superuser']

        extra_kwargs = {
            "email":{
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(NewUser.objects.all(), "Un utilisateur avec cet email existe déjà")
                ]
            },
            "password":{'write_only': True},
            "password2":{'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Vos mots de passe ne correspondent pas")
        return attrs

    def create(self, validated_data):
        user = NewUser.objects.create(
            email = validated_data.get("email"),
            last_name = validated_data.get("last_name"),
            first_name = validated_data.get("first_name"),
            username = validated_data.get("username"),
            password = make_password(validated_data.get("password")),
            mobile = validated_data.get("mobile"),
            region = validated_data.get("region"),
            type = validated_data.get("type"),
            fonction = validated_data.get("fonction"),
            address = validated_data.get("address"),
            is_staff = validated_data.get("staff"),
            is_active = validated_data.get("active"),
            is_superuser = validated_data.get("superuser"),
        )
        #user.set_password(validated_data.get("password"))
        return user



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=6, write_only = True)
    fullname = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = NewUser
        fields = ['email','password','fullname','access_token','refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Identifiant incorrect. Veuillez ré-essayer")
        if not user.is_verified:
            raise AuthenticationFailed("Votre email n'est pas authentique!")
        user_tokens = user.token()

        return {
            'email':user.email,
            'full_name':user.get_full_name,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh')),
        }


class UserSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSheet
        fields = "__all__"