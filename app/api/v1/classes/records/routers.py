from fastapi import APIRouter, Depends,status
import app.api.v1.classes.records.service as service
from app.api.v1.database.database import get_db
from sqlalchemy.orm import Session
from app.api.v1.auth.authentication import oauth2_scheme
from .schemas import RecordInfo, RecordAdd
from app.api.v1.auth.authentication import verify_admin_access


record_router = APIRouter()

@record_router.get('/all/', response_model=list[RecordInfo], status_code=status.HTTP_200_OK,dependencies=[Depends(verify_admin_access)])
async def get_all_records(db: Session = Depends(get_db)):
    '''Ruta exclusiva para el administrador'''
    return service.get_all_records(db)


@record_router.get('/', response_model=list[RecordInfo], status_code=status.HTTP_200_OK)
async def get_my_records(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    return service.get_my_records(token, db)


@record_router.post('/', response_model=RecordInfo, status_code=status.HTTP_200_OK)
async def add_record(record: RecordAdd, token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    #Finalizar servicio.
    return service.add_record(record, token, db)

#Para mi deberia de retornarse Books_Returned_Info (Crear). 
@record_router.delete('/delete/{id}', response_model=RecordInfo, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin_access)])
def function(id: int, db:Session = Depends(get_db)):
    # El id es id_book_unit (Solo un libro puede ser reservado a la vez.)
    # Se busca en Records.
    
    pass