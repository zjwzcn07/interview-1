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
    employee = db.relationship('Employee', backref='department')
    leader_id = db.Column(BIGINT(unsigned=True), default=0)


class Employee(db.Model):
    __tablename__ = 'Employee'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    department_id = db.Column(
        BIGINT(unsigned=True), db.ForeignKey(Department.id))
