import pytest
from rest_framework.test import APIClient
from usuarios.models import User, UserCode, FriendShip, Notices
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.test.client import encode_multipart
import requests
from PIL import Image
import io
import logging
from django.contrib.auth.hashers import make_password
import urllib

#Criando Usuario
@pytest.mark.django_db
def test_criando_usuario():
    client = APIClient()
    url = '/users/criando'
    
    # Criar arquivos de exemplo
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
   
    
    # Dados do usuário como um único dicionário
    dados = {
    "user": {
        "user_email": "teste@gmail.com",
        "user_firstName": "Teste",
        "user_lastName": "Teste",
        "password": "teste123",
        "user_idioma": "pt-br",
        "user_games": "lol",
        "user_pais": "Brasil",
        "tipo": "admin",
        "is_confirmed": True,
        "user_name": "teste",
        "user_birthday": "2021-09-01",
    }
    }
    


    response = client.post(url, {'user': json.dumps(dados['user']), 'image': imagem}, format='multipart')
    assert response.status_code == 200 
    assert response.json() == {"mensagem": "Usuário criado com sucesso"}

# Login no sistema
@pytest.mark.django_db
def test_login_sistema():
    client = APIClient()
    url = '/login/login'
    
    dados = {
        "user_email": "teste@gmail.com",
        "password": "teste123"
    }

    response = client.post(url, dados, format='json')
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Usuário e/ou senha incorreto(s)'
    

@pytest.mark.django_db
def test_login_sistema_valido():
    client = APIClient()
    url = '/login/login'
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    dados = {
        "user_email": "teste@gmail.com",
        "password": "teste123"
    }
    
    response = client.post(url, dados, format='json')
    assert response.status_code == 200
    assert 'access' in response.json()
    assert 'refresh' in response.json()
    assert 'mensagem' in response.json()
    assert response.json()['mensagem'] == 'Logado com sucesso'
    
@pytest.mark.django_db
def test_password_reset_request():
    # Teste de envio de código de redefinição de senha que dá status 200
    client = APIClient()
    url = '/login/password-reset-request'
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    response = client.post(f'{url}?user_email={user.user_email}')
    assert response.status_code == 200
    assert 'mensagem' in response.json()
    assert response.json()['mensagem'] == 'Um código de redefinição de senha foi enviado para o seu e-mail.'  
    

# Testes de Users
@pytest.mark.django_db
def test_perfil_usuario():
    
    client = APIClient()
    url = '/users/perfil'
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    ) 

    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    assert login_response.status_code == 200
    assert 'access' in login_response.json()

    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(url)
    assert response.status_code == 200
    assert 'user_email' in response.json()
    assert response.json()['user_email'] == user.user_email
    
@pytest.mark.django_db
def test_perfil_usuario_not_authorizated():
    client = APIClient()
    url = '/users/perfil'
    
    response = client.get(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'


@pytest.mark.django_db
def test_perfil_atualizar_usuario():
    client = APIClient()
    
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    banner_content = io.BytesIO()
    banner = Image.new('RGB', (100, 100))
    banner.save(banner_content, format='JPEG')
    banner_content.seek(0)
    banner = SimpleUploadedFile("banner.jpg", banner_content.read(), content_type="image/jpeg")
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    url = f'/users/atualizar/{user.id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    dados = {
        "user": {
            "user_firstName": "Teste2",
        }
    }
    
    response = client.put(url, {'user': json.dumps(dados['user']), 'image': imagem, 'banner': banner}, format='multipart')
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_perfil_deletar_usuario():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    url = f'/users/deletar'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.delete(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_perfil_deletar_usuario_not_authorizated():
    client = APIClient()
    url = '/users/deletar'
    
    response = client.delete(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'


@pytest.mark.django_db
def test_get_usuario_by_id():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    url = f'/users/usuario/{user.id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.get(url)
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_get_usuario_by_id_not_authorizated():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    url = f'/users/usuario/{user.id}'
    
    response = client.get(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_pesquisar_by_username():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    url = f'/users/pesquisar/{user.user_name}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_atualizar_senha():
    client = APIClient()
    
    url = '/users/atualizar_senha'
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    dados = {
            "senha_atual": "teste123",
            "senha_nova": "teste1234",
            "confirmar_senha": "teste1234"
    }
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.put(url, dados, format='json')
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_atualizar_senha_not_authorizated():
    client = APIClient()
    
    url = '/users/atualizar_senha'
    
    dados = {
            "senha_atual": "teste123",
            "senha_nova": "teste1234",
            "confirmar_senha": "teste1234"
    }
    
    response = client.put(url, dados, format='json')
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_get_all_public():
    client = APIClient()
    
    url = '/users/getAllPublic'
    
    response = client.get(url)
    
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_perfil_by_username():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    url = f'/users/perfil/{friend.user_name}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_perfil_by_username_not_authorizated():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    url = f'/users/perfil/{friend.user_name}'
    
    response = client.get(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_enviar_codigo():
    client = APIClient()
    
    url = '/users/enviar_codigo'
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url)
    assert response.status_code == 200
    assert 'mensagem' in response.json()
    assert response.json()['mensagem'] == 'Código enviado com sucesso'
    
@pytest.mark.django_db
def test_enviar_codigo_not_authorizated():
    client = APIClient()
    
    url = '/users/enviar_codigo'
    
    response = client.post(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
    
@pytest.mark.django_db
def test_verificar_codigo():
    client = APIClient()
    
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    user_code = UserCode.objects.create(
        user_id=user,
        verification_code='123423'
    )
    
    url = f'/users/verificar_codigo/{user_code.verification_code}'
    
    
    response = client.post(url, format='json')
    assert response.status_code == 200

# Teste friendship
@pytest.mark.django_db
def test_enviar_pedido_amizade():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    url = f'/friendship/send_request/{friend.id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_enviar_pedido_amizade_self():
    cliente = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    url = f'/friendship/send_request/{user.id}'
    
    login_response = cliente.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = cliente.post(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Você não pode enviar solicitação de amizade para si mesmo.'
    
@pytest.mark.django_db
def test_enviar_pedido_not_authorizated():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    url = f'/friendship/send_request/{friend.id}'
    
    response = client.post(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_accept_request():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/accept_request/{friendship.id}'
    
    login_response = client.post('/login/login', {'user_email': friend.user_email, 'password': 'teste1233'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_accept_request_not_authorizated():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/accept_request/{friendship.id}'
    
    response = client.post(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_accept_self():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/accept_request/{friendship.id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url)
    assert response.status_code == 403
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Você não tem permissão para aceitar esta solicitação.'
    
@pytest.mark.django_db
def test_reject_request():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/reject_request/{friendship.id}'
    
    login_response = client.post('/login/login', {'user_email': friend.user_email, 'password': 'teste1233'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_reject_request_self():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/reject_request/{friendship.id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url)
    assert response.status_code == 403
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Você não tem permissão para rejeitar esta solicitação.'
    
@pytest.mark.django_db
def test_reject_request_not_authorizated():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/reject_request/{friendship.id}'
    
    response = client.post(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'

@pytest.mark.django_db
def test_remove_friendship():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='accepted'
    )
    
    url = f'/friendship/delete_friendship'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.delete(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_remove_friendship_not_authorizated():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='accepted'
    )
    
    url = f'/friendship/delete_friendship'
    
    response = client.delete(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_remove_friendship_self():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='accepted'
    )
    
    url = f'/friendship/delete_friendship'
    
    login_response = client.post('/login/login', {'user_email': friend.user_email, 'password': 'teste1233'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.delete(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_pending_request():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='pending'
    )
    
    url = f'/friendship/pending_requests'
    
    login_response = client.post('/login/login', {'user_email': friend.user_email, 'password': 'teste1233'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_pending_request_not_authorizated():
    client = APIClient()
    
    url = f'/friendship/pending_requests'
    
    response = client.get(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_accepts_friends():
    client = APIClient()
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    friendship = FriendShip.objects.create(
        user=user,
        friend=friend,
        friendship_status='accepted'
    )
    
    url = f'/friendship/accepted_friends'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_accepts_friends_not_authorizated():
    client = APIClient()
    
    url = f'/friendship/accepted_friends'
    
    response = client.get(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
# Teste com as Noticias

@pytest.mark.django_db
def test_criar_noticia():
    client = APIClient()
    
    url = '/notices/notices'
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    dados = {
        "notice": { 
            "notice_title": "Teste",
            "notice_content": "Teste",
            "notice_date": "2021-09-01",
        }
    }
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.post(url, {'notice': json.dumps(dados['notice']), 'image': imagem}, format='multipart')
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_criar_noticia_not_authorizated():
    client = APIClient()
    
    url = '/notices/notices'
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    dados = {
        "notice": { 
            "notice_title": "Teste",
            "notice_content": "Teste",
            "notice_date": "2021-09-01",
        }
    }
    
    response = client.post(url, {'notice': json.dumps(dados['notice']), 'image': imagem}, format='multipart')
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_get_all_notices():
    client = APIClient()
    
    url = '/notices/allnotices'
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_all_notices_not_authorizated():
    client = APIClient()
    
    url = '/notices/allnotices'
    
    response = client.get(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_delete_by_id():
    client = APIClient()
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    notice = Notices.objects.create(
        notice_title="Teste",
        notice_content="Teste",
        notice_date="2021-09-01",
        notice_image=imagem,
        notice_writer=user
    )
    
    url = f'/notices/deletando/{notice.notice_id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.delete(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_by_id_not_authorizated_friend_notice():
    client = APIClient()
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste.jpg",
        user_banner="teste.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    notice = Notices.objects.create(
        notice_title="Teste",
        notice_content="Teste",
        notice_date="2021-09-01",
        notice_image=imagem,
        notice_writer=friend
    )
    
    url = f'/notices/deletando/{notice.notice_id}'
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.delete(url)
    assert response.status_code == 403
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Você não tem permissão para deletar essa notícia'
    
@pytest.mark.django_db
def test_delete_by_id_not_authorizated():
    client = APIClient()
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    
    user = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    notice = Notices.objects.create(
        notice_title="Teste",
        notice_content="Teste",
        notice_date="2021-09-01",
        notice_image=imagem,
        notice_writer=user
    )
    
    url = f'/notices/deletando/{notice.notice_id}'
    
    response = client.delete(url)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_update_by_id():
    client = APIClient()
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    image_content2 = io.BytesIO()
    image2 = Image.new('RGB', (100, 100))
    image2.save(image_content2, format='JPEG')
    image_content2.seek(0)
    imagem2 = SimpleUploadedFile("image.jpg", image_content2.read(), content_type="image/jpeg")
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste1.jpg",
        user_banner="teste1.jpg"
    )
    
    notice = Notices.objects.create(
        notice_title="Teste",
        notice_content="Teste",
        notice_date="2021-09-01",
        notice_image=imagem,
        notice_writer=user
    )
    
    url = f'/notices/update/{notice.notice_id}'
    
    dados = {
        "notice": { 
            "notice_title": "Teste2",
            "notice_content": "Teste2",
            "notice_date": "2021-09-01",
        }
    }
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.put(url, {'notice': json.dumps(dados['notice']), 'image': imagem2}, format='multipart')
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_by_id_not_authorizated():
    client = APIClient()
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    image_content2 = io.BytesIO()
    image2 = Image.new('RGB', (100, 100))
    image2.save(image_content2, format='JPEG')
    image_content2.seek(0)
    imagem2 = SimpleUploadedFile("image.jpg", image_content2.read(), content_type="image/jpeg")
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste1.jpg",
        user_banner="teste1.jpg"
    )
    
    notice = Notices.objects.create(
        notice_title="Teste",
        notice_content="Teste",
        notice_date="2021-09-01",
        notice_image=imagem,
        notice_writer=user
    )
    
    url = f'/notices/update/{notice.notice_id}'
    
    dados = {
        "notice": { 
            "notice_title": "Teste2",
            "notice_content": "Teste2",
            "notice_date": "2021-09-01",
        }
    }
    
    response = client.put(url, {'notice': json.dumps(dados['notice']), 'image': imagem2}, format='multipart')
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    
@pytest.mark.django_db
def test_update_by_id_not_authorizated_friend_notice():
    client = APIClient()
    
    image_content = io.BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_content, format='JPEG')
    image_content.seek(0)
    imagem = SimpleUploadedFile("image.jpg", image_content.read(), content_type="image/jpeg")
    
    image_content2 = io.BytesIO()
    image2 = Image.new('RGB', (100, 100))
    image2.save(image_content2, format='JPEG')
    image_content2.seek(0)
    imagem2 = SimpleUploadedFile("image.jpg", image_content2.read(), content_type="image/jpeg")
    
    user = User.objects.create(
        user_email="teste@gmail.com",
        user_firstName="Teste",
        user_lastName="Teste",
        password=make_password("teste123"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste",
        user_birthday="2021-09-01",
        user_image="teste1.jpg",
        user_banner="teste1.jpg"
    )
    
    friend = User.objects.create(
        user_email="teste2@gmail.com",
        user_firstName="Teste2",
        user_lastName="Teste2",
        password=make_password("teste1233"),
        user_idioma="pt-br",
        user_games="lol",
        user_pais="Brasil",
        tipo="admin",
        is_confirmed=True,
        user_name="teste2",
        user_birthday="2021-09-01",
        user_image="teste2.jpg",
        user_banner="teste2.jpg"
    )
    
    notice = Notices.objects.create(
        notice_title="Teste",
        notice_content="Teste",
        notice_date="2021-09-01",
        notice_image=imagem,
        notice_writer=friend
    )
    
    url = f'/notices/update/{notice.notice_id}'
    
    dados = {
        "notice": { 
            "notice_title": "Teste2",
            "notice_content": "Teste2",
            "notice_date": "2021-09-01",
        }
    }
    
    login_response = client.post('/login/login', {'user_email': user.user_email, 'password': 'teste123'}, format='json')
    token = login_response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = client.put(url, {'notice': json.dumps(dados['notice']), 'image': imagem2}, format='multipart')
    assert response.status_code == 403
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Você não tem permissão para editar essa notícia'
