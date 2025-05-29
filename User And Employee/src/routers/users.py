from fastapi import APIRouter, Depends
from models.user import UserModel
from database.schema import User
from config.database_connection import get_db_connection


user_router = APIRouter()

@user_router.post('/create-user', tags=['User'])
async def create_user(
    user: UserModel,
    conn = Depends(get_db_connection)
):
    try:
        response = await user.create_user(conn)
        return {
            "Message: ": "User Created Successfully",
            "Details": response
        }
    except BaseException as e:
        print(e)
        raise e


@user_router.get('/get-all-users', tags=['User'])
async def get_all_users(
    conn = Depends(get_db_connection)
):
    try: 
        return await UserModel.get_user_details(conn)
    except BaseException as e:
        print(e)
        raise e
    

@user_router.get('/get-user-by-name', tags=['User'])
async def get_user_by_name(
    name: str,
    db = Depends(get_db_connection)
):
    try:
        user = await UserModel.get_user_by_name(name, db)
        return user
    except BaseException as e:
        print(e)
        raise e
    


@user_router.patch('/update-user/{user_id}', tags=['User'])
async def update_user(
    user_id: int,
    updated_data: UserModel,
    db = Depends(get_db_connection)
):
    try:
        result = await UserModel.update_user_details(user_id, updated_data, db)
        return result
    except BaseException as e:
        print(e)
        raise e
    

@user_router.delete('/delete-user/{user_id}', tags=['User'])
async def delete_user(
    user_id: int,
    db = Depends(get_db_connection)
):
    try:
        return await UserModel.delete_user(user_id, db)
    except BaseException as e:
        print(e)
        raise e


@user_router.get('/search', tags=['User'])
async def user(
    search: str,
    db = Depends(get_db_connection)
):
    try:
        return await UserModel.get_paginated_and_filtered_records(db, search)
    except BaseException as e:
        print(e)
        raise e
    





    