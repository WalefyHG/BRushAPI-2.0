from datetime import datetime
from ninja import File
from ninja_extra import route, api_controller
from ninja_jwt.authentication import JWTAuth
from usuarios.models import Notices
from ninja.files import UploadedFile
from usuarios.schemas import NoticeIn, NoticeOut, UserResponse
from ninja.errors import HttpError
from django.utils.dateparse import parse_date


@api_controller(
    "notices/",
    auth=JWTAuth(),
    tags=["Notícias - Publico"],
)

class NoticesController:
    @route.get('allnotices', response={200: list[NoticeOut]})
    def get_notices(self, request):
        notices = Notices.objects.all()
        serialized_notices = []
        for notice in notices:
            notice_out = NoticeOut(
                notice_id=notice.notice_id,
                notice_title=notice.notice_title,
                notice_content=notice.notice_content,
                notice_date=notice.notice_date,
                notice_image=notice.notice_image.url if notice.notice_image else None,
                notice_writer=notice.notice_writer
            )
            serialized_notices.append(notice_out)
        return serialized_notices
    
    @route.post('notices', response={200: NoticeOut})
    def create_notices(self, request, notice: NoticeIn, image: UploadedFile = File(None)):
        user = request.auth
        notice_date = notice.notice_date.date()
        
        notices = Notices.objects.create(
            notice_title=notice.notice_title,
            notice_content=notice.notice_content,
            notice_date=notice_date,
            notice_image=image,
            notice_writer=user
        )
        notices.save()
        return notices
    
    @route.delete('deletando/{id}', response={200: UserResponse})
    def delete_notice_by_id(self, request, id: int):
        try:
            user = request.auth
            notice_data = Notices.objects.get(notice_id=id)
            if user.user_name == notice_data.notice_writer.user_name:
                notice_data.delete()
                return UserResponse(mensagem="Notícia deletada com sucesso")
            else:
                raise HttpError(403, "Você não tem permissão para deletar essa notícia")
        
        except Notices.DoesNotExist:
            raise HttpError(404, "Notícia não encontrada")
        
        
    @route.put('update/{id}', response={200: NoticeOut})
    def update_notices_by_id(self, request, id: int, notice: NoticeIn, image: UploadedFile = File(None)):
        user = request.auth
        existing_notice = Notices.objects.get(notice_id=id)
        if user.user_name == existing_notice.notice_writer.user_name:
            existing_notice.notice_title = notice.notice_title
            existing_notice.notice_content = notice.notice_content
            existing_notice.notice_date = notice.notice_date
            if image is not None:
                existing_notice.notice_image = image
            existing_notice.save()
            return existing_notice
        else:
            raise HttpError(403, "Você não tem permissão para editar essa notícia")
            