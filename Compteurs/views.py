from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from Ressources.models import Vehicules
from .models import Compteur
from Preventive.models import SuiviEp
from Preventive.PreventSerializer import SuiviEpSerializer
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

            data_s = {}
            vehicule = Vehicules.objects.filter(id=self.kwargs['engin_pk']).first()
            data =  request.data.copy()
            stat = ""
            datacopy =  request.data.copy()
            suivi = SuiviEp.objects.filter(vehicule_id=self.kwargs['engin_pk']).first()
            if suivi != None:
                if int(datacopy['compt_act']) >= int(suivi.cpt_actuel):
                    ecrt = int(data["compt_act"]) - int(suivi.cpt_next_ep)
                    alertcompt = int(vehicule.alert_compt)
                    
                    if ecrt >= alertcompt and ecrt <= 0:
                        stat = "A VIDANGER"
                    elif ecrt > 0:   
                        stat = "EN DEPASSEMENT"
                    else:  
                        stat = "RAS"


                    data_s['vehicule'] = self.kwargs['engin_pk']
                    data_s['cpt_actuel'] = data["compt_act"]
                    data_s['ecart'] = ecrt
                    data_s['statut'] = stat

                    serializer = SuiviEpSerializer(suivi, data=data_s, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                
                    datacopy['last_compt'] = suivi.cpt_actuel
                    datacopy['start_compt'] = suivi.cpt_last_ep
                    datacopy['ecart'] = int(datacopy['compt_act']) - int(suivi.cpt_next_ep)
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
                data_t = data.copy()

                data_t['vehicule'] = self.kwargs['engin_pk']
                data_t['region'] = vehicule.region
                data_t['cpt_last_ep'] = 0
                data_t['cpt_next_ep'] = int(data['compt_act']) + 250
                data_t['cpt_actuel'] = data['compt_act']
                data_t['start_compt'] = data['compt_act']
                data_t['ecart'] = 0
                data_t['statut'] = "RAS"
                data_t['responsable'] = vehicule.responsable_sabc

                serializer = SuiviEpSerializer(data=data_t)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                datacopy['start_compt'] = datacopy['compt_act']
                datacopy['user_compt'] = self.request.user.id
                datacopy['ecart'] = 0
                print(datacopy['ecart'])
                print("********************------------------------------\n")
                datacopy['user_compt'] = self.request.user.id

                serializer = self.get_serializer(data=datacopy)
                serializer.is_valid(raise_exception=True)                        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)