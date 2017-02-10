# coding: utf-8
"""
"""
from flask import Flask
app = Flask('interview', instance_relative_config=True)
app.config.from_object('interview.config.common')
