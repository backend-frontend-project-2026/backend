from app.models.base import BaseModel


class NeighbourhoodModel(BaseModel, table=True):
    __tablename__ = 'neighbourhoods'

    city: str
    district_name: str
