from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
from uuid import UUID
from datetime import date
from app.api.v1.utils.enums import Role
from typing_extensions import Self
from .models import User

class UserRegister (BaseModel):
    '''
    Modelo para registro de usuario.
    El usuario es el email.
    '''
    # id_users: UUID = UUID() No, ya que no lo ingresa el usuario.
    name: str
    lastname: str
    email: EmailStr
    password: str 
    verify_password: str
    birthdate: date

    #Estos modelos no se colocan ya que no quiero que el usuario los ingrese. 
    #Los agrego en otro modelo y sqlalchemy eventualmente.

    # verified_email: bool = False
    # role: Role = Role.USER
    # warning_amount: int = 0
    # ban: bool = False
    # rented_boooks = 0

    @model_validator(mode='after')
    def verify_passwords(self)-> Self:
        if self.password == self.verify_password:
            return self 
        else:
            raise ValueError('passwords do not match')

    @field_validator('password')
    def check_password_length(cls, v):
        if len(v) < 8:
            raise ValueError("passwords must have at least 8 characters.")
        return v

class UserInfo(BaseModel):
    '''
    
    Modelo que asemeja a ORM y es devuelto al frontend
    para que el usuario visualice sus datos en perfil.
    
    '''
    #Luego quitar id_user al retornar informacion ya que se filtra por el mismo en la bdd.
    id_user: UUID
    name: str
    lastname: str
    email: EmailStr
    birthdate: date
    user_role: Role
    #Agregar cuando cree entidad libros:
    
    #Cantidad de libros que posee?
    #rented_books : int

    #Lista de los libros que posee
    #books_rented (?): list[Books]
    warning_amounts: int
    ban: bool

    @classmethod
    def from_orm(cls, user:User):
        return cls(id_user = UUID(bytes=user.id_user))

    class Config:
        orm_mode:True
    
class UserChangeProfileData(BaseModel):
    '''
    Establece el modelo para el cambio de datos
    en el perfil de usuario.
    (Los datos cambiables, como por ejemplo, dia de nacimiento.)

    Cambio de contraseña hacer aparte.
    '''
    name: str
    lastname: str
    password:str
    email: EmailStr
    birthdate: date

class PasswordChange(BaseModel):
    '''
    Permite el cambio de contraseña
    '''
    
    old_password: str
    new_password:str
    verify_new_password:str


    @model_validator(mode='after')
    def verify_passwords(self)-> Self:
        if self.new_password == self.verify_new_password:
            return self 
        else:
            raise ValueError('passwords do not match')

    @field_validator('new_password')
    def check_password_length(cls, v):
        if len(v) < 8:
            raise ValueError("passwords must have at least 8 characters.")
        return v

