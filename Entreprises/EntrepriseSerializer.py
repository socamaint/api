from rest_framework import serializers
from .models import Eses

class EseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eses
        fields = ['id', 'region', 'created_on', 'nom_ese', 'schema_sigle', 'description_ese', 'email', 'mobile', 'logo_ese']


