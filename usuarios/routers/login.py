from ninja_extra import route, api_controller
from ninja_jwt.tokens import AccessToken, RefreshToken
from utils.sending_code import sending_code
from .. import schemas, models
from ninja_jwt.schema import TokenObtainPairInputSchema, TokenObtainPairOutputSchema
from ninja_jwt.controller import TokenObtainPairController
from django.contrib.auth.hashers import check_password

@api_controller(
    "login/",
    auth=None,
    permissions=[],
    tags=['Login - Publico']
)

class LoginController(TokenObtainPairController):
    @route.post('/login', auth=None, response=schemas.LoginResponse)
    def obtain_token(self, user_input: TokenObtainPairInputSchema):
        try:
            user = models.User.objects.get(user_email=user_input.user_email)
            
            if check_password(user_input.password, user.password):
                if user.is_confirmed:
                    access_token = AccessToken.for_user(user)
                    refresh_token = RefreshToken.for_user(user)
                    return schemas.LoginResponse(access=str(access_token), refresh=str(refresh_token), mensagem="Logado com sucesso")
                else:
                    verification_code = sending_code(user)
                    token = AccessToken.for_user(user)
                    return schemas.LoginResponse(mensagem="Usuário não confirmado", code=verification_code["code"], access=str(token))
            else:
                return {"mensagem": "Senha incorreta"}
            
        except models.User.DoesNotExist:
            return {"mensagem": "Usuário não encontrado"}