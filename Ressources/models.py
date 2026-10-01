from django.db import models
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core import validators
import uuid



class Vehicules(models.Model):

    COMPT = [
        ("H", "H"),
        ("KM", "KM"),
    ]
    region = models.CharField(max_length=50, blank=True, null=True)
    nparc = models.CharField(max_length=20, blank=True, null=True)
    noptim = models.CharField(max_length=20, blank=True, null=True)
    immat = models.CharField(max_length=20, blank=True, null=True)
    nature = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    marque = models.CharField(max_length=50, blank=True, null=True)
    modele = models.CharField(max_length=50, blank=True, null=True)
    serie = models.CharField(max_length=50, blank=True, null=True)
    energie = models.CharField(max_length=20, blank=True, null=True)
    puissance = models.CharField(max_length=15, blank=True, null=True)
    type_compt = models.CharField(max_length=10, choices=COMPT)
    annee_mes = models.CharField(max_length=20, blank=True, null=True)
    statut = models.CharField(max_length=20, blank=True, null=True)
    affectation = models.CharField(max_length=100, blank=True, null=True)
    site = models.CharField(max_length=20, blank=True, null=True)
    responsable_sabc = models.CharField(max_length=255, blank=True, null=True)
    alert_compt = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.region}_{self.noptim}_{self.nature}_{self.marque}_{self.type}"




# MODELS DES UTILISATEURS


class ClientUserManager(BaseUserManager):
    def _create_user(self, region, email, password, first_name, last_name, username, mobile, address, type, fonction, site, **extra_fields):
        if not email:
            raise ValueError("Vous devez fournir une adresse mail")
        if not password:
            raise ValueError('Vous devez fournir un mot de passe')

        NewUser = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            mobile = mobile,
            region = region,
            fonction = fonction,
            address = address,
            type = type,
            site = site,

            **extra_fields
        )

        NewUser.set_password(password)
        NewUser.save(using=self._db)
        return NewUser

    def create_user(self, region, email, password, first_name, last_name, username, mobile, address, type, fonction, site, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(region, email, password, first_name, last_name, username, mobile, address, type, fonction, site, **extra_fields)

    def create_superuser(self, region, email, password, first_name, last_name, username, mobile, address, type, fonction, site, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(region, email, password, first_name, last_name, username, mobile, address, type, fonction, site, **extra_fields)


# Create your User Model here.
class NewUser(AbstractBaseUser,PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default

    TYPEUSERS = [
        ('OPERATEUR', 'OPERATEUR'),
        ('CHEF_ZONE', 'CHEF_ZONE'),
        ('CHEF_ATELIER', 'CHEF_ATELIER'),
        ('CHEF_AGENCE', 'CHEF_AGENCE'),
        ('MASTER_DATA', 'MASTER_DATA'),
        ('DIRECTEUR', 'DIRECTEUR')
        
    ]    

    id_newuser = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    email = models.EmailField(db_index=True, unique=True, max_length=254, validators=[validators.EmailValidator(message="Email invalide")],)
    username = models.CharField(max_length=255, null=True,blank=True)
    first_name = models.CharField(max_length=240, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, blank=True, choices=TYPEUSERS)
    mobile = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    fonction = models.CharField(max_length=255, null=True,blank=True)
    region = models.CharField(max_length=255, null=True,blank=True)
    site = models.CharField(max_length=255, null=True,blank=True)
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(blank=True, null=True)
    

    is_staff = models.BooleanField(default=True) # must needed, otherwise you won't be able to login to django-admin.
    is_active = models.BooleanField(default=True) # must needed, otherwise you won't be able to login to django-admin.
    is_superuser = models.BooleanField(default=False) # this field we inherit from PermissionsMixin.

    objects = ClientUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','last_name', 'mobile', 'type', 'first_name', 'region', 'site']


    @property
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    
    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.region} - {self.region} - {self.site}"

    
class UserSheet(models.Model):
    id            = models.BigAutoField(primary_key=True, unique=True)
    type          = models.CharField("TYPE", max_length=50, blank=True)
    email         = models.CharField("EMAIL", max_length=100, blank=True)
    username      = models.CharField("Username", max_length=255, null=True,blank=True) 
    password      = models.CharField("MOT DE PASSE", max_length=100, blank=True)
    first_name    = models.CharField("PRENOM", max_length=240, blank=True)
    last_name     = models.CharField("NOM", max_length=255, blank=True)
    mobile        = models.CharField("N° TELEPHONE", max_length=255, blank=True)
    address       = models.CharField("ADRESSE", max_length=255, null=True, blank=True)
    fonction      = models.CharField("POSTE", max_length=255, null=True,blank=True)
    type          = models.CharField("TYPE PERSONNEL", max_length=50)
    region        = models.CharField("Région", max_length=255, null=True,blank=True)
    site          = models.CharField("Site", max_length=255, null=True,blank=True)
    is_staff      = models.BooleanField("STAFF", default=True)
    is_active     = models.BooleanField("ACTIF", default=True)
    is_superuser  = models.BooleanField("SUPER UTILISATEUR", default=False)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.region} - {self.site} - {self.type}"