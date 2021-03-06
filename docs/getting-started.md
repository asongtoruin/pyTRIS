## Creating an API object
The first step to accessing the data is to create an instance of the `API` 
object. The only parameter required is `version` - at the time of writing 
(July 2020), the only `version` of the webTRIS APIs that is available is 1.0, 
and so this is passed through by default

```Python
from pytris import API

api = API()
```

## Accessing Endpoints
Endpoints are accessed through methods from the API object relating to their
corresponding resource. These are named in line with their descriptions from 
webTRIS, albeit with some modifications to match Python conventions. To access 
endpoints for Sites, for example, we can use:

```Python
from pytris import API

api = API()
sites = api.sites()
```

The methods that are available vary by the type of resource being accessed. Some
resources are provided as objects (_Sites_, _Areas_ and _SiteTypes_) while 
others are provide data (_Reports_ and _Quality_). Next we'll go on to briefly 
describe how to use the _Sites_ and _Reports_ endpoints, as these are likely to 
be the most used. Information on the other endpoints can be found in the 
[Endpoints](./endpoints.md) section.

### Sites
The Sites endpoints let the user look up information for one or all of the count
locations stored in webTRIS.

#### Looking up one site
Sometimes you may need to look up information for a single site - for example, 
when checking data that's been provided to you from some other source. To do 
this, we can use the `.get()` method for sites and pass through the ID of the
site we want to find information about:

```Python
from pytris import API

api = API()
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
from pytris import API

api = API()
sites = api.sites()

for site in sites.all():
    # Do something with each site
    print(site.id, site.description)
```

### Reports
`pyTRIS` handles Reports in a slightly differently manner to Sites. 

#### Report Types
webTRIS provides three different kinds of report. In `pyTRIS`, we handle these
through different methods on the `API` object:

* `.daily_reports()`, which provides data down to 15 minute intervals
* `.monthly_reports()`, which provides summaries by day
* `.annual_reports()`, which provides averages for each year

#### Required Parameters
Each of these methods has the same required parameters:

* `sites` should either be:
    * the `id` of a single site to be looked up, which can be passed as either a 
      string or integer
    * multiple site IDs joined with commas and provided as a single string - 
      e.g. `'8438,8439'`
* `start_date` should be a date in string format of `DDMMYYYY` - e.g. 
  `'01012020'` for the 1st January 2020
* `end_date` should be a date, again as a string in the same format

??? warning
    If any of the required parameters are missing, `pyTRIS` will raise a 
    `ValueError` detailing the missing parameters.

#### Report Format
The reports themselves are provided as lists - the format varies slightly 
between the different report types, but the columns provided are fairly 
straightforward.

#### Example
Putting this together, an example to get data for one site would be as follows:

```Python
from pytris import API

api = API()
daily = api.daily_reports()

result = daily.get(
    sites=8438, start_date='01122019', end_date='01022020'
)
```

Changing to return `monthly_reports` or `annual_reports` just requires changing
the method used.

??? example "Example for `monthly_reports`"
    To get monthly reports, the `daily_reports` example would change to be as 
    follows:

    ```Python
    from pytris import API

    api = API()
    monthly = api.monthly_reports()

    result = monthly.get(
        sites=8438, start_date='01122019', end_date='01022020'
    )
    ```

??? example "Example for Multiple Sites"
    To get multiple sites, the `daily_reports` example would change to be as 
    follows:

    ```Python
    from pytris import API

    api = API()
    daily = api.daily_reports()

    result = daily.get(
        sites='8438,8439', start_date='01122019', end_date='01022020'
    )
    ```

#### Exporting to `pandas`

!!! warning
    Installing `pyTRIS` does not install of `pandas` as a dependency, and as 
    such the user must ensure that `pandas` is installed in their environment 
    for the following examples to work.

Many data analysis processes in Python involve the use of `pandas` and its 
`DataFrame` objects. With this in mind, `pyTRIS` offers a direct way of 
exporting a `Report` to a `DataFrame` through the `to_frame()` method.

For `daily_reports` and `annual_reports`, this method directly returns a 
`DataFrame`, like so:

```Python
from pytris import API

api = API()
daily = api.daily_reports()

result = daily.get(
    sites=8438, start_date='01122019', end_date='01022020'
)

df = result.to_frame()
```

For `monthly_reports`, however, the process is slightly different. This endpoint
provides multiple aggregations of data. As such, the `to_frame()` method for 
this endpoint provides a `dict` of dataframes. The keys to this `dict` describe
the data contained within the values, which are:

- *Days*, which provides total flows for each individual day
- *Daily Aggregations*, which provides averages for each weekday within each 
  month
- *Hourly Aggregations*, which provides averages by hour for each weekday within 
  each month
- *Summary Aggregations*, which provides high-level summary figures for each 
  month (e.g. ADT)