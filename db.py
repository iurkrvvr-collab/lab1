from contextlib import contextmanager
from typing import Iterator
from abc import ABC, abstractmethod
import csv

from models import Cat

class CatDatabase(ABC):
    @abstractmethod
    def get_all(self) -> list[Cat]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Cat | None:
        pass


class ListCatDatabase(CatDatabase): 
    def __init__(self, cats: list[Cat]):
        self._cats = cats
        
    def get_all(self) -> list[Cat]:
        return self._cats
        
    def get_by_id(self, id: int) -> Cat | None: 
        for cat in self._cats: 
            if cat.id == id: 
                return cat
        return None
    

class CsvCatDatabase(CatDatabase):
    def __init__(self, file_path: str = "cats.csv"):
       self._path = file_path

    @staticmethod
    def _row_to_cat(row: dict) -> Cat:
        return Cat( 
            id=int(row["ID"]),       # Великі літери
            name=row["Name"],        # Великі літери
            photo=row["Photo"],      # Великі літери
            age=int(row["Age"])      # Великі літери
        )
    
    @contextmanager
    def _create_reader(self) -> Iterator[csv.DictReader]:
        with open(self._path, newline='', encoding="utf-8-sig") as csvfile:
            yield csv.DictReader(csvfile, delimiter=";")

    def get_all(self) -> list[Cat]:
        cats = []
        with self._create_reader() as reader:
            for row in reader:
                cats.append(self._row_to_cat(row))
        return cats

    def get_by_id(self, id: int) -> Cat | None:
        with self._create_reader() as reader:
            for row in reader:
                if int(row["ID"]) == id:  # ТУТ ТЕЖ ВЕЛИКІ ЛІТЕРИ!
                    return self._row_to_cat(row)
        return None

            
def load_database() -> CatDatabase:
    return CsvCatDatabase()