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

    @abstractmethod
    def add_cat(self, cat: Cat) -> None:
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

    def add_cat(self, cat: Cat) -> None:
        self._cats.append(cat)
    

class CsvCatDatabase(CatDatabase):
    def __init__(self, file_path: str = "cats.csv"):
        self._path = file_path

    @staticmethod
    def _row_to_cat(row: dict) -> Cat:
        return Cat( 
            id=int(row["ID"]),       
            name=row["Name"],        
            photo=row["Photo"],      
            age=int(row["Age"])      
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
                if int(row["ID"]) == id:  
                    return self._row_to_cat(row)
        return None

    def add_cat(self, cat: Cat) -> None:
        with open(self._path, mode='a', newline='', encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow([cat.id, cat.name, cat.photo, cat.age])
            

def load_database() -> CatDatabase:
    return CsvCatDatabase()