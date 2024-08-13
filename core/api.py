from ninja_extra import NinjaExtraAPI
from usuarios.routers.chat import ChatController
from usuarios.routers.docs import DocsPrivateContoller
from usuarios.routers.login import LoginController
from usuarios.routers.notices import NoticesController
from usuarios.routers.users import UserPublicContoller
from ninja_jwt.authentication import JWTAuth

api = NinjaExtraAPI(version='2.0.0', title='API do BRush', description='Nossa nova API')

api.register_controllers(LoginController)
api.register_controllers(UserPublicContoller)
api.register_controllers(DocsPrivateContoller)
api.register_controllers(ChatController)
api.register_controllers(NoticesController)