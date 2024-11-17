from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from business import Encoder, Analyzer


class CompressRequest(BaseModel):
    raw_str: str


class DecompressRequest(BaseModel):
    compressed_str: str


class AnalyzeRequest(BaseModel):
    compressed_str: Optional[str] = None
    raw_str: Optional[str] = None


app = FastAPI()


@app.get("/")
async def healthcheck():
    return {"message": "App is running"}


@app.post("/compress")
async def compress(request: CompressRequest):
    raw_str = request.raw_str
    encoder = Encoder()
    return {"raw_string": raw_str, "compressed_string": encoder.encode(raw_str)}


@app.post("/decompress")
async def decompress(request: DecompressRequest):
    compressed_str = request.compressed_str
    encoder = Encoder()
    return {
        "compressed_string": compressed_str,
        "raw_string": encoder.decode(compressed_str),
    }


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    analyzer = Analyzer()
    if request.compressed_str:
        encoder = Encoder()
        raw_str = encoder.decode(request.compressed_str)
        most_freq_substrs, frequency = analyzer.get_most_freq_substrs(raw_str)
        return {
            "raw_string": raw_str,
            "compressed_string": request.compressed_str,
            "analysis": {
                "most_frequent_patterns": most_freq_substrs,
                "frequency": frequency,
            },
        }
    most_freq_substrs, frequency = analyzer.get_most_freq_substrs(request.raw_str)
    return {
        "raw_string": request.raw_str,
        "analysis": {
            "most_frequent_patterns": most_freq_substrs,
            "frequency": frequency,
        },
    }
