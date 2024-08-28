from ninja_extra import route, api_controller
from django.shortcuts import get_object_or_404
from ..schemas import UserOut, UserResponse, UserOutFriend
from ..models import User, FriendShip
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError

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
        
        return {"mensagem": "Solicitação de amizade enviada com sucesso."}

    @route.post("/accept_request/{friendship_id}", response={200: UserResponse})
    def accept_request(self, request, friendship_id: int):
        friendship = get_object_or_404(FriendShip, id=friendship_id)
        if friendship.friend != request.auth:
            raise HttpError(403, "Você não tem permissão para aceitar esta solicitação.")
        
        friendship.accepted = True
        friendship.save()
        return {"mensagem": "Solicitação de amizade aceita."}

    @route.post("/reject_request/{friendship_id}", response={200: UserResponse})
    def reject_request(self, request, friendship_id: int):
        friendship = get_object_or_404(FriendShip, id=friendship_id)
        
        if friendship.friend != request.auth:
            raise HttpError(403, "Você não tem permissão para rejeitar esta solicitação.")
        
        friendship.delete()
        return {"mensagem": "Solicitação de amizade rejeitada."}

    @route.get("/accepted_friends", response={200: list[UserOutFriend]})
    def listando(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(friend=user, accepted=True)
        friends_with_ids = []
        for friendship in friendships:
            friend = {
                "id": friendship.user.id,
                "user_name": friendship.user.user_name,
                "user_email": friendship.user.user_email,
                "user_birthday": friendship.user.user_birthday,
                "user_firstName": friendship.user.user_firstName,
                "user_lastName": friendship.user.user_lastName,
                "user_idioma": friendship.user.user_idioma,
                "user_games": friendship.user.user_games,
                "user_pais": friendship.user.user_pais,
                "user_youtube": friendship.user.user_youtube,
                "user_twitch": friendship.user.user_twitch,
                "user_instagram": friendship.user.user_instagram,
                "user_twitter": friendship.user.user_twitter,
                "user_image": friendship.user.user_image.url if friendship.friend.user_image else None,
                "user_banner": friendship.user.user_banner.url if friendship.friend.user_banner else None,
                "tipo": friendship.user.tipo,
                "is_confirmed": friendship.user.is_confirmed,
                "id_friend": friendship.id  
                }
            friends_with_ids.append(friend)
    
        return friends_with_ids

    @route.get("/pending_requests", response={200: list[UserOutFriend]})
    def pending_requests(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(friend=user, accepted=False)
        friends_with_ids = []
        
        for friendship in friendships:
            friend = {
                "id": friendship.user.id,
                "user_name": friendship.user.user_name,
                "user_email": friendship.user.user_email,
                "user_birthday": friendship.user.user_birthday,
                "user_firstName": friendship.user.user_firstName,
                "user_lastName": friendship.user.user_lastName,
                "user_idioma": friendship.user.user_idioma,
                "user_games": friendship.user.user_games,
                "user_pais": friendship.user.user_pais,
                "user_youtube": friendship.user.user_youtube,
                "user_twitch": friendship.user.user_twitch,
                "user_instagram": friendship.user.user_instagram,
                "user_twitter": friendship.user.user_twitter,
                "user_image": friendship.user.user_image.url if friendship.friend.user_image else None,
                "user_banner": friendship.user.user_banner.url if friendship.friend.user_banner else None,
                "tipo": friendship.user.tipo,
                "is_confirmed": friendship.user.is_confirmed,
                "id_friend": friendship.id  
                }
            friends_with_ids.append(friend)
            
        return friends_with_ids
    
    
    @route.delete("/delete_friendship", response={200: UserResponse})
    def delete_account_friend(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(friend=user)
        friendships.delete()
        return {"mensagem": "Amizades deletadas com sucesso."}