## Creating an API object
The first step to accessing the data is to create an instance of the `API` 
object. The only parameter required is `version` - at the time of writing 
(July 2020), the only `version` of the webTRIS APIs that is available is 1.0.

```Python
from pytris.api import API

api = API(version='1.0')
```

## Accessing Endpoints
Endpoints are accessed through methods from the API object. These are named 
in line with their descriptions from webTRIS, albeit with some modifications to 
match Python conventions. To access endpoints for Sites, for example, we can 
use:

```Python
from pytris.api import API

api = API(version='1.0')
sites = api.sites()
```
