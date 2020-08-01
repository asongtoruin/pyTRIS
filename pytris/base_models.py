from .utilities import requires_pandas


class Model:
    def __init__(self, *args, **kwargs):
        pass


class Report(list):
    @requires_pandas
    def to_frame(self):
        return pd.DataFrame(self)
