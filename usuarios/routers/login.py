from ninja_extra import route, api_controller
from ninja_jwt.tokens import AccessToken, RefreshToken
from utils.sending_code import sending_code
from .. import schemas, models
from ninja_jwt.schema import TokenObtainPairInputSchema, TokenObtainPairOutputSchema
from ninja_jwt.controller import TokenObtainPairController
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
from utils.sending_password import sending_password_reset_code

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
                return schemas.UserResponse(mensagem="Senha incorreta")
            
        except models.User.DoesNotExist:
            return schemas.UserResponse(mensagem="Usuário não encontrado")
        
    @route.post('/password-reset-request', auth=None)
    def password_reset_request(self, user_email: str):
        try:
            user = models.User.objects.get(user_email=user_email)

            reset_code_response = sending_password_reset_code(user)

            if "code" in reset_code_response:
                return {"mensagem": "Um código de redefinição de senha foi enviado para o seu e-mail."}
            else:
                return {"mensagem": "Erro ao enviar o código de redefinição de senha."}, 500
        
        except models.User.DoesNotExist:
            return {"mensagem": "Usuário com este e-mail não foi encontrado"}, 404

    @route.post('/reset-password', auth=None)
    def reset_password(self, user_email: str, code: str, new_password: str):
        try:
            user = models.User.objects.get(user_email=user_email)
            user_code = models.UserCode.objects.filter(user_id=user, verification_code=code).first()

            if not user_code or user_code.verification_code_expires < datetime.now(timezone.utc):
                return {"mensagem": "Código inválido ou expirado"}, 400

            user.password = make_password(new_password)
            user_code.delete()
            user.save()

            return {"mensagem": "Senha redefinida com sucesso."}
        
        except models.User.DoesNotExist:
            return {"mensagem": "Usuário não encontrado"}, 404
        except Exception as e:
            return {"mensagem": f"Erro ao redefinir a senha: {str(e)}"}, 400