from pydantic import BaseModel, constr


class Model(BaseModel):
    name: str


class Manufacture(BaseModel):
    name: str


class VinCode(BaseModel):
    name: constr(max_length=17, min_length=17)
    manufacture: Manufacture
    model: Model


class VinCodeResponse(BaseModel):
    id: int
    manufacturer_id: int
    model_id: int



