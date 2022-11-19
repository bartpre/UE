import io
import PIL
import secrets
from fastapi import FastAPI, Path, File,Depends,HTTPException,status
from PIL import Image
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import datetime



app = FastAPI()
security=HTTPBasic()

@app.get("/")
def home():
    return {"Data": "Testing"}

#CZESC 1

@app.get("/prime/{number}")
def get_number(
    number:int = Path(title="Wprowadz liczbe naturalna", ge=2, le=9223372036854775807, description="Liczba musi byc naturalna!")):
    if number==2:
        return "JEST TO LICZBA PIERWSZA"
    for i in range(2,number):
        if(number%i==0):
            return number,"NIE JEST TO LICZBA PIERWSZA"
            
        else:
           return number,"JEST TO LICZBA PIERWSZA"

#CZESC 2
@app.post("/picture/invert")
def create_file(file: bytes = File(...)):
    image = Image.open(io.BytesIO(file))
    image=PIL.ImageOps.invert(image)
    inverted = io.BytesIO()
    image.save(inverted, "JPEG")
    inverted.seek(0)
    return StreamingResponse(inverted, media_type="image/jpeg")
   
#CZESC 3

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"login"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"haslo"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="zly login/haslo",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    date1 = datetime.datetime.now()
    date1 = date1.strftime("%d/%m/%Y, %H:%M:%S")
    return date1   