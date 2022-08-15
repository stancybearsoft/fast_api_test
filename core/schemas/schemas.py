from pydantic import BaseModel, constr


class ModelsCreate(BaseModel):
    name: str


class ManufacturerCreate(BaseModel):
    name: str


class VinCodeCreate(BaseModel):
    name: constr(max_length=17, min_length=17)
    manufacturer: int
    model: int


class VinCodeResponse(BaseModel):
    id: int
    manufacturer_id: int
    model_id: int
