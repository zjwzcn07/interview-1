# coding: utf-8
"""
DepartmentService
"""
from inspect import Signature, Parameter
from ..models import Employee
from ..models import Department

parms = [Parameter('user_id', Parameter.POSITIONAL_OR_KEYWORD),
         Parameter('department_id', Parameter.POSITIONAL_OR_KEYWORD)]
sig = Signature(parms)


class DepartmentService(object):

    # FIXME: replace *args **kwargs with paramters
    def is_user_in_department(self, *args, **kwargs) -> bool:
        bound_val = sig.bind(*args, **kwargs)
        user_id = bound_val.arguments['user_id']
        department_id = bound_val.arguments['department_id']
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
