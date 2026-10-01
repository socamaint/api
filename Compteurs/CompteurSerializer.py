from rest_framework import serializers
from .models import Compteur


class CompteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compteur
        fields = ["id", "vehicule", "start_compt", "last_compt", "compt_act", "user_compt", "date_compt" ,"ecart", "statut_compt"]
        # read_only_fields = ["vehicule", "start_compt", "last_compt", "user_compt", "date_compt" ,"ecart", "statut_compt"]
        # required_fields = ["vehicule", "start_compt", "last_compt", "user_compt", "date_compt" ,"ecart", "statut_compt"]
        

    def create(self, validated_data):
        engin_id = self.context['engin_id'] 
        return Compteur.objects.create(vehicule_id=engin_id, **validated_data)

