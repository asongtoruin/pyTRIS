## Creating an API object
The first step to accessing the data is to create an instance of the `API` 
object. The only parameter required is `version` - at the time of writing 
(July 2020), the only `version` of the webTRIS APIs that is available is 1.0.

```python
from pytris.api import API

api = API(version='1.0')
```