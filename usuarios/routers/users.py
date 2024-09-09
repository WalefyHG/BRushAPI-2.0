from typing import Optional
from django.http import JsonResponse
from ninja import UploadedFile, Form, File
from ninja_extra import route, api_controller
from main.permissions import AdminAcess
from utils.sending_code import sending_code
from ..models import FriendShip, User, UserCode, ChatMessage
from ..schemas import UserOut, UserIn, UserOutFriendShip, UserResponse, UserPut, UserChangePassword, UserSocialMedias, ReadCount
from datetime import datetime
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.hashers import make_password, check_password
from ninja_extra.exceptions import HttpError
from django.utils import timezone as django_timezone

@api_controller(
    "users/",
    auth=JWTAuth(),
    tags=["Usuarios - Publico"],
)

class UserPublicContoller:
    @route.get('/pegarAll', response={200: list[UserOut]})
    def get_all_users(self, request):
        users = User.objects.all()
        serialized_users = []
        for user in users:
            user_out = UserOut(
            id=user.id,
            user_name=user.user_name,
            user_email=user.user_email,
            user_birthday=user.user_birthday,
            user_firstName=user.user_firstName,
            user_lastName=user.user_lastName,
            user_idioma=user.user_idioma,
            user_games=user.user_games,
            user_pais=user.user_pais,
            user_youtube=user.user_youtube,
            user_twitch=user.user_twitch,
            user_instagram=user.user_instagram,
            user_twitter=user.user_twitter,
            is_confirmed=user.is_confirmed,
            tipo=user.tipo,
            
            )
            
            if user.user_image:
                user_out.user_image = user.user_image.url
            if user.user_banner:
                user_out.user_banner = user.user_banner.url
            serialized_users.append(user_out)
        return serialized_users

    @route.get('/perfil', response={200: UserOut})
    def get_user_by_token(self, request):
        return request.auth
    
    
    @route.post('/criando', auth=None, response={200: UserResponse, 302: str})
    def create_user(self, request, user: UserIn, image: UploadedFile = File(None)):
        password_hash = make_password(user.password)
        verificarion_data = User.objects.filter(user_email=user.user_email).first()
        
    
        if(verificarion_data):
            if(user.user_email == verificarion_data.user_email):
                raise HttpError(302,"Email já cadastrado")
            elif(user.user_name == verificarion_data.user_name):
                raise HttpError(302,"Nome de usuário já cadastrado")
        else:
            user_data = User.objects.create(
                user_name=user.user_name,
                user_email=user.user_email,
                password=password_hash,
                user_birthday=user.user_birthday,
                user_firstName=user.user_firstName,
                user_lastName=user.user_lastName,
                user_idioma= user.user_idioma,
                user_games= user.user_games,
                user_pais= user.user_pais,
                is_confirmed = user.is_confirmed,
                tipo = user.tipo,
            )
            if(image):
                user_data.user_image = image

        user_data.save()
        
        if user.is_confirmed == False:
            sending_code(user_data)
            return {"mensagem": "Usuário criado com sucesso, verifique seu email para confirmar o cadastro"}
    
    @route.get('/perfil/{user_name}', response={200: UserOutFriendShip})
    def get_user_perfil_by_username(self, request, user_name: str):
        user = User.objects.get(user_name=user_name)
        user_friendShip_Status = FriendShip.objects.filter(user=request.auth, friend=user).first()
        user_out = UserOutFriendShip(
            id=user.id,
            user_name=user.user_name,
            user_email=user.user_email,
            user_birthday=user.user_birthday,
            user_firstName=user.user_firstName,
            user_lastName=user.user_lastName,
            user_idioma=user.user_idioma,
            user_games=user.user_games,
            user_pais=user.user_pais,
            user_youtube=user.user_youtube,
            user_twitch=user.user_twitch,
            user_instagram=user.user_instagram,
            user_twitter=user.user_twitter,
            is_confirmed=user.is_confirmed,
            tipo=user.tipo,
            friend_ship_request=False,
            are_friends=False,
            friendship_status=user_friendShip_Status.friendship_status
        )
        current_user = request.auth
        friend_ship_request = FriendShip.objects.filter(user=current_user, friend=user, friendship_status='pending' ).exists()
        
        are_friends = FriendShip.objects.filter(user=current_user, friend=user, friendship_status= 'accepted').exists() or \
                      FriendShip.objects.filter(user=user, friend=current_user, friendship_status= 'accepted').exists()
        
        if user.user_image:
            user_out.user_image = user.user_image.url
        if user.user_banner:
            user_out.user_banner = user.user_banner.url
            
        
        user_out.friend_ship_request = friend_ship_request
        user_out.are_friends = are_friends
        return user_out
    
    @route.get('/usuario/{id}', response={200: UserOut})
    def get_user_by_id(self, request, id: int):
        user = User.objects.get(id=id)
        user_out = UserOut(
            id=user.id,
            user_name=user.user_name,
            user_email=user.user_email,
            user_birthday=user.user_birthday,
            user_firstName=user.user_firstName,
            user_lastName=user.user_lastName,
            user_idioma=user.user_idioma,
            user_games=user.user_games,
            user_pais=user.user_pais,
            user_youtube=user.user_youtube,
            user_twitch=user.user_twitch,
            user_instagram=user.user_instagram,
            user_twitter=user.user_twitter,
            is_confirmed=user.is_confirmed,
            tipo=user.tipo,
        )
        
        if user.user_image:
            user_out.user_image = user.user_image.url
        if user.user_banner:
            user_out.user_banner = user.user_banner.url
        return user_out

    @route.get('/pesquisar/{user_firstName}', response={200: list[UserOut]}, auth=None)
    def get_user_by_userfirstname(self, request, user_firstName: str):
        users = User.objects.filter(user_firstName__icontains=user_firstName)
        serialized_users = []
        for user in users:
            user_out = UserOut(
            id=user.id,
            user_name=user.user_name,
            user_email=user.user_email,
            user_birthday=user.user_birthday,
            user_firstName=user.user_firstName,
            user_lastName=user.user_lastName,
            user_idioma=user.user_idioma,
            user_games=user.user_games,
            user_pais=user.user_pais,
            user_youtube=user.user_youtube,
            user_twitch=user.user_twitch,
            user_instagram=user.user_instagram,
            user_twitter=user.user_twitter,
            is_confirmed=user.is_confirmed,
            tipo=user.tipo,
            )
            
            if user.user_image:
                user_out.user_image = user.user_image.url
            if user.user_banner:
                user_out.user_banner = user.user_banner.url
        serialized_users.append(user_out)
        return serialized_users
    
    @route.put('/atualizar/{id}', response={200: UserResponse}, auth=None)
    def update_user(self, request, id: int, user: UserPut, image: UploadedFile = File(None), banner: UploadedFile = File(None)):
        user_data = User.objects.get(id=id)
        user_data.user_name = user.user_name
        user_data.user_email = user.user_email
        user_data.user_birthday = user.user_birthday
        user_data.user_firstName = user.user_firstName
        user_data.user_lastName = user.user_lastName
        user_data.user_idioma = user.user_idioma
        user_data.user_games = user.user_games
        user_data.user_pais = user.user_pais
        user_data.user_youtube = user.user_youtube
        user_data.user_twitch = user.user_twitch
        user_data.user_instagram = user.user_instagram
        user_data.user_twitter = user.user_twitter
        user_data.tipo = user.tipo
        if image:
            user_data.user_image = image
        if banner:
            user_data.user_banner = banner
        user_data.save()
        return {"mensagem": "Usuário atualizado com sucesso"}
    
    @route.delete('/deletar', response={200: UserResponse}, permissions=[AdminAcess])
    def delete_user(self, request):
        user = request.auth
        user.delete()
        return {"mensagem": "Usuário deletado com sucesso"}
    
    @route.post('/verificar_codigo/{code}', response={200: UserResponse}, auth=None)
    def verify_code(self, request, code: str):
        try:
            user = UserCode.objects.get(verification_code=code)
            user_data = User.objects.get(id=user.user_id_id)
            if user_data:
                user_data.is_confirmed = True
                user_data.save()
                user.delete()
                return {"mensagem": "Usuário confirmado com sucesso"}
            else:
                return {"mensagem": "Usuário não encontrado"}
        except:
            return {'mensagem': 'Código inválido'}
        
        
    @route.put('/atualizar_senha', response={200: UserResponse}, auth=None)
    def update_password(self, request, change_password: UserChangePassword):
        user = request.auth
        if change_password.senha_nova == change_password.confirmar_senha:
            if check_password(change_password.senha_atual, user.password):
                user.password = make_password(change_password.senha_nova)
                user.save()
                return {"mensagem": "Senha atualizada com sucesso"}
            else:
                return HttpError(400, "Senha atual incorreta")
        else:
            return HttpError(402, "Senhas não coincidem")
        
        
        
    @route.post('/enviar_codigo', response={200: UserResponse})
    def send_code(self, request):
        user = request.auth
        return sending_code(user)
    
    
    @route.put('/atualizar_redes_sociais', response={200: UserResponse})
    def update_social_medias(self, request, social_medias: UserSocialMedias):
        user = request.auth
        user.user_twitter = social_medias.user_twitter
        user.user_youtube = social_medias.user_youtube
        user.user_twitch = social_medias.user_twitch
        user.user_instagram = social_medias.user_instagram
        user.save()
        return {"mensagem": "Redes sociais atualizadas com sucesso"}
    
    
    @route.get('/read_count', response={200: ReadCount})
    def count_read_message(self, request, user_id: int):
        user = User.objects.get(id=user_id)
        count = ChatMessage.objects.filter(user=user, read=False).count()
        return {"count": count}
    
    @route.get('/getAllPublic', response={200: list[UserOut]}, auth=None)
    def get_all_users(self, request):
        users = User.objects.all()
        serialized_users = []
        for user in users:
            user_out = UserOut(
            id=user.id,
            user_name=user.user_name,
            user_email=user.user_email,
            user_birthday=user.user_birthday,
            user_firstName=user.user_firstName,
            user_lastName=user.user_lastName,
            user_idioma=user.user_idioma,
            user_games=user.user_games,
            user_pais=user.user_pais,
            user_youtube=user.user_youtube,
            user_twitch=user.user_twitch,
            user_instagram=user.user_instagram,
            user_twitter=user.user_twitter,
            is_confirmed=user.is_confirmed,
            tipo=user.tipo,
            )
            
            if user.user_image:
                user_out.user_image = user.user_image.url
            if user.user_banner:
                user_out.user_banner = user.user_banner.url
            serialized_users.append(user_out)
        return serialized_users