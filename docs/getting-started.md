## Creating an API object
The first step to accessing the data is to create an instance of the `API` 
object. The only parameter required is `version` - at the time of writing 
(July 2020), the only `version` of the webTRIS APIs that is available is 1.0.

```Python
from pytris.api import API

api = API(version='1.0')
```

## Accessing Endpoints
Endpoints are accessed through methods from the API object relating to their
corresponding resource. These are named in line with their descriptions from 
webTRIS, albeit with some modifications to match Python conventions. To access 
endpoints for Sites, for example, we can use:

```Python
from pytris.api import API

api = API(version='1.0')
sites = api.sites()
```

The methods that are available vary by the type of resource being accessed. Some
resources are used to access objects (_Sites_, _Areas_ and _SiteTypes_) while 
others are used to access data (_Reports_ and _Quality_). Next we'll go on to 
briefly describe how to use the _Sites_ and _Reports_ endpoints, as these are
likely to be the most used. Information on the other endpoints can be found in 
the [Endpoints](./endpoints.md) section.

### Sites
The Sites endpoints let the user look up information for one or all of the count
locations stored in webTRIS.

#### Looking up one site
Sometimes you may need to look up information for a single site - for example, 
when checking data that's been provided to you from some other source. To do 
this, we can use the `.get()` method for sites and pass through the ID of the
site we want to find information about:

```Python
from pytris.api import API

api = API(version='1.0')
sites = api.sites()

result = sites.get(1)
```

This will return a `Site` object - this is a data storage class containing the 
attributes relating to this site. The attributes are again named in line with 
the API documentation, so in this example we have:

- `result.id` gives the Site ID
- `result.description` provides the description
- `result.longitude` provides the longitude of the site location
- `result.latitude` provides the latitude of the site location
- `result.status` details the status of the site (e.g. _Active_, _Inactive_)

#### Looking up all sites
You may also want to look up _all_ of the webTRIS sites. There are, at time of
writing (July 2020), over 18,000 sites in webTRIS so care should be taken when
using this method. This may be useful, however, for mapping all sites and 
understanding which sites may be relevant for further analysis.

The `.all()` method returns a generator of `Site` objects, so in most cases 
you'll need to iterate through them:

```Python
from pytris.api import API

api = API(version='1.0')
sites = api.sites()

for site in sites.all():
    # Do something with each site
```

### Reports
_Coming soon_