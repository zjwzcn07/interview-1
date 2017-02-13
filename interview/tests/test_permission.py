# coding: utf-8
"""
 
"""
from unittest import TestCase
from ..permission.service import PermissionService

from ..models import db
from ..models import Department
from ..models import Employee
from ..models import Resource
from ..models import Permission
from ..models import DepartmentPermission
from ..models import DepartmentLeaderPermission


class TestPermission(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_permissions(self):
        newService = PermissionService()
        print("grant department 2 permission 1")
        # permission1 to department 2->4->6
        newService.grant_department_permissions(2, 1)
        temp = newService.get_user_permissions(1, 1)['permissions']
        print(temp)
        assert(temp == set(["read"]))

        print("grant department 2 permission 2")
        # permission2 to department 1->2->4->6, 1->3->5->7
        newService.grant_department_permissions(1, 2)
        temp = newService.get_user_permissions(1, 1)['permissions']
        print(temp)
        assert(temp == set(["read", "write"]))

        print("grant leader_department 6 permission 3")
        # permission3 to department 4<-2<-1
        newService.grant_department_leader_permissions(6, 3)
        temp = newService.get_user_permissions(2, 2)['permissions']
        print(temp)
        assert(temp == set())

        print("query user_1 have resource 2")
        temp = newService.get_user_permissions(1, 2)['permissions']
        print(temp)
        assert(temp == set(["remove"]))

        print("grant department 7 permission 4")
        # permission4 to department 7
        newService.grant_department_permissions(7, 4)
        temp = newService.get_user_permissions(3, 2)['permissions']
        print(temp)
        assert(temp == set(['modify']))

        print("query user 3 have resource 2")
        temp = newService.get_user_permissions(3, 2)['permissions']
        print(temp)
        assert(temp == set(["modify"]))

        print("grant leader_department 6 permission 4")
        # permission4 to department 4<-2<-1
        newService.grant_department_leader_permissions(6, 4)
        temp = newService.get_user_permissions(1, 2)['permissions']
        print(temp)
        assert(temp == set(["modify", "remove"]))

        print("hehe")
