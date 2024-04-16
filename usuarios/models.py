from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    
    TIPO_CHOICES = (
        ('admin', 'Admin'),
        ('atleta', 'Atleta'),
        ('team', 'Team')
    )
    
    
    user_name = models.CharField(max_length=20, unique=True)
    user_email = models.CharField(max_length=50, unique=True)
    user_image = models.ImageField(upload_to='image/', null=True, blank=True, default='')
    user_birthday = models.DateField(null=True, blank=True)
    user_firstName = models.CharField(max_length=50)
    user_lastName = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    user_idioma = models.CharField(max_length=20)
    user_games = models.CharField(max_length=50)
    user_pais = models.CharField(max_length=20)
    user_banner = models.ImageField(upload_to='banner/', null=True, blank=True, default='')
    user_youtube = models.CharField(max_length=100, null=True, blank=True, default='')
    user_twitch = models.CharField(max_length=100, null=True, blank=True, default='')
    user_instagram = models.CharField(max_length=100, null=True, blank=True, default='')
    user_twitter = models.CharField(max_length=100, null=True, blank=True, default='')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='atleta')
    username = None
    
    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['id', 'password']
    
    class Meta:
        pass
    
User._meta.get_field('groups').remote_field.related_name = 'usuarios_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'usuarios_user_permissions'


class Notices(models.Model):
    notice_id = models.AutoField(primary_key=True)
    notice_title = models.CharField(max_length=100)
    notice_content = models.TextField()
    notice_date = models.DateTimeField(auto_now_add=True)
    notice_image = models.ImageField(upload_to='newsImage/', null=True, blank=True)
    notice_writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_writer')
    
class UserCode(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True)
    verification_code_expires = models.DateTimeField(null=True)