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
        return self._objects_from_resp(request.fetch(), self.model, self.path)

    def get(self, key):
        # TODO check key type
        item_path = '/'.join([self.path, str(key)])
        request = self.request_class(self.version, item_path)

        # Single item endpoints seem to still return an iterable for objects.
        # Only return the first one.
        return next(
            self._objects_from_resp(request.fetch(), self.model, self.path)
        )
    
    def _objects_from_resp(self, resp, model, key_name):
        return (
            model(**{k.lower(): v for k, v in mod_dict.items()})
            for mod_dict in resp[key_name]
        )

class SubObjectEndpoint(ObjectEndpoint):
    def __init__(self, version, path, model, submodel, sub_path, request_class):
        super().__init__(version, path, model, request_class)
        self.submodel = submodel
        self.sub_path = sub_path

    def get(self, *args, **kwargs):
        BaseEndpoint.get(self, *args, **kwargs)
    
    def get_children(self, key):
        item_path = '/'.join([self.path, str(key), self.sub_path])
        request = self.request_class(self.version, item_path)
        return self._objects_from_resp(
            request.fetch(), self.submodel, self.sub_path
        )


class DataEndpoint(BaseEndpoint):
    pass
