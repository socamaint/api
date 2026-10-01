from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .RessourceSerializer import userRegisterSerializer
from rest_framework import status
from django.http import HttpResponseRedirect
from datetime import datetime
from .utils import envoie_email
from .models import NewUser, UserSheet
from .RessourceSerializer import NewuserSerializer, UserSheetSerializer
from Entreprises.models import Eses
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import codecs
from django.http import HttpResponseForbidden
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser



@api_view(["GET"])
def test(request):
    return Response({"Bonjour sur notre page d'accueil"})

# fonction pour l'envoie du mail de notification de la création d'un compte utilisateur au concerné
def user_mail(request, email, full_name, type, site, region, password):
    """ This view help to create and account for testing sending mails."""

    # client = get_tenant(request=request)
    # ese = InfoEses.objects.get(sigle=client.schema_sigle)

    region_ese = Eses.objects.filter(region=region).first()

    subjet = "Création du compte utilisateur"
    template = 'user_email_notif.html'
    context = {
        'date': datetime.today().date,
        'email': email,
        'full_name': full_name,
        'type':type,
        'site': site,
        'password': password,
        'nom_ese': region_ese.nom_ese,
        'sigle': region_ese.schema_sigle,
        'logo': region_ese.logo_ese,
        'email_ese': region_ese.email,
        'region': region_ese.region,
        'mobile': region_ese.mobile,
    
    }

    receivers = [email]

    has_send = envoie_email(
        subjet=subjet,
        receivers=receivers,
        template=template,
        context=context
        )

    if has_send:
        return Response({'msg':"mail envoyee avec success."}, status=status.HTTP_200_OK)
    else:
        return Response({'msg':"email envoie echoue."}, status=status.HTTP_400_BAD_REQUEST)



class RegisterUserView(GenericAPIView):
    serializer_class = userRegisterSerializer

    def post(self,request):
        user_data = request.data
        serializer = self.serializer_class(data = user_data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            #fonction envoie mail pour les infos d'utilisateur
            user = NewUser.objects.get(email=user_data['email'])
            user_mail(request, email=user.email, full_name=user.get_full_name, type=user.type, site=user.site, region=user.region, password=user.password)
            return Response({
                'message':f" merci de vous être fais enregistrer "
            }, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

        



@api_view(["POST"])
def get_user_data(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_info':{
                'id':user.id_newuser,
                'username':user.email,
                'full_name':user.get_full_name,
                'site':user.site,
                'type':user.type,
                'mobile':user.mobile,
                'region':user.region,
                'fonction':user.fonction,
            }
        })
    return Response({"erreur": "Pas authentifié"}, status=status.HTTP_400_BAD_REQUEST)



class register_user(generics.CreateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = NewUser.objects.all()
    serializer_class = userRegisterSerializer

    def perform_create(self, serializer):
        # serializer = self.serializer_class
        ##################################
        user = serializer.save(using="NewUser")
        data_usersheet = {}
        data_usersheet["email"] = serializer.validated_data.get("email", None)
        data_usersheet["username"] = serializer.validated_data.get("username", None)
        data_usersheet["first_name"] = serializer.validated_data.get("first_name", None)
        data_usersheet["last_name"] = serializer.validated_data.get("last_name", None)
        data_usersheet["mobile"] = serializer.validated_data.get("mobile", None)
        data_usersheet["password"] = serializer.validated_data.get("password", None)
        data_usersheet["fonction"] = serializer.validated_data.get("fonction", None)
        data_usersheet["region"] = serializer.validated_data.get("region", None)
        data_usersheet["site"] = serializer.validated_data.get("site", None)
        data_usersheet["address"] = serializer.validated_data.get("address", None)
        data_usersheet["type"] = serializer.validated_data.get("type", None)
        data_usersheet["is_staff"] = serializer.validated_data.get("is_staff", True)
        data_usersheet["is_active"] = serializer.validated_data.get("is_active", True)
        data_usersheet["is_superuser"] = serializer.validated_data.get("is_superuser", False)
        serializer2 = UserSheetSerializer(data=data_usersheet)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()
        #token = AuthToken.objects.create(user)[1]
        token = default_token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.id_newuser))
        current_site = self.request.META['HTTP_HOST']
        print(current_site)
        region_ese = Eses.objects.filter(region=user.region).first()
        # client = get_tenant(self.request)
        nom_ese = region_ese.nom_ese
        sigle = region_ese.schema_sigle

        context ={
            "token":token,
            "uid":uid,
            "domaine":f"http://{current_site}",
            "nom_ese":nom_ese,
            "sigle":sigle,
            "region":region_ese.region,
        }

        text_html = render_to_string("create_user.html", context)
        msg = EmailMessage(
            "Compte utilisateur",
            text_html,
            f"{sigle} <socamaryde@gmail.com>",
            [user.email],
        )
        msg.content_subtype = "html"
        msg.send()
        return Response({
            'user_info':{
                'username':user.email,
                'last_name':user.last_name,
                'fonction':user.fonction,
                'type':user.type,
                'mobile':user.mobile,
                'region':user.region,
                'site':user.site,
                'id':user.id_newuser,
            },
            'token': token
        })



# --------------------- RECUPERATION DE MOT DE PASSE ----------------------------------#


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = NewUser.objects.filter(email=email).first()
        if user:
            print("Email envoyé")
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id_newuser))
            current_site = request.META['HTTP_HOST']

            context ={
                "token":token,
                "uid":uid,
                "domaine":f"http://{current_site}",
            }

            text_html = render_to_string("email.html", context)
            msg = EmailMessage(
                "Message Test de Soretac",
                text_html,
                "SORETAC <socamaryde@gmail.com>",
                [user.email]
            )
            msg.content_subtype = "html"
            msg.send()
        else:
            print("L'utilisateur n'existe pas")

    #return HttpResponseRedirect(redirect_to='/account/login/')
    return render(request, 'forgot_password.html', {})


def update_password(request, token, uid):
    print(token, uid)
    #client = get_tenant(request)
    try:
        user_id = urlsafe_base64_decode(uid)
        decode_id = codecs.decode(user_id, 'utf-8')
        user = NewUser.objects.get(id_newuser=decode_id)
        usersheet = UserSheet.objects.get(email=user.email)

    except:
        return HttpResponseForbidden("Utilisateur non identifié. Vous ne pouvez changer le mot de passe")

    check_token = default_token_generator.check_token(user, token)
    print(check_token)
    if not check_token:
        return HttpResponseForbidden("Utilisateur non identifié. Vous ne pouvez changer le mot de passe")

    error = False
    success = False
    message = ""
    if request.method == "POST":
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password == repassword:
            try:
                validate_password(password, user)
                if Eses.objects.filter(email=user.email).exists():
                    ese = Eses.objects.filter(email=user.email).first()
                    eses = Eses.objects.filter(email =user.email).first()
                    ese.mdp_admin = password
                    ese.save()
                    eses.mdp_admin_ese = password
                    eses.save()
                usersheet.password=password
                usersheet.save()
                user.set_password(password)
                user.save()


                success = True
                message = "Mot de passe modifié avec succès"
                return HttpResponseRedirect(redirect_to='/comptes/register/')

            except ValidationError as e:
                error=True
                message = str(e)
        else:
            error = True
            message = "Les deux mots de passe ne correspondent pas"
    context = {
        "error":error,
        "success": success,
        "message": message,
    }

    return render(request, 'update_password.html', context)



# class UpdateUser(generics.UpdateAPIView):
#     serializer_class = NewuserSerializer
#     queryset = NewUser.objects.all()
    
class ListNewUser(generics.ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = NewUser.objects.all()
    serializer_class = NewuserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('engin', 'date_compt', 'releveur_compteur', 'releve_compt')


class ListUser(generics.ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = UserSheet.objects.all()
    serializer_class = UserSheetSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('engin', 'date_compt', 'releveur_compteur', 'releve_compt')


class DetailUser(generics.RetrieveAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = UserSheet.objects.all()
    serializer_class = UserSheetSerializer
    lookup_field = 'pk'


class DeleteUser(generics.DestroyAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = NewUser.objects.all()
    serializer_class = NewuserSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        UserSheet.objects.filter(email=instance.email).first().delete()
        self.perform_destroy(instance)
        return self.destroy(request, *args, **kwargs)

