from typing import Optional
from pydantic import BaseModel, EmailStr
from database.schema import User
from fastapi import HTTPException, status

class UserModel(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr

    @staticmethod
    async def get_user_by_id_utility(conn, user_id):
        return await User.get(conn, id=user_id)

    async def create_user(self, conn):
        current_user = await UserModel.get_user_by_id_utility(conn, self.id)

        if current_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User with this id already exists')

        user_to_add = User(
            id=self.id,
            name=self.name,
            email=self.email
        )
        await user_to_add.insert(conn=conn)
        return user_to_add
    

    @staticmethod
    async def get_user_details(
        conn
    ):
        result = await User.select(conn)
        return result
    

    
    @staticmethod
    async def get_user_by_name(name: str, conn):
        user = await User.get(conn, name = name)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with this name does not exist')
        return user

    
    @staticmethod
    async def update_user_details(user_id, updated_data, conn):
        current_record = await UserModel.get_user_by_id_utility(conn, user_id)

        if not current_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')


        for k, v in updated_data.dict(exclude_unset = True).items():
            setattr(current_record, k, v)
        await current_record.update(conn=conn)

        return current_record
    

    @staticmethod
    async def delete_user(user_id: int, conn):
        current_record = await User.get(conn, id = user_id)

        if not current_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')

        
        await current_record.delete(conn)

        return {
            "Message: ": "Record deleted successfully!"
        }
    

    @staticmethod
    async def get_paginated_and_filtered_records(
        conn,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ):
        if search:
            all_users = await User.select(conn=conn)
            filtered_users = [
                user for user in all_users
                if search.lower() in user.name.lower() or search.lower() in user.email.lower()
            ]
        else:
            filtered_users = await User.select(conn=conn)

        paginated_users = filtered_users[offset:offset+limit]
        return paginated_users






