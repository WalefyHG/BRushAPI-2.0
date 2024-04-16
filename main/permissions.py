from .user_permission import BaseAcess

class AdminAcess(BaseAcess):
    ROLE_USER = 'admin'
    
class AtletaAcess(BaseAcess):
    ROLE_USER = 'atleta'
    
class TeamAcess(BaseAcess):
    ROLE_USER = 'team'