class BaseEndpoint:
    def __init__(self, version, path, model, request_class):
        self.version = version
        self.path = path
        self.model = model
        self.request_class = request_class

    def all(self, *args, **kwargs):
        raise NotImplementedError('Not implemented for this endpoint')

    def get(self, *args, **kwargs):
        raise NotImplementedError('Not implemented for this endpoint')


class ObjectEndpoint(BaseEndpoint):
    def all(self):
        request = self.request_class(self.version, self.path)
        return self._objects_from_resp(request.fetch())

    def get(self, key):
        # TODO check key type
        item_path = '/'.join([self.path, str(key)])
        request = self.request_class(self.version, item_path)
        return self._objects_from_resp(request.fetch())
    
    def _objects_from_resp(self, resp):
        return (
            self.model(**{k.lower(): v for k, v in mod_dict.items()})
            for mod_dict in resp[self.path]
        )


class DataEndpoint(BaseEndpoint):
    pass
