# coding: utf-8
"""
DepartmentService
"""
from ..models import Employee
from ..models import Department


class DepartmentService(object):

    # FIXME: replace *args **kwargs with paramters
    def is_user_in_department(self, user_id:int, department_id:int) -> bool:
        # 返回查到的第一个元素
        exist_user_id = Employee.query.filter_by(id=user_id).first()
        exist_department_id = Department.query.filter_by(
            id=department_id).first()
        # 确有此查询
        if exist_user_id and exist_department_id:
            user_department_id = Employee.query.filter_by(
                id=user_id).first().department_id
            # 如果当前部门就是所查即返回，否则检查其上级部门
            if user_department_id == department_id:
                return True
            while user_department_id:
                if department_id == user_department_id:
                    return True
                user_department_id = Department.query.filter_by(
                    id=user_department_id).first().leader_id
            return False
        return False
