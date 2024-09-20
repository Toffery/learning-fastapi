from fastapi import APIRouter, Body
from repositories.hotels import HotelRepository
from src.hotels.schemas import HotelCreate, HotelPUT, HotelUpdate
from src.hotels.dependencies import PaginatorDep
from src.hotels.models import Hotel

from sqlalchemy import func, insert, select, update, delete
from database import async_session_maker


hotels = [
    {"id": 1, "title": "Sochi", "description": "Hotel in sochi"},
    {"id": 2, "title": "Moscow", "description": "Hotel in moscow"},
    {"id": 3, "title": "Berlin", "description": "Hotel in berlin"},
    {"id": 4, "title": "London", "description": "Hotel in london"},
    {"id": 5, "title": "Paris", "description": "Hotel in paris"},
    {"id": 6, "title": "Rome", "description": "Hotel in rome"},
    {"id": 7, "title": "New York", "description": "Hotel in new york"},
    {"id": 8, "title": "Tokyo", "description": "Hotel in tokyo"},
    {"id": 9, "title": "Sydney", "description": "Hotel in sydney"},
    {"id": 10, "title": "Amsterdam", "description": "Hotel in amsterdam"},
    {"id": 11, "title": "Amman", "description": "Hotel in amman"},
]

router = APIRouter(prefix="/hotels")


@router.get(
    "/", 

    summary="Получить все отели"
)
async def get_hotels(
    paginator: PaginatorDep,
    location: str | None = None,
    title: str | None = None
):
    """
    Ручка для получения всех отелей 
    с пагинацией и фильтрацией по полям `title` и `location`.

    Фильтрация не чувствительна к регистру.
    """
    # start = (paginator.page - 1) * paginator.per_page
    # end = paginator.per_page
    
    # async with async_session_maker() as session:
    #     async with session.begin():
    #         query = select(Hotel)
    #         if location:
    #             location = location.strip().lower()
    #             query = query.filter(func.lower(Hotel.location).contains(location))
    #         if title:
    #             title = title.strip().lower()
    #             query = query.filter(func.lower(Hotel.title).contains(title))
    #         query = (
    #             query
    #             .offset(start)
    #             .limit(end)
    #         )
    #         result = await session.execute(query)
    # hotels = result.scalars().all()
    
    # return hotels
    async with async_session_maker() as session:
        return await HotelRepository(session=session).get_all()

@router.post(
    "/",
    summary="Создать отель",
    description="Создание нового отеля.",
)
async def create_hotel(
    hotel: HotelCreate = Body(
        openapi_examples={
            "1": {
                "summary": "Абстрактный отель",
                "value": {
                    "title": "New Hotel",
                    "location": "Abstract Hotel location",
                }
            },
            "2": {
                "summary": "Лучший отель",
                "value": {
                    "title": "The best Hotel",
                    "location": "Yoshkar-Ola, Panfilova st. 1",
                }
            },
        }
    )
):
    async with async_session_maker() as session:
        async with session.begin():
            add_hotel_stmt = insert(Hotel).values(**hotel.model_dump())
            await session.execute(add_hotel_stmt)
            
    return {"message": "Hotel added"}

@router.put(
    "/",
    summary="Обновить отель",
    description="Обновление существующего отеля.",
)
async def update_hotel(
    hotel_data: HotelUpdate,
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_data.id][0]
    hotel["title"] = hotel_data.title
    hotel["description"] = hotel_data.description
    print(hotels)
    return hotel

@router.patch(
    "/{hotel_id}",
    summary="Обновить отдельную информацию об отеле",
    description="Обновление существующего отеля. \
        Возможно как обновить какие-либо поля по отдельности, так и полностью, \
        но для полного обновления лучше воспользоваться ручкой с методом PUT 'Обновить отель'."
)
async def patch_hotel(
    hotel_id: int, 
    hotel_data: HotelPUT
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.location:
        hotel["description"] = hotel_data.location
    print(hotels)
    return hotel

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель",
    description="Удаление существующего отеля по его id."
)
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Hotel deleted"}
