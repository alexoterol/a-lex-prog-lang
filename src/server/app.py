import io
import sys
from fastapi import FastAPI
from analyzers.analizador_semantico import parser, tokens, lexer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class CodeRequest(BaseModel):
    code: str


app = FastAPI(
        title="swift analyzer"
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
)


@app.get("/")
async def root():
    return { "message": "Funciona" }


@app.post("/get_errors")
async def get_errors(request: CodeRequest):
    if request.code == "":
        return { "result" : "" }

    lexer.lineno = 1
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        parser.parse(request.code, lexer=lexer)
    finally:
        sys.stdout = old_stdout

    captured_output = buffer.getvalue()
    buffer.close()
    print("Captured:", captured_output)
    return { "result" : captured_output }
