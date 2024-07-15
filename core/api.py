from ninja_extra import NinjaExtraAPI
from usuarios.routers.docs import DocsPrivateContoller
from usuarios.routers.login import LoginController
from usuarios.routers.users import UserPublicContoller


api = NinjaExtraAPI(version='2.0.0', title='API do BRush', description='Nossa nova API')

api.register_controllers(LoginController)
api.register_controllers(UserPublicContoller)
api.register_controllers(DocsPrivateContoller)