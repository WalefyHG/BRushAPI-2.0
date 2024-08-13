from typing import Any, List, Optional
from datetime import date, datetime
from ninja import Schema
from pydantic import BaseModel, ConfigDict, validator
import pydantic.dataclasses


class UserIn(Schema):
    user_name: str
    user_email: str
    password: str
    user_birthday: date = None
    user_lastName: str = None
    user_firstName: str = None
    user_idioma: str = None
    user_games: str = None
    user_pais: str = None
    user_image: Optional[str] = None
    tipo: str = None
    
class UserOut(Schema):
    id: int = None
    user_name: str = None
    user_email: str = None
    user_birthday: date = None
    user_firstName: str = None
    user_lastName: str = None
    user_image: Optional[str] = None
    user_idioma: str = None
    user_games: str = None
    user_pais: str = None
    user_banner: Optional[str] = None
    user_youtube : str = None
    user_twitch : str = None
    user_instagram : str = None
    user_twitter : str = None
    is_confirmed: bool = None
    tipo: str = None

class UserResponse(Schema):
    mensagem: str
    

class UserSocialMedias(Schema):
    user_twitter: str = None
    user_youtube : str = None
    user_twitch : str = None
    user_instagram : str = None
    
class UserLogin(Schema):
    user_email: str
    user_password: str
    
class UserPut(Schema):
    user_name: Optional[str] = ''
    user_email: Optional[str] = ''
    user_birthday: date = None
    user_idioma: Optional[str] = ''
    user_games: Optional[str] = ''
    user_pais: Optional[str] = ''


class UserChangePassword(Schema):
    senha_atual: str
    senha_nova: str
    confirmar_senha: str

class TeamIn(Schema):
    team_name: str
    
class TeamOut(Schema):
    team_name: str
    team_member: List[UserOut] = None

class TeamResponse(Schema):
    mensagem: str
    

class TeamAssing(Schema):
    user_id: List[int]
    team_id: int


class NoticeIn(Schema):
    notice_title: str
    notice_content: str
    notice_date: datetime = None

class NoticeOut(Schema):
    notice_id: int
    notice_title: str
    notice_content: str
    notice_date: datetime = None
    notice_image: Optional[str] = None
    notice_writer: UserOut = None
    
    
class LoginResponse(Schema):
    mensagem: str
    access: Optional[str] = None
    refresh: Optional[str] = None
    code: Optional[str] = None
    
    
class ChatMessageIn(Schema):
    recipient_id: int
    content: str

class ChatMessageResponse(Schema):
    id: int
    content: str
    sender: UserOut
    room: str
    timestamp: datetime
    
class ChatRoomOut(Schema):
    id: int
    users: List[int]
    messages: List[ChatMessageResponse]
    
    
class ReadCount(Schema):
    count: int