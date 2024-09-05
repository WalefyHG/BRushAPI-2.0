from usuarios.models import User, UserCode
import random, string, threading
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail

def sending_password_reset_code(user):
    try:
        existing_code = UserCode.objects.filter(user_id=user).first()

        if existing_code:
            code = generate_verification_code()
            existing_code.verification_code = code["code"]
            existing_code.verification_code_expires = code["verification_code_expires"]
            existing_code.save()
            user_code = existing_code
        else:
            code = generate_verification_code()
            user_code = UserCode.objects.create(
                user_id=user,
                verification_code=code["code"],
                verification_code_expires=code["verification_code_expires"]
            )
            user_code.save()

        timer = threading.Timer(600, delete_verification_code, args=[user_code.id])
        timer.start()

        subject = '🔒 Redefinição de Senha - B-Rush'
        mensagem = f'''
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f2f2f2;">
                <div style="background-color: #222; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); color: white;">
                    <h2>Olá {user.user_firstName},</h2>
                    <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
                        Recebemos uma solicitação para redefinir sua senha na Plataforma B-Rush 🚀. 
                        Use o código abaixo para concluir o processo de redefinição:
                    </p>
                    <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
                        Código de Redefinição: <strong style="font-size: 16px;line-height: 24px; color: #d407e7;">{code["code"]}</strong>
                    </p>
                    <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
                        Este código é válido por 10 minutos. Se você não solicitou esta ação, por favor, ignore este e-mail.
                    </p>
                    <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
                        Caso tenha dúvidas, entre em contato com nosso suporte respondendo a este e-mail.
                    </p>
                    <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">Atenciosamente,</p>
                    <pre style="font-size: 16px; line-height: 24px; color: #dfd7d7;">
                    Suporte B-Rush
                    brushsuporte@gmail.com
                    </pre>
                </div>
            </body>
            </html>
        '''
        from_email = 'BRushSuporte@gmail.com'
        recipient_list = [user.user_email]
        send_mail(subject, 
                  '', 
                  from_email, 
                  recipient_list, 
                  fail_silently=False, 
                  auth_user='brushsuporte@gmail.com', 
                  auth_password='bgqs qwmw iimh jxzj',
                  html_message=mensagem
                  )
        return {"mensagem": "Enviado com sucesso", "code": code["code"]}
    except User.DoesNotExist:
        return {"mensagem": "Usuário não encontrado"}

def generate_verification_code():
    code = ''.join(random.choice(string.digits) for _ in range(6))
    verification_code_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    return {"code": code, "verification_code_expires": verification_code_expires}

def delete_verification_code(user_code_id):
    try:
        user_code = UserCode.objects.get(id=user_code_id)
        user_code.delete()
    except UserCode.DoesNotExist:
        pass
    except Exception as e:
        print(f"Erro ao excluir código: {e}")