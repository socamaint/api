from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Eses
from .EntrepriseSerializer import EseSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from Ressources.RessourceSerializer import ImportEnginSerializer, VehiculeSerializer
from Ressources.models import Vehicules
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


class EseViews(ModelViewSet):
    serializer_class = EseSerializer
    queryset = Eses.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     return Eses.objects.filter(region=user.region)
   
    
class VehiculeViewSet(ModelViewSet):

    serializer_class = VehiculeSerializer
    queryset = Vehicules.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = VehiculeFilters
    search_fields = ["immat", "nparc", "affectation", "statut", "site", "marque", "modele", "nature"]
    ordering_fields = ["date_mse"]
    pagination_class = PageNumberPagination
    parser_classes =  [FormParser, MultiPartParser]



class ImportEnginView(APIView):
    serializer_class = ImportEnginSerializer
    parser_classes =  [FormParser, MultiPartParser]
    

    def post(self, request):
        

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
        for k in range(len(df)):
            if Vehicules.objects.filter(immat=str(df.iloc[k, 4]).upper()).first() == None:
                vehicule = {}                    

                vehicule['region'] = str(df.iloc[k, 1]).strip().upper()
                vehicule['nparc'] = str(df.iloc[k, 2]).strip().upper()
                vehicule['noptim'] = str(df.iloc[k, 3]).upper()
                vehicule['immat'] = str(df.iloc[k, 4]).strip().upper()
                vehicule['nature'] = str(df.iloc[k, 5]).strip().upper()
                vehicule['type'] = str(df.iloc[k, 6]).strip().upper()
                vehicule['marque'] = str(df.iloc[k, 7]).strip().upper()
                vehicule['modele'] = str(df.iloc[k, 8]).strip().upper()
                vehicule['serie'] = str(df.iloc[k, 9]).strip().upper()
                vehicule['energie'] = str(df.iloc[k, 10]).strip().upper()
                vehicule['puissance'] = str(df.iloc[k, 11]).strip().upper()
                vehicule['type_compt'] = str(df.iloc[k, 12] ).strip().upper()                  
                vehicule['annee_mes'] = str(df.iloc[k, 13])
                vehicule['statut'] = str(df.iloc[k, 14]).strip().upper()
                vehicule['affectation'] = str(df.iloc[k, 15]).strip().upper()
                vehicule['site'] = str(df.iloc[k, 16]).strip().upper()
                vehicule['alert_compt'] = str(df.iloc[k, 17]).strip().upper()
                vehicule['responsable_sabc'] = str(df.iloc[k, 18]).strip().upper()

                serializer_engin = VehiculeSerializer(data = vehicule)
                serializer_engin.is_valid(raise_exception=True)
                serializer_engin.save()
            else:
                j = k+1
                messages_errors.append("L'engin immatriculé " +str(df.iloc[k, 4])+ " de la ligne " +str(j)+ " existe déjà dans le parc")


        return Response({
            'status': True,
            'message': "Fichier des engin importé avec succès.",
            'messages_errors': messages_errors,
        }, status=status.HTTP_201_CREATED)