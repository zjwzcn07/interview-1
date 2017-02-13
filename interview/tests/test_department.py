# coding: utf-8
"""

"""
from unittest import TestCase
from ..department.service import DepartmentService
from ..models import db
from ..models import Department
from ..models import Employee
from ..models import Resource
from ..models import Permission


class TestDepartment(TestCase):

    def setUp(self):
        # pass
        db.drop_all()
        db.create_all()
        # id = 1
        company = Department(name='company')

        # id = 2 3
        RD1 = Department(name='R&D_1', leader_id=1)
        RD2 = Department(name='R&D_2', leader_id=1)

        # id = 4 5
        clientRD1 = Department(name='clientR&D_1', leader_id=2)
        clientRD2 = Department(name='clientR&D_2', leader_id=3)

        # id = 6 7
        androidRD = Department(name='android', leader_id=4)
        iosRD = Department(name='ios', leader_id=5)

        # id = 1 2 3
        employee1 = Employee(name='Alice', department=clientRD1)
        employee2 = Employee(name='Bob', department=androidRD)
        employee3 = Employee(name='Eve', department=iosRD)

        # db.session.add_all(
        # [company, RD1, RD2, clientRD1, clientRD2,androidRD, iosRD,
        #  employee1, employee2,employee3])

        resource1 = Resource(name='resource1')
        resource2 = Resource(name='resource2')

        permission1 = Permission(action='read', resource=resource1)
        permission2 = Permission(action='write', resource=resource1)
        permission3 = Permission(action='remove', resource=resource2)
        permission4 = Permission(action='modify', resource=resource2)

        db.session.add_all(
            [company, RD1, RD2, clientRD1, clientRD2, androidRD, iosRD,
             employee1, employee2, employee3,
             resource1, resource2,
             permission1, permission2, permission3, permission4])

        db.session.commit()

    def tearDown(self):
        pass

    def test_is_user_in_department(self):
        # raise NotImplementedError()
        newService = DepartmentService()

        # employee1 in depart 1->2->4
        assert(newService.is_user_in_department(1, 1) == True)
        assert(newService.is_user_in_department(1, 2) == True)
        assert(newService.is_user_in_department(1, 3) == False)
        assert(newService.is_user_in_department(1, 4) == True)

        # employee2 in depart 1->2->4->6
        assert(newService.is_user_in_department(2, 1) == True)
        assert(newService.is_user_in_department(2, 2) == True)
        assert(newService.is_user_in_department(2, 4) == True)
        assert(newService.is_user_in_department(2, 5) == False)
        assert(newService.is_user_in_department(2, 6) == True)

        # employee1 in depart 1->3->5->7
        assert(newService.is_user_in_department(3, 1) == True)
        assert(newService.is_user_in_department(3, 3) == True)
        assert(newService.is_user_in_department(3, 4) == False)
        assert(newService.is_user_in_department(3, 5) == True)
