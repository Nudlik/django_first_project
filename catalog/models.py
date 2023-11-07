from dataclasses import dataclass

from django.db import models

# Create your models here.


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    description: list
    price: float
