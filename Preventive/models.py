from django.db import models
from Ressources.models import Vehicules, NewUser


class SuiviEp(models.Model):

    STATUT = [
        ("RAS", "RAS"),
        ("A VIDANGER", "A VIDANGER"),
        ("EN DEPASSEMENT", "EN DEPASSEMENT")
    ]

    EP = [
        ("250 H", "250 H"),
        ("500 H", "500 H"),
        ("750 H", "750 H"),
        ("1000 H", "1000 H"),
        ("1250 H", "1250 H"),
        ("1500 H", "1500 H"),
        ("1750 H", "1750 H"),
        ("2000 H", "2000 H"),
        ("", ""),
        ("5000 KM", "5000 KM"),
        ("10000 KM", "10000 KM"),
        ("15000 KM", "15000 KM"),
        ("20000 KM", "20000 KM"),
        ("25000 KM", "25000 KM"),
        ("30000 KM", "30000 KM"),
        ("", ""),
        ("150 H", "150 H"),
        ("300 H", "300 H"),
        ("450 H", "450 H"),
        ("600 H", "600 H"),
        ("750 H", "750 H"),
        ("900 H", "900 H"),
        ("1050 H", "1050 H"),
        ("1200 H", "1200 H"),

    ]

    vehicule = models.ForeignKey(Vehicules, on_delete=models.SET_NULL, null=True, related_name="suivi_veh")
    region = models.CharField("Région", max_length=50, null=True, blank=True)
    last_ep = models.CharField(max_length=10, blank=True, null=True, choices=EP)
    date_last_ep = models.DateField(max_length=30, blank=True, null=True)
    cpt_last_ep = models.PositiveIntegerField()
    cpt_next_ep = models.PositiveIntegerField()
    cpt_actuel = models.PositiveIntegerField()
    # ecart = models.FloatField()
    # statut = models.CharField(max_length=30, blank=True, null=True, choices=STATUT)
    program_ep = models.CharField(max_length=20, choices=EP, blank=True, null=True)
    bt = models.CharField(max_length=30, blank=True, null=True)
    responsable = models.CharField(max_length=255, blank=True, null=True)


    @property
    def ecart(self):
        return self.cpt_actuel - self.cpt_next_ep


    @property
    def statut(self):
        alt = self.vehicule.alert_compt
        if self.ecart >= alt and self.ecart <= 0:
            stat =  "A VIDANGER"
        elif self.ecart > 0:  
            stat = "EN DEPASSEMENT"
        else:
            stat = "RAS"
        return stat


    def __str__(self):
        return f"{self.vehicule} - {self.statut} - {self.program_ep}"





class PlanningEp(models.Model):

    ETAT = [
        ("EFFECTUE", "EFFECTUE"),
        ("NON EFFECTUE", "NON EFFECTUE"),
    ]

    STATUT = [
        ("PLANIFIE", "PLANIFIE"),
        ("NON PLANIFIE", "NON PLANIFIE"),
    ]

    OBSERV = [
        ("", ""),
        ("ENGIN PAS LIBERE", "ENGIN PAS LIBERE"),
        ("COMPTEUR NON ECHU", "COMPTEUR NON ECHU"),
        ("ENGIN EN PANNE", "ENGIN EN PANNE"),
    ]

    veh = models.ForeignKey(Vehicules, on_delete=models.SET_NULL, null=True, related_name="planning_veh")
    compt_ep = models.PositiveIntegerField(blank=True, null=True)
    date_recept = models.DateField()
    date_ent = models.DateField()
    type_ep = models.CharField(max_length=15)
    etat = models.CharField(max_length=15, choices=ETAT, default="NON EFFECTUE")
    statut = models.CharField(max_length=15, choices=STATUT, default="PLANIFIE")
    numbt = models.CharField(max_length=20, blank=True, null=True)
    observation = models.CharField(max_length=255, blank=True, null=True, choices=OBSERV)

    def __str__(self):
        return f"{self.veh.nparc} - {self.type_ep} - {self.etat}"
