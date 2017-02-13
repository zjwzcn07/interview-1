# coding: utf-8
"""
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR

from .flask import app

db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = 'Department'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False, unique=True)
    leader_id = db.Column(BIGINT(unsigned=True), default=0)
    employees = db.relationship('Employee', backref='department')
    department_permissions = db.relationship(
        'DepartmentPermission', backref='department')


class Employee(db.Model):
    __tablename__ = 'Employee'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    department_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Department.id))


class Resource(db.Model):
    __tablename__ = 'Resource'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    permissions = db.relationship('Permission', backref='resource')


class Permission(db.Model):
    __tablename__ = 'Permission'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    action = db.Column(VARCHAR(64), nullable=False)
    resources_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Resource.id))
    department_permissions = db.relationship(
        'DepartmentPermission', backref='permission')


class DepartmentPermission(db.Model):
    __tablename__ = 'DepartmentPermission'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Department.id))
    permission_id = db.Column(
        BIGINT(unsigned=True), db.ForeignKey(Permission.id))


class DepartmentLeaderPermission(db.Model):
    __tablename__ = 'DepartmentLeaderPermission'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    department_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Department.id))
    permission_id = db.Column(
        BIGINT(unsigned=True), db.ForeignKey(Permission.id))
