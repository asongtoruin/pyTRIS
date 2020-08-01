class Model:
    def __init__(self, *args, **kwargs):
        pass


class Report(list):
    def to_frame(self):
        import pandas as pd

        return pd.DataFrame(self)
