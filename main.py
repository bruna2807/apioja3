from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Banco de dados simulado
users = [
    {"id": 1, "name": "Luara", "email": "luara@gmail.com", "phone": "2010"},
    {"id": 2, "name": "Bruna", "email": "bruna@gmail.com", "phone": "2022"},
]

# Página de Login
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    if email == "luara@gmail.com" and password == "luara2010":
        return RedirectResponse(url="/docs", status_code=303)
    raise HTTPException(status_code=401, detail="Email ou senha incorretos")


# Endpoints de Usuários
@app.get("/users")
async def list_users():
    return {"users": users}


@app.post("/users")
async def create_user(name: str, email: str, phone: str):
    new_id = max(user["id"] for user in users) + 1
    new_user = {"id": new_id, "name": name, "email": email, "phone": phone}
    users.append(new_user)
    return {"message": "Usuário cadastrado com sucesso!", "user": new_user}


@app.put("/users/{user_id}")
async def update_user(user_id: int, name: str = None, email: str = None, phone: str = None):
    for user in users:
        if user["id"] == user_id:
            if name:
                user["name"] = name
            if email:
                user["email"] = email
            if phone:
                user["phone"] = phone
            return {"message": "Usuário atualizado com sucesso!", "user": user}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    global users
    users = [user for user in users if user["id"] != user_id]
    return {"message": "Usuário removido com sucesso!"}


@app.get("/users/filter")
async def filter_users(email: str = None, phone: str = None):
    filtered = [user for user in users if (email and user["email"] == email) or (phone and user["phone"] == phone)]
    if not filtered:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado com os critérios fornecidos")
    return {"users": filtered}
