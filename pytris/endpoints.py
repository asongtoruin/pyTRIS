from typing import Iterator, Optional, Type, Union

from .base_models import Model, Report
from .requests import HTTPRequest


class BaseEndpoint:
    def __init__(self, version: str, path: str, 
                 model: Union[Type[Model], Type[Report]], 
                 request_class: Type[HTTPRequest]):
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

    def get(self, key: Union[int, str]):
        # TODO check key type
        item_path = '/'.join([self.path, str(key)])
        request = self.request_class(self.version, item_path)

        # Single item endpoints seem to still return an iterable for objects.
        # Only return the first one.
        return next(
            self._objects_from_resp(request.fetch(), self.model, self.path)
        )
    
    def _objects_from_resp(self, resp: dict, 
                           model: Union[Type[Model], Type[Report]], 
                           key_name: str):
        return (
            model(**{k.lower(): v for k, v in mod_dict.items()})
            for mod_dict in resp[key_name]
        )

class SubObjectEndpoint(ObjectEndpoint):
    def __init__(self, version: str, path: str, 
                 model: Type[Model], submodel: Type[Model], 
                 sub_path: str, request_class: Type[HTTPRequest]):
        super().__init__(version, path, model, request_class)
        self.submodel = submodel
        self.sub_path = sub_path

    def get(self, *args, **kwargs):
        BaseEndpoint.get(self, *args, **kwargs)
    
    def get_children(self, key: Union[int, str]):
        item_path = '/'.join([self.path, str(key), self.sub_path])
        request = self.request_class(self.version, item_path)
        return self._objects_from_resp(
            request.fetch(), self.submodel, self.sub_path
        )


class DataEndpoint(BaseEndpoint):
    PAGE_SIZE = 50

    def __init__(self, version: str, path: str, 
                 model: Type[Report], request_class: Type[HTTPRequest], 
                 interval: str, entry_point: str, 
                 required: Iterator[str], paginate: bool):
        super().__init__(version, path, model, request_class)
        self._interval = interval
        self._entry_point = entry_point
        self._paginate = paginate
        self._required = required

    def get(self, page_size: Optional[int]=None, **kwargs):
        if not page_size:
            page_size = self.PAGE_SIZE

        missing_params = [k for k in self._required if k not in kwargs.keys()]
        if missing_params:
            raise ValueError(
                f'Missing required parameters: {", ".join(missing_params)}'
            )
        
        if self._paginate:
            kwargs['page'] = 1
            kwargs['page_size'] = page_size

        endpoint_path = '/'.join([self.path, self._interval])

        request = self.request_class(self.version, endpoint_path)
        resp = request.fetch(params=kwargs)

        results = resp[self._entry_point]

        # TODO make this neater? It's kinda ugly.
        if self._paginate:
            next_page = self._next_page_link(resp)
            while next_page is not None:
                kwargs['page'] += 1
                resp = request.fetch(params=kwargs)

                results += resp[self._entry_point]
                next_page = self._next_page_link(resp)
        
        return self.model(results)
                
    
    @staticmethod
    def _next_page_link(resp: dict):
        header = resp.get('Header', dict())
        links = header.get('links', [])

        for link in links:
            if link['rel'].lower() == 'nextpage':
                return link['href']
        
        return None