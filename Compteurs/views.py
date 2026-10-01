from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from Ressources.models import Vehicules
from .models import Compteur
from .CompteurSerializer import CompteurSerializer
from Ressources.models import NewUser
from rest_framework import status
from django.db.models import Q
from decimal import Decimal
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend





class CompteurCreate(ModelViewSet):
    serializer_class = CompteurSerializer

    def get_queryset(self): 
        myuser = self.request.user
        # return Compteur.objects.filter(Q(vehicule_id=self.kwargs['engin_pk']) & Q(vehicule__site__in=myuser.site)).select_related('vehicule')
        return Compteur.objects.filter(Q(vehicule_id=self.kwargs['engin_pk'])).select_related('vehicule')
        
   
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return {"engin_id": self.kwargs['engin_pk']}
    
    def create(self, request, *args, **kwargs):

        if request.data['compt_act'] == "":
            return Response({'message': "Compteur incorrect, Veuillez renseigner le compteur"},  status=status.HTTP_406_NOT_ACCEPTABLE)
        
        else:

            datacopy =  request.data.copy()
                        
            last_enrg = Compteur.objects.filter(vehicule_id=self.kwargs['engin_pk']).last()
            print("******------------*************--------------***********---------\n")
            print(last_enrg)
            if last_enrg != None:
                if int(datacopy['compt_act']) >= int(last_enrg.compt_act):
                    datacopy['last_compt'] = last_enrg.compt_act
                    datacopy['start_compt'] = last_enrg.start_compt
                    datacopy['ecart'] = int(datacopy['compt_act']) - int(last_enrg.start_compt)
                    print(datacopy['ecart'])
                    print("********************------------------------------\n")
                    datacopy['user_compt'] = self.request.user.id

                    serializer = self.get_serializer(data=datacopy)
                    serializer.is_valid(raise_exception=True)                        
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': "Compteur incorrect, donnant un écart négatif avec le précédent"},  status=status.HTTP_406_NOT_ACCEPTABLE)
        
            else:
                datacopy['last_compt'] = datacopy['compt_act']
                datacopy['start_compt'] = datacopy['compt_act']
                datacopy['ecart'] = 0
                datacopy['user_compt'] = self.request.user.id

                serializer = self.get_serializer(data=datacopy)
                serializer.is_valid(raise_exception=True)                        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
