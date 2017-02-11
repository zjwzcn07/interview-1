# coding: utf-8
"""
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR

from .flask import app

db = SQLAlchemy(app)


class Develop(db.Model):
    __tablename__ = 'Department'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False, unique=True)
    leader_id = db.Column(BIGINT(unsigned=True), default=0)
    employees = db.relationship('Employee', backref='develop')
    develop_permissions = db.relationship(
        'DevelopPermission', backref='develop')


class Employee(db.Model):
    __tablename__ = 'Employee'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(64), nullable=False)
    develop_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Develop.id))


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
    develop_permissions = db.relationship(
        'DevelopPermission', backref='permission')


class DevelopPermission(db.Model):
    __tablename__ = 'DevelopPermission'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    develop_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Develop.id))
    permission_id = db.Column(
        BIGINT(unsigned=True), db.ForeignKey(Permission.id))


class DevelopLeaderPermission(db.Model):
    __tablename__ = 'DevelopLeaderPermission'
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    develop_id = db.Column(BIGINT(unsigned=True), db.ForeignKey(Develop.id))
    permission_id = db.Column(
        BIGINT(unsigned=True), db.ForeignKey(Permission.id))
