from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
import datetime
from django.db.models import Q
from Preventive.PreventSerializer import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from django.shortcuts import get_object_or_404


# </head>

# class CompteurViews(ModelViewSet):
#     serializer_class = CompteurSerializer
#     def get_queryset(self): 
#         users = self.request.user
#         return Compteur.objects.filter(Q(veh_id=self.kwargs['engin_pk'])).select_related('compteur_veh')


#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return {"engin_id": self.kwargs['engin_pk']}



#     def create(self, request, *args, **kwargs):
        
#         data =  request.data.copy()
                    
#         # last_enrg = Compteur.objects.filter(veh_id=data["veh"]).last('id')
#         # print(last_enrg)
#         # if last_enrg != None:
#         suivi = SuiviEp.objects.filter(veh=data["veh"]).first()
#         compt_act = suivi.cpt_actuel
#         if compt_act > int(data["compt"]):
#             return Response({'message': "Compteur incorrect, Veuillez renseigner le compteur"},  status=status.HTTP_406_NOT_ACCEPTABLE)

#         else:
#             data_s = {}
#             stat = ""
#             cptnext_ep = suivi.cpt_next_ep
#             ecrt = int(data["compt"]) - int(cptnext_ep)
#             # suivi.cpt_actuel = int(data["compt"])
#             # suivi.ecart = ecrt

#             vehicule = Vehicules.objects.filter(id=data["veh"]).first()
#             typcompt = vehicule.type_compt
#             typveh = vehicule.type
#             alertcompt = int(vehicule.alert_compt)
            
#             if ecrt >= alertcompt and ecrt <= 0:
#                 # suivi.statut = "A vidanger"
#                 stat = "A VIDANGER"
#             elif ecrt > 0:
#                 # suivi.statut = "En dépassement"
#                 stat = "EN DEPASSEMENT"
#             else:
#                 # suivi.statut = "R.A.S"
#                 stat = "RAS"


#             data_s['veh'] = data["veh"]
#             data_s['cpt_actuel'] = data["compt"]
#             data_s['ecart'] = ecrt
#             data_s['statut'] = stat
#             # data_s['responsable'] = vehicule.responsable_sabc
#             # data_s['last_ep'] = 
#             # data_s['date_last_ep'] = 
#             # data_s['cpt_last_ep'] = 
#             # data_s['cpt_next_ep'] =                   
#             # data_s['program_ep'] = 
#             # data_s['bt'] = 
            

#             serializer = SuiviEpSerializer(suivi, data=data_s, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             serializer_compt = self.serializer_class(data=request.data)
#             serializer_compt.is_valid(raise_exception=True)
#             serializer_compt.save()
#             return Response(serializer_compt.data, status=status.HTTP_200_OK)




# CRUD POUR SUIVI EP

class CreateSuiviEP(CreateAPIView):
    serializer_class = SuiviEpSerializer
    queryset = SuiviEp.objects.all()
    parser_classes = [FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        EP_MN = ['250 H', '500 H', '750 H', '1000 H', '1250 H', '1500 H', '1750 H', '2000 H']
        EP_VL = ['5000 KM', '10000 KM', '15000 KM', '20000 KM', '25000 KM', '30000 KM']
        EP_PL = ['150 H', '300 H', '450 H', '600 H', '750 H', '900 H', '1050 H', '1200 H']
        list_epch = ["CH SF", "CH DF"]
        data = request.data.copy()
        
        suivi = SuiviEp.objects.filter(vehicule_id=data["vehicule"]).first()
        if suivi != None:
            return Response({'message': "Le suivi de cet engin existe déjà. Vous pouvez plutôt le modifier!"},  status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            veh = Vehicules.objects.filter(id=data["vehicule"]).first()
            if veh.type in list_epch:
                cpt_next = int(data["cpt_last_ep"]) + 250
                data["cpt_next_ep"] = cpt_next
                ecrt = int(data["cpt_actuel"]) - cpt_next
                data["ecart"] = ecrt
                i = int(EP_MN.index(data["last_ep"])) + 9
                data['program_ep'] = EP_MN[i % 8]

            elif veh.type == "VL":
                cpt_next = int(data["cpt_last_ep"]) + 5000
                data["cpt_next_ep"] = cpt_next
                ecrt = int(data["cpt_actuel"]) - cpt_next
                data["ecart"] = ecrt
                i = int(EP_VL.index(data["last_ep"])) + 7
                data['program_ep'] = EP_VL[i % 6]

            elif veh.type == "PL":
                cpt_next = int(data["cpt_last_ep"]) + 150
                data["cpt_next_ep"] = cpt_next
                ecrt = int(data["cpt_actuel"]) - cpt_next
                data["ecart"] = ecrt
                i = int(EP_PL.index(data["last_ep"])) + 9
                data['program_ep'] = EP_PL[i % 8]

            
            if ecrt >= veh.alert_compt and ecrt <= 0:
                stat = "A VIDANGER"

            elif ecrt > 0:  
                stat = "EN DEPASSEMENT"

            else:      
                stat = "RAS"

            data["statut"] = stat

            suivi = SuiviEpSerializer(data=data)
            suivi.is_valid(raise_exception=True)
            suivi.save()
            
            return Response(suivi.data, status=status.HTTP_201_CREATED)


class ListSuiviEP(ListAPIView):
    serializer_class = SuiviEpSerializer
    queryset = SuiviEp.objects.all()
    parser_classes = [FormParser, MultiPartParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["vehicule", "statut", "program_ep", "last_ep"]
    ordering_fields = ["statut"]
    pagination_class = PageNumberPagination



class UpdateSuiviEP(RetrieveUpdateAPIView):
    serializer_class = UpdateSuiviEpSerializer
    queryset = SuiviEp.objects.all()
    parser_classes = [FormParser, MultiPartParser]

    def perform_update(self, serializer):
        return super().perform_update(serializer)

    def patch(self, request, *args, **kwargs):
        list_epch = ["CH SF", "CH DF"]
        EP_MN = ['250 H', '500 H', '750 H', '1000 H', '1250 H', '1500 H', '1750 H', '2000 H']
        EP_VL = ['5000 KM', '10000 KM', '15000 KM', '20000 KM', '25000 KM', '30000 KM']
        EP_PL = ['150 H', '300 H', '450 H', '600 H', '750 H', '900 H', '1050 H', '1200 H']
        partial = kwargs.pop('partial', False) # Detects if PATCH or PUT was used
        instance = self.get_object()
        data=request.data

        if instance.type in list_epch:
            cpt_next = int(instance["cpt_last_ep"]) + 250
            instance["cpt_next_ep"] = cpt_next
            # ecrt = int(instance["cpt_actuel"]) - cpt_next
            # instance["ecart"] = ecrt
            i = int(EP_MN.index(instance["last_ep"])) + 9
            instance['program_ep'] = EP_MN[i % 8]
            # data["ecart"] = ecrt
            data["program_ep"] = EP_MN[i % 8]
        
        elif instance.type == "VL":
            cpt_next = int(instance["cpt_last_ep"]) + 5000
            instance["cpt_next_ep"] = cpt_next
            ecrt = int(instance["cpt_actuel"]) - cpt_next
            instance["ecart"] = ecrt
            i = int(EP_VL.index(instance["last_ep"])) + 7
            instance['program_ep'] = EP_VL[i % 6]
            data["ecart"] = ecrt
            data['program_ep'] = EP_VL[i % 6]
        
        elif instance.type == "PL":
            cpt_next = int(instance["cpt_last_ep"]) + 150
            instance["cpt_next_ep"] = cpt_next
            ecrt = int(instance["cpt_actuel"]) - cpt_next
            instance["ecart"] = ecrt
            i = int(EP_PL.index(instance["last_ep"])) + 9
            instance['program_ep'] = EP_PL[i % 8]
            data["ecart"] = ecrt
            data['program_ep'] = EP_PL[i % 8]
        
        
        if ecrt >= instance.alert_compt and ecrt <= 0:
            stat = "A VIDANGER"
        
        elif ecrt > 0:  
            stat = "EN DEPASSEMENT"
        
        else:      
            stat = "RAS"
        
        data["statut"] = stat

        serializer = self.get_serializer(instance, data=data, partial=partial)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {"message": "Mis à jour avec succès!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    

class DeleteSuiviEP(DestroyAPIView):
    serializer_class = SuiviEpSerializer
    queryset = SuiviEp.objects.all()
    parser_classes = [FormParser, MultiPartParser]



class ImportSuiviEP(CreateAPIView):
    serializer_class = ImportSuiviEPSerializer
    parser_classes =  [FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        
        data = request.FILES
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': 'Pourvoir un fichier valide'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        excel_file = data.get('file')
        df = pd.read_excel(excel_file, sheet_name=0)
        
        messages_errors = []
        messages_success = []
        for k in range(len(df)):
            vehicule = Vehicules.objects.filter(noptim=str(df.iloc[k, 2]).strip()).first()
            if vehicule != None:
                suiviep = SuiviEp.objects.filter(vehicule_id=vehicule.id).first()
                if suiviep == None:
                    impsuivi = {}                    
            
                    impsuivi['veh'] = vehicule.id
                    impsuivi['region'] = vehicule.region
                    impsuivi['last_ep'] = str(df.iloc[k, 7]).upper()
                    impsuivi['date_last_ep'] = datetime.date.strptime(str(df.iloc[k, 9]).strip().upper(),"%Y-%m-%d %H:%M:%S") 
                    impsuivi['cpt_last_ep'] = str(df.iloc[k, 8]).strip().upper()
                    impsuivi['cpt_next_ep'] = str(df.iloc[k, 10]).strip().upper()
                    impsuivi['cpt_actuel'] = str(df.iloc[k, 11]).strip().upper()
                    impsuivi['ecart'] = str(df.iloc[k, 12]).strip().upper()
                    impsuivi['statut'] = str(df.iloc[k, 13]).strip().upper()
                    impsuivi['program_ep'] = str(df.iloc[k, 14]).strip().upper()
                    impsuivi['bt'] = str(df.iloc[k, 15]).strip().upper()
                    impsuivi['responsable'] = str(df.iloc[k, 1]).strip().upper()

                    serializer_suivi = SuiviEpSerializer(data=impsuivi)
                    serializer_suivi.is_valid(raise_exception=True)
                    serializer_suivi.save()
                    j = k+1
                    messages_success.append("Le suivi de la ligne " +str(j)+  " pour l'engin " +str(df.iloc[k, 2])+  " a été enregistré avec succès")


                else:
                    j = k+1
                    messages_errors.append("L'engin " +str(df.iloc[k, 2])+ " de la ligne " +str(j)+ " existe déjà dans le Suivi EP; il y'aurait 02 suivi pour un meme engin")
            
            else:
                j = k+1
                messages_errors.append("L'engin " +str(df.iloc[k, 2])+ " de la ligne " +str(j)+ " n'existe pas dans ce parc automobile")
                    

        return Response({
            'status': True,
            'message': "Suivi des EP importé avec succès.",
            'messages_success': messages_success,
            'messages_errors': messages_errors,
        }, status=status.HTTP_201_CREATED)

    
    