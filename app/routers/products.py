from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Request, Query

from app.database.session import get_db
from app.utils.token import get_current_user
from app.services.product_service import ProductService
from app.utils.image_utils import generate_mock_image_url
from app.responses.product_responses import for_create, for_get
from app.schemas.product import ProductCreate, ProductFilter, ProductUpdate


router = APIRouter(prefix="/products", tags=['Products'])

@router.get("/", responses=for_get)
async def get_all_products(
        filters: ProductFilter = Query(...),
        db: AsyncSession = Depends(get_db)):
  try:
    products = await ProductService.get_all_products(db, filters)
    if not products:
      return {"message": "Products not found"}
    return {"products": products}
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/", responses=for_create, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_data: ProductCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)):
  try:
    if not product_data.image_url:
      product_data.image_url = generate_mock_image_url()
    new_product = await ProductService.create_product(db, product_data, current_user)
    return new_product
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/{product_id}")
async def get_product(
        request: Request,
        product_id: int,
        db: AsyncSession = Depends(get_db)):
  try:
    product = await ProductService.get_product_by_id(request, db, product_id)
    return product
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.put("/{product_id}")
async def update_product(
        request: Request,
        product_id: int,
        product_data: ProductUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)):
  try:
    updated_product = await ProductService.update_product(request, db, product_id, product_data, current_user)
    return updated_product
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{product_id}")
async def delete_product(
        request: Request,
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)):
  try:
    deleted_product = await ProductService.delete_product(request, db, product_id, current_user)
    return deleted_product
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)