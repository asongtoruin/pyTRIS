class Area:
    def __init__(self, area_id: str, name: str, description: str, 
                 xlongitude: str, xlatitude: str, 
                 ylongitude: str, ylatitude: str):
        self.area_id = area_id
        self.name = name
        self.description = description
        self.xlongitude = xlongitude
        self.xlatitude = xlatitude
        self.ylongitude = ylongitude
        self.ylatitude = ylatitude



class AreaMixin(object):
    @staticmethod
    def _resp_to_areas(resp):
        return tuple(
            Area(
                area_id=a['Id'], name=a['Name'], description=a['Description'],
                xlongitude=a['XLongitude'], xlatitude=a['XLatitude'],
                ylongitude=a['YLongitude'], ylatitude=a['YLatitude'],
            )
            for a in resp['areas']
        )

    def get_all_areas(self):
        endpoint = 'areas'

        res = self._get(endpoint)

        return self._resp_to_areas(res)
