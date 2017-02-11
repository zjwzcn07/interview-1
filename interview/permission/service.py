# coding: utf-8
"""
PermissionService
"""

from typing import Dict
from inspect import Signature, Parameter
from ..models import Develop
from ..models import Employee
from ..models import Resource
from ..models import Permission
from ..models import DevelopPermission
from ..models import DevelopLeaderPermission
from ..models import db

parms = [Parameter('user_id', Parameter.POSITIONAL_OR_KEYWORD),
         Parameter('resource_id', Parameter.POSITIONAL_OR_KEYWORD)]
sig = Signature(parms)


class PermissionService(object):

    def grant_department_permissions(self, department_id, permission_id):
        newRow = DevelopPermission(
            develop_id=department_id, permission_id=permission_id)
        db.session.add(newRow)
        db.session.commit()

    def grant_department_leader_permissions(self, department_id, permission_id):
        # 伪递归向上赋予权限
        while department_id:
            leader_id = Develop.query.filter_by(
                id=department_id).first().leader_id
            if leader_id == 0:
                break
            newRow = DevelopLeaderPermission(
                develop_id=leader_id, permission_id=permission_id)
            db.session.add(newRow)
            department_id = leader_id
        db.session.commit()

    # FIXME: replace *args **kwargs with paramters
    def get_user_permissions(self, *args, **kwargs) -> Dict:
        result = set()
        temp_result = set()
        dict_result = {}
        bound_val = sig.bind(*args, **kwargs)
        user_id = bound_val.arguments['user_id']
        resource_id = bound_val.arguments['resource_id']

        exist_user_id = Employee.query.filter_by(id=user_id).first()
        exist_resource_id = Resource.query.filter_by(id=resource_id).first()
        if exist_resource_id and exist_user_id:
            department_id = Employee.query.filter_by(
                id=user_id).first().develop_id
            # 向上递归检查领导是否有向下特权
            while department_id:
                department_permission = DevelopPermission.query.filter_by(
                    develop_id=department_id).all()
                for each_permission in department_permission:
                    temp_result.update(Permission.query.filter_by(
                        resources_id=resource_id, id=each_permission.permission_id).all())
                department_id = Develop.query.filter_by(
                    id=department_id).first().leader_id
            department_id = Employee.query.filter_by(
                id=user_id).first().develop_id
            # 检查自己是否有leader权限
            if bool(Develop.query.filter_by(leader_id=department_id)):
                department_leader_permission = DevelopLeaderPermission.query.filter_by(
                    develop_id=department_id).all()
                for each_permission in department_leader_permission:
                    temp_result.update(Permission.query.filter_by(
                        resources_id=resource_id, id=each_permission.permission_id).all())
            for each_permission in temp_result:
                result.add(each_permission.action)
        dict_result['permissions'] = result
        return dict_result
