from django.db import models
from Ressources.models import Vehicules, NewUser



class Compteur(models.Model):
    
    STATUT_COMPT = [
        ("USUEL", "USUEL"),
        ("EP", "EP"),    
    ]

    vehicule            = models.ForeignKey(Vehicules, null=True, on_delete= models.SET_NULL, related_name='vehicule_compteur')
    start_compt         = models.PositiveIntegerField(blank=True, null=True)
    last_compt          = models.PositiveIntegerField(blank=True, null=True)
    compt_act           = models.PositiveIntegerField(blank=True, null=True)
    date_compt          = models.DateTimeField(auto_now_add=True)
    user_compt          = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, related_name="compteur_user")
    ecart               = models.FloatField()
    statut_compt        = models.CharField(max_length=15, choices=STATUT_COMPT, default="USUEL")

    def __str__(self):
        return f"{self.vehicule.nparc} - {self.compt_act} - {self.date_compt}"