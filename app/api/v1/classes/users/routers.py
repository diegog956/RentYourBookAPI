from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from .schemas import UserRegister, UserInfo, UserChangeProfileData
from uuid import UUID
import app.api.v1.classes.users.service as service
from sqlalchemy.orm import Session
from app.api.v1.database.database import get_db
from app.api.v1.auth.authentication import oauth2_scheme, get_id, verify_admin_access


user_router = APIRouter()


#<----------- GET ----------->#

# '[GET] Retorna la Home que prueba el enrutamiento (?)'
# @user_router.get('/', status_code=status.HTTP_200_OK)
# async def home_user():
#     return 'Users'

'[GET] Devuelve la informacion del usuario por su id' #PROTEGER
@user_router.get('/', response_model=UserInfo ,status_code=status.HTTP_200_OK)
async def get_one_user(token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)):
    current_id: UUID = get_id(token)
    return service.get_user_info(current_id, db)
   

'''Tener cuidado con rutas como '/all' ya que toma como que 'all' es un id! '''
'[GET] Devuelve todos los usuarios para listado en seccion admin'
@user_router.get('/all/', response_model=list[UserInfo], status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin_access)])
async def get_all_users(db:Session=Depends(get_db)):

    '''La propiedad de ver la info de todos los usuarios es del administrador.
        Verifico si el scope en su token asi lo indica.
    '''
    return service.get_all_users(db)
#<----------- POST ----------->#

'[POST] Envia a la base de datos la informacion del usuario a crear' 
@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_model= UserInfo)
async def register(user_register: UserRegister, db: Session = Depends(get_db)):
    
    try:
        return service.register_user(user_register,db)
    
    except ValueError as e:
        #Es siempre raise http exception, no return!
        if 'password' in str(e):
            raise HTTPException(detail= str(e), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)

#<----------- PATCH ----------->#
    
'[PATCH] Desbanea usuario a partir del id'
@user_router.patch('/unban/{id}', response_model=str, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin_access)]) #PROTEGER
async def unban(id: UUID, db: Session = Depends(get_db)):
    try:
        return service.unban(id, db)
    except ValueError as e: 
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)

#<---------- PUT ------------->#

'[PUT] Cambia informacion del usuario a partir de id y contraseña'
@user_router.put('/modify', response_model=UserInfo, status_code=status.HTTP_202_ACCEPTED)
async def modify(user: UserChangeProfileData, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        current_id: UUID = get_id(token)
        return service.modify(current_id, user, db)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise HTTPException(detail=str(e))
    
#<---------- PATCH ------------->#

@user_router.patch('/password', status_code=status.HTTP_200_OK)
async def change_password(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):

    'Se debe de crear un modelo de pydantic con la contrseña. Parametros de query pueden ser vistos por otros.'
    service.change_password() #Realizar implementacion.
    pass