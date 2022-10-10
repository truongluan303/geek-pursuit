from flask import Blueprint

routes = Blueprint("routes", __name__)

from .index import *
from .linkedin_job_info import *
from .linkedin_company_info import *
