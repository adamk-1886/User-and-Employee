from fastorm import FastORM
from typing import Optional, Union

class User(FastORM):
    _primary_keys = ["id"]
    _table_name = "users"

    id: Optional[int]
    name: str
    email: str

class Employee(FastORM):
    _primary_keys = ['id']
    _table_name = 'employees'

    id: Optional[int]
    user_id: Union[int, User]
    employee_role: str
    employee_designation: str

    


