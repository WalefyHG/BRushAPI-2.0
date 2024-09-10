from ninja_extra import route, api_controller
from django.shortcuts import get_object_or_404
from ..schemas import UserOut, UserResponse, UserOutFriend
from ..models import User, FriendShip
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from django.db.models import Q

@api_controller(
    "/friendship",
    tags=["Friendship"],
    auth=JWTAuth()
)

class FriendshipController:
    @route.post("/send_request/{user_id}", response={200: UserResponse})
    def send_request(self, request, user_id: int):
        user = request.auth
        friend = get_object_or_404(User, id=user_id)
        
        if FriendShip.objects.filter(user=user, friend=friend).exists():
            raise HttpError(400, "Solicitação de amizade já enviada.")
        
        if user == friend:
            raise HttpError(401, "Você não pode enviar solicitação de amizade para si mesmo.")
        
        friendship = FriendShip.objects.create(user=user, friend=friend)
        
        friendship.friendship_status = 'pending'
        friendship.save()
        
        return {"mensagem": "Solicitação de amizade enviada com sucesso."}

    @route.post("/accept_request/{friendship_id}", response={200: UserResponse})
    def accept_request(self, request, friendship_id: int):
        friendship = get_object_or_404(FriendShip, id=friendship_id)
        
        if friendship.friend != request.auth:
            raise HttpError(403, "Você não tem permissão para aceitar esta solicitação.")
        
        friendship.friendship_status = 'accepted'
        friendship.save()
        
        return {"mensagem": "Solicitação de amizade aceita."}

    @route.post("/reject_request/{friendship_id}", response={200: UserResponse})
    def reject_request(self, request, friendship_id: int):
        friendship = get_object_or_404(FriendShip, id=friendship_id)
        
        if friendship.friend != request.auth:
            raise HttpError(403, "Você não tem permissão para rejeitar esta solicitação.")
        
        friendship.friendship_status = 'rejected'
        if friendship.friendship_status == 'rejected':
            friendship.delete()
        else:
            raise HttpError(400, "Erro ao rejeitar solicitação de amizade.")
        
        return {"mensagem": "Solicitação de amizade rejeitada."}

    @route.get("/accepted_friends", response={200: list[UserOutFriend]})
    def listando(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(
            (Q(user=user) | Q(friend=user)) & Q(friendship_status='accepted')
        )
        
        friends_with_ids = []
        for friendship in friendships:
            friend = friendship.friend if friendship.user == user else friendship.user
            
            friend_data = {
                "id": friend.id,
                "user_name": friend.user_name,
                "user_email": friend.user_email,
                "user_birthday": friend.user_birthday,
                "user_firstName": friend.user_firstName,
                "user_lastName": friend.user_lastName,
                "user_idioma": friend.user_idioma,
                "user_games": friend.user_games,
                "user_pais": friend.user_pais,
                "user_youtube": friend.user_youtube,
                "user_twitch": friend.user_twitch,
                "user_instagram": friend.user_instagram,
                "user_twitter": friend.user_twitter,
                "user_image": friend.user_image.url if friend.user_image else None,
                "user_banner": friend.user_banner.url if friend.user_banner else None,
                "tipo": friend.tipo,
                "is_confirmed": friend.is_confirmed,
                "id_friend": friendship.id,
            }
            
            friends_with_ids.append(friend_data)
            
        return friends_with_ids

    @route.get("/pending_requests", response={200: list[UserOutFriend]})
    def pending_requests(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(
            (Q(user=user) | Q(friend=user)) & Q(friendship_status='pending')
        )
        
        friends_with_ids = []
        for friendship in friendships:
            friend = friendship.friend if friendship.user == user else friendship.user
            
            friend_data = {
                "id": friend.id,
                "user_name": friend.user_name,
                "user_email": friend.user_email,
                "user_birthday": friend.user_birthday,
                "user_firstName": friend.user_firstName,
                "user_lastName": friend.user_lastName,
                "user_idioma": friend.user_idioma,
                "user_games": friend.user_games,
                "user_pais": friend.user_pais,
                "user_youtube": friend.user_youtube,
                "user_twitch": friend.user_twitch,
                "user_instagram": friend.user_instagram,
                "user_twitter": friend.user_twitter,
                "user_image": friend.user_image.url if friend.user_image else None,
                "user_banner": friend.user_banner.url if friend.user_banner else None,
                "tipo": friend.tipo,
                "is_confirmed": friend.is_confirmed,
                "id_friend": friendship.id,
                "is_sender": friendship.user == user,
            }
            
            friends_with_ids.append(friend_data)
            
        return friends_with_ids

    @route.delete("/delete_friendship", response={200: UserResponse})
    def delete_account_friend(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(Q(user=user) | Q(friend=user) | Q(friendship_status='accepted'))
        friendships.delete()
        
        return {"mensagem": "Amizades deletadas com sucesso."}