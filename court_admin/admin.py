from django.contrib import admin
from django.contrib.admin.sites import AdminSite


class CourtAdmin(AdminSite):
    pass

court_admin = CourtAdmin()

