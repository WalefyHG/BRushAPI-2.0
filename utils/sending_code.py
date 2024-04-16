from usuarios.models import User, UserCode
import random, string, threading
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail

def sending_code(user):
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
            user_code_id = user_code.id

        timer = threading.Timer(600, delete_verification_code, args=[user_code.id])  # 600 segundos = 10 minutos
        timer.start()
        
        subject = '🌟 Bem-vindo ao Nosso Site 🌟'
        mensagem = f'''
             <html>

  <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f2f2f2;">
    <div style="background-color: #222; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); color: white;">
      <h2>Olá {user.user_firstName}! 😊</h2>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Esperamos que você esteja bem. Para garantir a segurança da sua conta na
        Plataforma B-Rush 🚀, estamos implementando um processo de verificação
        adicional. Por favor, siga as instruções abaixo para concluir a
        verificação:
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">Nome de Usuário: <strong style="font-size: 16px;line-height: 24px; color: #d407e7;">{user.user_name}</strong></p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Código de Verificação: <strong style="font-size: 16px;line-height: 24px; color: #d407e7;">{code["code"]}</strong>
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Este código é válido por 10 minutos. Certifique-se de inseri-lo assim que possível para evitar
        quaisquer inconvenientes no acesso à sua conta.
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Se você não solicitou este código ou tem alguma dúvida, por favor, entre
        em contato conosco imediatamente respondendo a este e-mail. Estamos aqui
        para ajudar.
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">Agradecemos pela sua cooperação.</p>
      <pre style=" font-size: 16px; line-height: 24px; color: #dfd7d7;">
    Atenciosamente,

    Suporte
    B-Rush Suporte
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