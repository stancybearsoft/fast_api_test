from fastapi import APIRouter, Path, HTTPException

from core.models.repositories import vin_code_repo
from core.schemas.schemas import VinCodeResponse


router = APIRouter(prefix="/vehicle")


@router.get("/get/{vin_code}", response_model=VinCodeResponse)
async def get_vin_code_info(vin_code: str = Path(default="4Y1SL65848Z411439",
                                                 description="4Y1SL65848Z411439",
                                                 min_length=17, max_length=17)):
    """
    returns information about vehicle by vin code
    """

    result = await vin_code_repo.get_vin_code_info(vin_code=vin_code)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
