from fastapi import APIRouter, Depends
from models.employee import EmployeeModel
from config.database_connection import get_db_connection

employee_router = APIRouter()

@employee_router.post('/create-employee', tags=['Employee'])
async def create_employee(
    employee: EmployeeModel,
    conn = Depends(get_db_connection)
):
    try:
        response = await employee.create_employee(conn)
        return {
            "Message:": "Employee Created Successfully",
            "Details": response
        }
    except BaseException as e:
        print(e)
        raise e


@employee_router.get('/get-all-employees', tags=['Employee'])
async def get_all_employees(
    conn = Depends(get_db_connection)
):
    try: 
        return await EmployeeModel.get_employee_details(conn)
    except BaseException as e:
        print(e)
        raise e
    

@employee_router.get('/get-employee-by-name', tags=['Employee'])
async def get_employee_by_name(
    name: str,
    db = Depends(get_db_connection)
):
    try:
        user = await EmployeeModel.get_employee_by_name(name, db)
        return user
    except BaseException as e:
        print(e)
        raise e
    

@employee_router.patch('/update-employee/{employee_id}', tags=['Employee'])
async def update_employee(
    employee_id: int,
    updated_data: EmployeeModel,
    db = Depends(get_db_connection)
):
    try:
        result = await EmployeeModel.update_employee_details(employee_id, updated_data, db)
        return result
    except BaseException as e:
        print(e)
        raise e
    


@employee_router.delete('/delete-employee/{employee_id}', tags=['Employee'])
async def delete_employee(
    employee_id: int,
    db = Depends(get_db_connection)
):
    try:
        return await EmployeeModel.delete_employee(employee_id, db)
    except BaseException as e:
        print(e)
        raise e


@employee_router.get('/search-employee', tags=['Employee'])
async def employee(
    search: str,
    db = Depends(get_db_connection)
):
    try:
        return await EmployeeModel.get_paginated_and_filtered_records(db, search)
    except BaseException as e:
        print(e)
        raise e
    





    