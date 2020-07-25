from .api import API
from .endpoints import ObjectEndpoint, SubObjectEndpoint


class Model:
    pass


@API.register('areas', endpoint_type=ObjectEndpoint)
class Area(Model):
    def __init__(self, id: str, name: str, description: str, 
                 xlongitude: str, xlatitude: str, 
                 ylongitude: str, ylatitude: str):
        self.id = id
        self.name = name
        self.description = description
        self.xlongitude = xlongitude
        self.xlatitude = xlatitude
        self.ylongitude = ylongitude
        self.ylatitude = ylatitude


@API.register('sites', endpoint_type=ObjectEndpoint)
class Site(Model):
    def __init__(self, id: str, name: str, description: str, 
                 longitude: str, latitude: str, status: str):
        self.id = id
        self.name = name
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.status = status


@API.register('site_types', endpoint_type=SubObjectEndpoint, submodel=Site,
              sub_path='sites')
class SiteType(Model):
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
