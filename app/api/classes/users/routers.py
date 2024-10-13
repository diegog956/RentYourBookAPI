from fastapi import APIRouter, status
from .schemas import UserRegister, UserInfo
from uuid import UUID
user_router = APIRouter()

#<----------- GET ----------->#

'[GET] Retorna la Home que prueba el enrutamiento (?)'
@user_router.get('/', status_code=status.HTTP_200_OK)
def home_user():
    return 'USERS.'

'[GET] Devuelve la informacion del usuario por su id'
@user_router.get('/{id}', response_model=UserInfo ,status_code=status.HTTP_200_OK)
def get_one_user(id: UUID):
    pass
    #Llamada al servicio que se dirige a la base de datos a buscar la info del usuario con el UUID correspondiente.


'[GET] Devuelve todos los usuarios para listado en seccion admin'
@user_router.get('/', response_model=list[UserInfo], status_code=status.HTTP_200_OK)
def get_all_users():
    pass

#<----------- POST ----------->#

'[POST] Envia a la base de datos la informacion del usuario a crear' 
@user_router.post('/register', status_code=status.HTTP_201_CREATED)
def register(user_register: UserRegister):
    #Llamada al servicio y.. posterior retorno de la informacion del usuario?
    return user_register.__dict__
