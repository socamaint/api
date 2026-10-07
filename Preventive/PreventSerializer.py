from rest_framework import serializers
from .models import SuiviEp, PlanningEp


class SuiviEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviEp
        fields = ["id", "region", "vehicule", "last_ep", "date_last_ep", "cpt_last_ep", "cpt_next_ep", "cpt_actuel", "ecart", "statut", "program_ep", "bt", "responsable"]
        read_only_fields = ["statut", "ecart"]
        

class UpdateSuiviEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviEp
        fields = ["id", "region", "vehicule", "last_ep", "date_last_ep", "cpt_last_ep", "cpt_next_ep", "cpt_actuel", "ecart", "statut", "program_ep", "bt", "responsable"]
        read_only_fields = [ "ecart", "statut"]
        required_fields = [ "ecart", "statut"]


class PlanningEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningEp
        fields = ["veh", "compt_ep", "date_recept", "date_ent", "type_ep", "etat", "statut", "numbt", "observation"]



class ImportSuiviEPSerializer(serializers.Serializer):
   file = serializers.FileField()