from django.db import models
import uuid
from django.core import validators


class Eses(models.Model):
    
    region              = models.CharField(max_length=255, unique=True)                         # Nom de location de l'entreprise dans la BD                                 
    created_on          = models.DateField("Date Enregistrement", auto_now_add=True)                                     # Date de creation de la location de l'entreprise
    nom_ese             = models.CharField("Nom Entreprise", max_length=255, blank=False, unique=True)
    schema_sigle        = models.CharField("Sigle Entreprise", max_length=255, unique=True)
    description_ese     = models.TextField("Description Entreprise", null=True, blank=True, default="Faire une description")
    email               = models.EmailField("Email Entreprise", max_length=255, unique=True, validators=[validators.EmailValidator(message="Email invalide")])
    mobile              = models.CharField("N° Telephone", max_length=255, blank=False, null=True)
    logo_ese            = models.ImageField("Logo Entreprise", upload_to='logos/', null=True, blank=True, default="logo_socamar.jpg")

    def __str__(self):
        return "{} ({}) - {}".format(self.nom_ese, self.schema_sigle, self.mobile)