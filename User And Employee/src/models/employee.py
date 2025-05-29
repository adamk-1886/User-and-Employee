from typing import Optional
from pydantic import BaseModel
from database.schema import Employee, User
from fastapi import HTTPException, status

class EmployeeModel(BaseModel):
    id: Optional[int]
    user_id: int
    employee_role: str
    employee_designation: str

    
    @staticmethod
    async def get_employee_by_id_utility(conn, employee_id):
        return await Employee.get(conn, id=employee_id)


    async def create_employee(self, conn):
        current_user = await User.get(conn, id = self.user_id)
        curent_employee = await EmployeeModel.get_employee_by_id_utility(conn, self.id)

        if curent_employee:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User with this id already exists')

        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist make sure before employee you have a user')

        employee_to_add = Employee(
            id=self.id,
            user_id=self.user_id,
            employee_role=self.employee_role,
            employee_designation=self.employee_designation
        )
        await employee_to_add.insert(conn=conn)
        return employee_to_add
    

    @staticmethod
    async def get_employee_details(
        conn
    ):
        result = await Employee.select(conn)
        return result
    

    
    @staticmethod
    async def get_employee_by_user_name(name: str, conn):
        user = await Employee.get(conn, name = name)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with this name does not exist')
        return user

    
    @staticmethod
    async def update_employee_details(employee_id, updated_data, conn):
        current_record = await EmployeeModel.get_employee_by_id_utility(conn, employee_id)

        if not current_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')


        for k, v in updated_data.dict(exclude_unset = True).items():
            setattr(current_record, k, v)
        await current_record.update(conn=conn)

        return current_record
    

    @staticmethod
    async def delete_employee(employee_id: int, conn):
        current_record = await Employee.get(conn, id=employee_id)

        if not current_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')

        
        await current_record.delete(conn)

        return {
            "Message:": "Record deleted successfully!"
        }
    

    @staticmethod
    async def get_paginated_and_filtered_records(
        conn,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ):
        if search:
            all_employees = await Employee.select(conn=conn)
            filtered_employees = [
                employee for employee in all_employees
                if search.lower() in employee.employee_role.lower() or search.lower() in employee.employee_designation.lower()
            ]
        else:
            filtered_employees = await Employee.select(conn=conn)

        paginated_employees = filtered_employees[offset:offset+limit]
        return paginated_employees






