from django.http import HttpRequest
from ninja_extra.controllers import ControllerBase
from ninja_extra.permissions import BasePermission


class BaseAcess(BasePermission):
    message = "Você não tem permissão para acessar este recurso"
    
    ROLE_USER: str
    
    def has_permission(self, request: HttpRequest, controller: ControllerBase) -> bool:
        if request.user.is_superuser:
            return True
        
        tipo = request.user.tipo
        
        if tipo == self.ROLE_USER:
            return tipo
        