import csv
import random
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Word(BaseModel):
    No: int
    標準的な表記: str
    読み: str
    語彙の難易度: str
    品詞1: str
    品詞2_詳細: str
    語種: str


words_data = []


def load_csv():
    with open("goi.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            words_data.append(
                Word(
                    No=int(row["No"]),
                    標準的な表記=row["標準的な表記"],
                    読み=row["読み"],
                    語彙の難易度=row["語彙の難易度"],
                    品詞1=row["品詞1"],
                    品詞2_詳細=row["品詞2(詳細)"],
                    語種=row["語種"],
                )
            )


load_csv()


@app.get("/words", response_model=List[Word])
async def get_words(speech: str = Query(None), lv: int = Query(None)):
    filtered_words = words_data
    if speech:
        filtered_words = [word for word in filtered_words if word.品詞1 == speech]
    if lv is not None:
        lv_map = {
            1: "1.初級前半,2.初級後半",
            2: "3.中級前半,4.中級後半",
            3: "5.上級前半,6.上級後半",
        }
        filtered_words = [
            word for word in filtered_words if word.語彙の難易度 in lv_map[lv]
        ]
    random.shuffle(filtered_words)
    return filtered_words[:10]


@app.get("/2words", response_model=List[str])
async def get_combined_words():
    nouns = [word for word in words_data if word.品詞1 == "名詞"]
    adjectives = [word for word in words_data if word.品詞1 in ["ナ形容詞", "イ形容詞"]]

    random.shuffle(nouns)
    random.shuffle(adjectives)

    combined_words = []
    for noun, adjective in zip(nouns[:10], adjectives[:10]):
        if adjective.品詞1 == "ナ形容詞":
            combined_word = f"{adjective.標準的な表記}な{noun.標準的な表記}"
        else:
            combined_word = f"{adjective.標準的な表記}{noun.標準的な表記}"
        combined_words.append(combined_word)

    return combined_words


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
