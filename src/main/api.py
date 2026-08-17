from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File

from parser import Parser

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {"message" : "index"}
    return templates.TemplateResponse(request=request, context=context, name="index.html", status_code=200)


@app.post("/process_memory_dump")
async def upload(memory_dump: UploadFile = File(...)):
    # Process file
    print("DEBUG: ENTRY")
    chunk_size = 8000000000
    passes = 0

    if memory_dump.size:
        passes = memory_dump.size // chunk_size

    parser = Parser(chunk_size, cache_dir="src/main/cache")

    print("Parser made")

    for i in range(1, passes, 1):
        parser.read_chunk_from_bytes(i, memory_dump)
    
    return {"file_name" : memory_dump.filename}