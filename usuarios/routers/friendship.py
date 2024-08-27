from ninja_extra import route, api_controller
from django.shortcuts import get_object_or_404
from ..schemas import UserOut, UserResponse
from ..models import User, FriendShip
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError

@api_controller(
    "/friendship",
    tags=["Friendship"],
    auth=JWTAuth()
)

class FriendshipController:
    @route.post("/send_request", response={200: UserResponse})
    def send_request(self, request, user_id: int):
        user = request.auth
        friend = get_object_or_404(User, id=user_id)
        
        if FriendShip.objects.filter(user=user, friend=friend).exists():
            raise HttpError(400, "Solicitação de amizade já enviada.")
        
        if user == friend:
            raise HttpError(400, "Você não pode enviar solicitação de amizade para si mesmo.")
        
        
        
        friendship = FriendShip.objects.create(user=user, friend=friend)
        
        return {"mensagem": "Solicitação de amizade enviada com sucesso."}

    @route.post("/accept_request", response={200: UserResponse})
    def accept_request(self, request, friendship_id: int):
        friendship = get_object_or_404(FriendShip, id=friendship_id)
        if friendship.friend != request.auth:
            raise HttpError(403, "Você não tem permissão para aceitar esta solicitação.")
        
        friendship.accepted = True
        friendship.save()
        return {"mensagem": "Solicitação de amizade aceita."}

    @route.post("/reject_request", response={200: UserResponse})
    def reject_request(self, request, friendship_id: int):
        friendship = get_object_or_404(FriendShip, id=friendship_id)
        
        if friendship.friend != request.auth:
            raise HttpError(403, "Você não tem permissão para rejeitar esta solicitação.")
        
        friendship.delete()
        return {"mensagem": "Solicitação de amizade rejeitada."}

    @route.get("/list", response={200: list[UserOut]})
    def list(self, request):
        user = request.auth
        friendships = FriendShip.objects.filter(friend=user, accepted=True)
        friends = [friendship.user for friendship in friendships]
        return friends