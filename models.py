from pydantic import BaseModel


class Word(BaseModel):
    No: int
    標準的な表記: str
    読み: str
    語彙の難易度: str
    品詞1: str
    品詞2_詳細: str
    語種: str
