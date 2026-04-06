# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Body
from app.models import UserRegister, UserLogin
from app.database import init_db, get_user, add_user, list_all_users
from app.auth import hash_password, verify_password, is_strong_password, create_token, verify_token

app = FastAPI()
init_db()

@app.get("/")
def home():
    return {"message": "ZenMode API en ejecucion..."}

@app.post("/register")
def register(user: UserRegister):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    if not is_strong_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="LA contraseña debe tener +8 caracteres, incluir Mayuscula, Minuscula, Numeros"
        )

    add_user(user.username, hash_password(user.password))
    return {"message": "Usuario registrado exitosamente"}

@app.post("/login")
def login(user: UserLogin):
    stored_user = get_user(user.username)
    if not stored_user or not verify_password(user.password, stored_user[1]):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")

    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

    
@app.get("/users")
def list_users():
    return {"users":list_all_users()}