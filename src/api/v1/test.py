from fastapi import APIRouter
from typing import Any, Dict


router: APIRouter = APIRouter()

@router.get('/test')
async def test_handler() -> Dict[str, Any]:
    return {'message': 'Test'}