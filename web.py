import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from app.config import TOKEN_SETS, NEXTDNS_KEY
from app.services import locket, nextdns

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return FileResponse("app/static/index.html")


class ActivateRequest(BaseModel):
    username: str


@app.post("/activate")
async def activate(req: ActivateRequest):
    username = req.username.strip()

    # Strip locket.cam URL if pasted
    if "locket.cam/" in username:
        username = username.split("locket.cam/")[-1].split("?")[0]

    if not username:
        return JSONResponse({"success": False, "error": "Vui lòng nhập username hoặc email."})

    # Step 1: Resolve UID
    uid = await locket.resolve_uid(username)
    if not uid:
        return JSONResponse({
            "success": False,
            "error": "Không tìm thấy user. Kiểm tra lại username hoặc đường link Locket."
        })

    # Step 2: Inject Gold — thử lần lượt từng TOKEN_SET (giống logic worker của bot)
    import re

    logs = []

    def log_callback(msg):
        clean = re.sub(r'\033\[[0-9;]*m', '', msg)
        logs.append(clean)

    success = False
    msg_result = "Tất cả token sets đều thất bại."

    for idx, token_config in enumerate(TOKEN_SETS):
        logs.append(f"[*] Thử Token Set #{idx + 1}...")
        success, msg_result = await locket.inject_gold(uid, token_config, log_callback)
        if success:
            break
        logs.append(f"[!] Token Set #{idx + 1} thất bại: {msg_result}")

    if not success:
        return JSONResponse({
            "success": False,
            "uid": uid,
            "username": username,
            "error": msg_result,
            "logs": logs
        })

    # Step 3: Create NextDNS profile
    pid, dns_link = await nextdns.create_profile(NEXTDNS_KEY, log_callback)

    dns_hostname = f"{pid}.dns.nextdns.io" if pid else None

    return JSONResponse({
        "success": True,
        "uid": uid,
        "username": username,
        "dns_link": dns_link,
        "dns_id": pid,
        "dns_hostname": dns_hostname,
        "logs": logs
    })
