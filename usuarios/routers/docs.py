
from ninja_extra import route, api_controller
from ninja_jwt.authentication import JWTAuth
from main.permissions import AdminAcess



@api_controller(
    "users/",
    auth=JWTAuth(),
    tags=["Docs - Private"],
)

class DocsPrivateContoller:
    @route.get('/docs', permissions=[AdminAcess])
    def docs(self, request):
        return request.auth
       