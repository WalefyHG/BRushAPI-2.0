from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    
    TIPO_CHOICES = (
        ('admin', 'Admin'),
        ('atleta', 'Atleta'),
        ('team', 'Team')
    )
    
    
    user_name = models.CharField(max_length=100, unique=True)
    user_email = models.CharField(max_length=100, unique=True)
    user_image = models.ImageField(upload_to='image/', null=True, blank=True, default='', max_length=255)
    user_birthday = models.DateField(null=True, blank=True)
    user_firstName = models.CharField(max_length=50)
    user_lastName = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    user_idioma = models.CharField(max_length=20)
    user_games = models.CharField(max_length=50)
    user_pais = models.CharField(max_length=20)
    user_banner = models.ImageField(upload_to='banner/', null=True, blank=True, default='', max_length=255)
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

class FriendShip(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    created = models.DateTimeField(auto_now_add=True)
    friendship_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', black=True, null=True)
    class Meta:
        unique_together = ['user', 'friend']


class Notices(models.Model):
    notice_id = models.AutoField(primary_key=True)
    notice_title = models.CharField(max_length=100)
    notice_content = models.TextField()
    notice_date = models.DateTimeField(auto_now_add=True)
    notice_image = models.ImageField(upload_to='newsImage/', null=True, blank=True, max_length=255)
    notice_writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_writer')
    
class UserCode(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True)
    verification_code_expires = models.DateTimeField(null=True)
    
    
    
class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    
    @property
    def room_name(self):
        sorted_ids = sorted([self.user1.id, self.user2.id])
        return f'{sorted_ids[0]}_{sorted_ids[1]}'
    
    @staticmethod
    def get_room_by_name(user1, user2):
        sorted_ids = sorted([user1.id, user2.id])
        room_name = f'{sorted_ids[0]}_{sorted_ids[1]}'
        
        room = ChatRoom.objects.filter(
            user1_id=sorted_ids[0], user2_id=sorted_ids[1]
        ).first()
        
        if not room:
            room = ChatRoom.objects.create(user1=user1, user2=user2)
        
        return room
    
class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} : {self.content}'
    