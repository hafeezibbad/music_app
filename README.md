# Music App
This project has been completed in accordance with requirements mentioned in [assignment description](https://github.com/hafeezibbad/music_app/blob/master/backend_test.txt). 
In this project, we have developed an API for performing search operations on a database of Songs. The project is
 developed using [Python](https://www.python.org/) programming language and [mongoDB](https://www.mongodb.com/) for
  data storage. 
  
## Setup the project locally. 
Please follow the following instructions to set up the project locally. The project has been developed using
 ``Python3.6`` and ``mongoDB``.

---
**NOTE**

The project has been developed and tested on a machine running Ubuntu 18.04 LTS operating system. The following
 instructions have been tested to run on similar operating systems. 
If you are using a different operating system, please use corresponding commands for your operating system.  

---  
  
* Make sure that you have ``Python3`` installed on your machine.
 
```bash
$ python3 --version   
Python 3.X.X

```
If you do not have a Python3 installation on your machine, please follow the instructions given 
[here](https://realpython.com/installing-python/). 
The project was developed using ``python3.6``. Since this project uses 
[typing](https://docs.python.org/3/library/typing.html) module, it will not work with python versions lower than
 ``python3.6``.
If your system default ``python3`` is ``python3.5`` or lower, please 
* either modify the ``PYTHON_RUNTIME`` variable in [Makefile](https://github.com/hafeezibbad/music_app/blob/master/Makefile) to use a different version of file
```text
PTYHON_RUNTIME ?= python3.6
``` 

* or set environment variable ``PYTHON_RUNTIME`` to specific python version 
    
```bash
export PYTHON_RUNTIME=python3.6
``` 

* Make sure, you have ``mongoDB`` installation on your machine 
```bash
$ mongo --version
MongoDB shell version v4.2.8
git version: 43d25964249164d76d5e04dd6cf38f6111e21f5f
OpenSSL version: OpenSSL 1.1.1  11 Sep 2018
allocator: tcmalloc
modules: none
build environment:
    distmod: ubuntu1804
    distarch: x86_64
    target_arch: x86_64
``` 
If you do not have ``mongoDB`` installed on your machine, please follow the [instructions](https://docs.mongodb.com/manual/installation/) to install it on your  machine.

In this project, we use python [venv](https://docs.python.org/3/library/venv.html) module to setup virtual
 environment. You can use other alternatives, such, [pipenv](https://github.com/pypa/pipenv), 
 [virtualenv](https://github.com/pypa/virtualenv) for this purpose as well. 
 
* Set up python virtual environment for setting up the project 

```bash
$ make python-venv
```
You can modify the name of default virtual environment (set up by ``make`` target) by modifying ``VIRTUAL_ENV
`` variable in [Makefile](https://github.com/hafeezibbad/music_app/blob/master/Makefile) 
In case you are using some other method instead of ``make`` targets for setting up virtual environment, please
 install project dependencies by running 
 
```bash
$ pip install -r requirements-dev.txt
``` 

* Run ``mongoDB`` server on your local machine. 
```bash
$ make mongodb-offline

Starting MongoDB locally
mongod
2020-07-09T10:22:09.621+0300 I  CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2020-07-09T10:22:09.636+0300 W  ASIO     [main] No TransportLayer configured during NetworkInterface startup
2020-07-09T10:22:09.636+0300 I  CONTROL  [initandlisten] MongoDB starting : pid=16668 port=27017 dbpath=/data/db 64-bit host=dev-ws

```
Please note that we run ``mongodb`` server on the default port number ``27017``. In case this port number changes
, please modify it accordingly in configuration file available in [configs/app/](https://github.com/hafeezibbad/music_app/tree/master/configs/app). 
You can run ``mongodb`` on custom port (``55555`` in this case) using ``make`` target as
```bash
$ DB_PORT_NUMBER=55555 make mongodb-offline
```

* Run app on your local machine using following command.
```bash
$ make app-offline

 * Serving Flask app "src.app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:3500/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-739-668
```
Now your server must be up and ready for usage. 
The server provides different endpoints which are discussed in Endpoints section.
Please note that 
* This target uses [dev-configuration](https://github.com/hafeezibbad/music_app/blob/master/configs/app/dev/config.yml) by default. In case you want to run some other configuration
 for running the application, please modify ``STAGE`` variable in [Makefile](https://github.com/hafeezibbad/music_app/blob/master/Makefile), or run this target as. 

```bash
$ STAGE="test" make app-offline
```
* This target assumes that ``mongoDB`` instance is running on ``DbHost`` and ``DbPort`` (specified in configuration
 file).  
* Yu can modify the server port and host address in configuration file. 


 
Once the server is up and running, you can run the end to end tests against this server as
```bash
$ make install-and-e2e-test
```
By default the end-to-end tests use the deployment environment (STAGE) specified in [Makefile](https://github.com/hafeezibbad/music_app/blob/master/Makefile), but you can run the
 tests against any other environment as ``STAGE="test" make install-and-e2e-test``
If you have modified ``ServerPort`` and/or ``EndpointBaseUrl`` settings in configuration file, or you want to run
 tests against another deployment of this app, please run e2e tests as ``ENDPOINT_BASE_URL='<base_url>' make e2e-test``

## Endpoints
All the endpoints listed as follows are tested for sunny day scenario, and these scenarios have been added to end-to
-end test suite. We support ``If-(None-)Match`` header for some of the endpoints, but it is not enforced. 

---
**NOTE**
We use ``/api/v1`` prefix for all API endpoints. This can be changed/removed by modifying the ``SONGS_API_PREFIX
`` variable in [src/routes/songs_api.py](https://github.com/hafeezibbad/music_app/blob/master/src/routes/songs_api.py#L19) file. 
----
### [GET] /api/v1/songs
This endpoint can be used to get a list of all songs in the database. 

```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs' \
--header 'Content-Type: application/json'
```

```json
{
    "songs": [
        {
            "artist": "The Yousicians",
            "title": "Lycanthropic Metamorphosis",
            "difficulty": 14.6,
            "level": 13,
            "rating": [],
            "released": "2016-10-26",
            "version": 0,
            "song_id": 1,
            "created_at": "2020-07-09T11:30:58.185000",
            "last_modified_at": "2020-07-09T11:30:58.185000"
        },
        {
            "artist": "The Yousicians",
            "title": "A New Kennel",
            "difficulty": 9.1,
            "level": 9,
            "rating": [],
            "released": "2010-02-03",
            "version": 0,
            "song_id": 2,
            "created_at": "2020-07-09T11:30:58.263000",
            "last_modified_at": "2020-07-09T11:30:58.263000"
        },
        {
            "artist": "Mr Fastfinger",
            "title": "Awaki-Waki",
            "difficulty": 15.0,
            "level": 13,
            "rating": [],
            "released": "2012-05-11",
            "version": 0,
            "song_id": 3,
            "created_at": "2020-07-09T11:30:58.268000",
            "last_modified_at": "2020-07-09T11:30:58.268000"
        },
        {
            "artist": "The Yousicians",
            "title": "You've Got The Power",
            "difficulty": 13.22,
            "level": 13,
            "rating": [],
            "released": "2014-12-20",
            "version": 0,
            "song_id": 4,
            "created_at": "2020-07-09T11:30:58.277000",
            "last_modified_at": "2020-07-09T11:30:58.277000"
        },
        {
            "artist": "The Yousicians",
            "title": "Wishing In The Night",
            "difficulty": 10.98,
            "level": 9,
            "rating": [],
            "released": "2016-01-01",
            "version": 0,
            "song_id": 5,
            "created_at": "2020-07-09T11:30:58.285000",
            "last_modified_at": "2020-07-09T11:30:58.285000"
        },
        {
            "artist": "The Yousicians",
            "title": "Opa Opa Ta Bouzoukia",
            "difficulty": 14.66,
            "level": 13,
            "rating": [],
            "released": "2013-04-27",
            "version": 0,
            "song_id": 6,
            "created_at": "2020-07-09T11:30:58.293000",
            "last_modified_at": "2020-07-09T11:30:58.293000"
        },
        {
            "artist": "The Yousicians",
            "title": "Greasy Fingers - boss level",
            "difficulty": 2.0,
            "level": 3,
            "rating": [],
            "released": "2016-03-01",
            "version": 0,
            "song_id": 7,
            "created_at": "2020-07-09T11:30:58.298000",
            "last_modified_at": "2020-07-09T11:30:58.298000"
        },
        {
            "artist": "The Yousicians",
            "title": "Alabama Sunrise",
            "difficulty": 5.0,
            "level": 6,
            "rating": [],
            "released": "2016-04-01",
            "version": 0,
            "song_id": 8,
            "created_at": "2020-07-09T11:30:58.305000",
            "last_modified_at": "2020-07-09T11:30:58.305000"
        },
        {
            "artist": "The Yousicians",
            "title": "Can't Buy Me Skills",
            "difficulty": 9.0,
            "level": 9,
            "rating": [],
            "released": "2016-05-01",
            "version": 0,
            "song_id": 9,
            "created_at": "2020-07-09T11:30:58.312000",
            "last_modified_at": "2020-07-09T11:30:58.312000"
        },
        {
            "artist": "The Yousicians",
            "title": "Vivaldi Allegro Mashup",
            "difficulty": 13.0,
            "level": 13,
            "rating": [],
            "released": "2016-06-01",
            "version": 0,
            "song_id": 10,
            "created_at": "2020-07-09T11:30:58.317000",
            "last_modified_at": "2020-07-09T11:30:58.317000"
        },
        {
            "artist": "The Yousicians",
            "title": "Babysitting",
            "difficulty": 7.0,
            "level": 6,
            "rating": [],
            "released": "2016-07-01",
            "version": 0,
            "song_id": 11,
            "created_at": "2020-07-09T11:30:58.323000",
            "last_modified_at": "2020-07-09T11:30:58.323000"
        }
    ]
}
```

The endpoint supports pagination by default, with 20 items per page by default. This number can be changed by
 modifying the ``pageSize`` parameter in request. If there are more songs in database than the specified page size
 , ``next_anchor`` is provided in response which should be used with subsequent API calls to get paginated responses
 . For example 
 
```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs?pageSize=1' \
--header 'Content-Type: application/json' 
```

```json
{
    "songs": [
        {
            "artist": "The Yousicians",
            "title": "Lycanthropic Metamorphosis",
            "difficulty": 14.6,
            "level": 13,
            "rating": [],
            "released": "2016-10-26",
            "version": 0,
            "song_id": 1,
            "created_at": "2020-07-09T11:30:58.185000",
            "last_modified_at": "2020-07-09T11:30:58.185000"
        }
    ],
    "links": {
        "next_anchor": "?nextId=2&pageSize=1"
    }
}
```

#### Limitations
* We use incremental sequence field as primary key in database for storing songs. Due to this, pagination
 may not behave as expected when some songs are deleted from in between primary key range.  
 

### [GET] /api/v1/songs/avg/difficulty
This endpoints returns average difficulty for all the songs in database. It accepts an optional parameter ``level``.
In case the optional parameter is provided, it returns average difficulty for the songs which have the same level as
 specified. 
 
_No level specified_
```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs/avg/difficulty'
```

```json
{
    "average_difficulty": 10.3
}
```

_level specified using optional parameter_
```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs/avg/difficulty?level=13'
```

```json
{
    "average_difficulty": 14.1
}
```

_No song found in database, or no songs with the specified level_
```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs/avg/difficulty?level=1'
```
```json
{
    "average_difficulty": 0
}
```

#### Limitations
* This request can take long to process if there are several thousands or millions of records in the database. 


### [GET] /songs/search
This endpoint takes a query parameter ``message`` and return all songs in database where *title* or *artist* contains
 specified message. The endpoint supports pagination by default with default page size of 20. 
 
```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs/search?message=yousician&pageSize=5'
```
```json
{
    "songs": [
        {
            "artist": "The Yousicians",
            "title": "Lycanthropic Metamorphosis",
            "difficulty": 14.6,
            "level": 13,
            "rating": [],
            "released": "2016-10-26",
            "version": 0,
            "song_id": 1,
            "created_at": "2020-07-09T11:30:58.185000",
            "last_modified_at": "2020-07-09T11:30:58.185000"
        },
        {
            "artist": "The Yousicians",
            "title": "A New Kennel",
            "difficulty": 9.1,
            "level": 9,
            "rating": [],
            "released": "2010-02-03",
            "version": 0,
            "song_id": 2,
            "created_at": "2020-07-09T11:30:58.263000",
            "last_modified_at": "2020-07-09T11:30:58.263000"
        },
        {
            "artist": "The Yousicians",
            "title": "You've Got The Power",
            "difficulty": 13.22,
            "level": 13,
            "rating": [],
            "released": "2014-12-20",
            "version": 0,
            "song_id": 4,
            "created_at": "2020-07-09T11:30:58.277000",
            "last_modified_at": "2020-07-09T11:30:58.277000"
        },
        {
            "artist": "The Yousicians",
            "title": "Wishing In The Night",
            "difficulty": 10.98,
            "level": 9,
            "rating": [],
            "released": "2016-01-01",
            "version": 0,
            "song_id": 5,
            "created_at": "2020-07-09T11:30:58.285000",
            "last_modified_at": "2020-07-09T11:30:58.285000"
        },
        {
            "artist": "The Yousicians",
            "title": "Opa Opa Ta Bouzoukia",
            "difficulty": 14.66,
            "level": 13,
            "rating": [],
            "released": "2013-04-27",
            "version": 0,
            "song_id": 6,
            "created_at": "2020-07-09T11:30:58.293000",
            "last_modified_at": "2020-07-09T11:30:58.293000"
        }
    ],
    "links": {
        "next_anchor": "?nextId=6&pageSize=5"
    }
}
```

Please note that ``links`` with next_anchor is only provided if the number of records matching this query are more than
 given page size. 
In case no records in database contain message in *title* or *artist* field, empty response is returned. 
```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs/search?message=invalid'
```
```json
{}
```

#### Limitations
* The response times may vary depending on the number of records matching the query in database. 
* If ``message`` is an empty string, all records from database are returned.

### [POST] /songs/rating
This endpoint takes two query string parameters namely ``song_id``, and ``rating``, and adds the required rating
 song (identified using ``song_id``) in database.

```bash
curl --location --request POST 'http://localhost:3500/api/v1/songs/rating?song_id=1&rating=2'
```

```json
{
    "artist": "The Yousicians",
    "title": "Lycanthropic Metamorphosis",
    "difficulty": 14.6,
    "level": 13,
    "rating": [
        2
    ],
    "released": "2016-10-26",
    "version": 1,
    "song_id": 1,
    "created_at": "2020-07-09T11:30:58.185000",
    "last_modified_at": "2020-07-09T12:24:56.574000"
}
```
 
#### Errors
* If no song exists in database with given ``song_id``, the response is ``404``.
* If ``rating`` is not in range ``[1, 5]``, the response is ``400 Bad Request``.


### GET /songs/avg/rating/<song_id>
This endpoint returns the stats for rating of a song with specified ``song_id``. 

```bash
curl --location --request GET 'http://localhost:3500/api/v1/songs/avg/rating/1'
```

```json
{
    "average": 3,
    "lowest": 1,
    "highest": 5
}
```

where the data for specific song (with ``song_id=1``) is given as follows
```json
{
    "artist": "The Yousicians",
    "title": "Lycanthropic Metamorphosis",
    "difficulty": 14.6,
    "level": 13,
    "rating": [
        2,
        1,
        3,
        4,
        5
    ],
    "released": "2016-10-26",
    "version": 5,
    "song_id": 1,
    "created_at": "2020-07-09T11:30:58.185000",
    "last_modified_at": "2020-07-09T12:26:19.500000"
}
```

#### Errors
* If no song exists in database with given ``song_id``, the response is ``404``.

## Assumptions
We have made following assumptions when developing this API. 
* ``level`` can be an integer in the range ``[1, 5]``
* ``difficulty`` for a song is always greater than ``0``
* A song with same _title_, _artist_, _difficulty_, _level_, and _release_date_ is considered as duplicate. When
 adding a duplicate song to the database using `[POST] /api/v1/songs/` request path will return `409 Conflict`.
* Instead of return ``404 NOT FOUND`` from ``[GET] /api/v1/songs/avg/difficulty`` and ``[GET] /songs/search`` when there
 are no records in database, the API returns ``200 OK`` with empty data. Perhaps this can be changed to return ``404``

## Known Issues 
* ``pipenv`` can be used to setup the virtual environment. 
* Unit tests must be added for several modules used in this project. Currently, the project has no unit test coverage
 :rage:.
* The application has not been stress tested with several million of records, so responses times for aggregate
 operations, for example, [GET] /songs/avg/difficulty may vary depending on the number of items in the database.   
* Although, we provide ``409 Conflict`` for a duplicate song record which has same release date, it is possible to
 add duplicate entries by first adding same song with two different release dates, and then modifying one of the
  songs using ``[PATCH] /api/v1/songs/<song_id>`` request to have same date as the other. This will result in two
   songs with similar data in the database. However, we can differentiate them based on ``version`` number and
    ``last_modified_at`` date.  
* Pagination logic will not work as expected if records are deleted but their IDs are still in `mongoengine.counters`.  

## Improvements 
* Authentication and Authorization should be added. JSON web tokens are a good candidate.
* API Rate limiting and caching should be added. 
* Instead of specifying configuration values at two places, that is, configuration files and ``Makefile``, there
 should be a script which reads the data from configuration file and use it to run the targets, for example, using
  non-default port numbers in ``make mongodb-offline``
* Naming can be improved
* Currently, we use incrementally increasing integers as primary key for songs. This can be replaced with using
 ``ObjectIds`` as primary key, which contain creation date as part of ``ObjectId``. 
* HTTP responses can be improved to follow OpenAPI standard format. 
* Endpoints paths can be improved, for example, ``[POST] /songs/ratings?song_id=1`` can be 
``[Patch] /songs/<song_id>/rating`` with new rating provided in payload.  
* ``[POST] /songs/ratings`` can be extended to include support for updating ratings to a batch of songs, instead of
 rating a single song. This is an open question.
* Support `created_at` filter with pagination.
* More end-to-end tests should be added.

## Developer notes. 
*  In case unit tests are added, they should be added to [tests/unit](https://github.com/hafeezibbad/music_app/tree/master/tests/unit) folder and run using ``make test`` 
 target.
* It is possible that end-to-end tests fail due to existing records in database, which result in ``409 Conflict
`` when we try to add songs for given test case. In that case, please remove all existing records from **test** 
database by running ``make clean-db``. This command will remove all records from ``SongRecord`` collection in
 ``mongoDB``. **Please run this command with care, and do not run it against production-like environment.**
* You can mark any test using ``@pytest.mark.<custom_marker>`` decorator and then run specifically marked tests as
 ``TEST_TAG=<custom_marker> make e2e-test`` 
* All DateTime values coming from API are in UTC format. Clients need to return it to specified time format. 
* In every song (document in database), we have a ``version`` field which is incremented every time the record is
 modified. This field is used to support ``If-(None-)Match`` header support. 
* After making code changes, we can run code-styling checks as

```bash
$ make analyze-code
```

This scheme uses [pylint](https://pypi.org/project/pylint/) and [pycodestyle](https://pypi.org/project/pycodestyle/) 
guidelines to check code styling and formatting issues. 
The default configuration for pylint checks can be overridden by modifying [pylint-configuration file](https://github.com/hafeezibbad/music_app/blob/master/configs/pylint/pylint.cfg)

### Common Error codes
* ``400 Bad request``, if the data provided in requests is invalid. 
* ``404 Not Found``, if not song is found with specified song ID
* ``503 Internal Server Error``, if client request was not processed successfully.

## Bonus endpoints
During development, some additional endpoints have been created.
#### [GET] /api/v1/songs/<song_id>
Returns the data for a song with specified ``songs_id``
```curl
curl --location --request GET 'http://localhost:3500/api/v1/songs/1' \
--header 'Content-Type: application/json'
```
```json
{
    "artist": "The Yousicians",
    "title": "Lycanthropic Metamorphosis",
    "difficulty": 14.6,
    "level": 13,
    "rating": [
        2,
        1,
        3,
        4,
        5
    ],
    "released": "2016-10-26",
    "version": 5,
    "song_id": 1,
    "created_at": "2020-07-09T11:30:58.185000",
    "last_modified_at": "2020-07-09T12:26:19.500000"
}
```
**Errors**: Returns ``412`` if the specified version in ``If-None-Match`` header is out-dated.

#### [POST] /api/v1/songs/
Creates a new song record in database

```curl
curl --location --request POST 'http://localhost:3500/api/v1/songs/' \
--header 'Content-Type: application/json' \
--data-raw '{"artist": "My Test Song","title": "my babysitting2","difficulty": 7,"level":6,"released": "2016-07-01"}'
```
```json
{
    "artist": "My Test Song",
    "title": "my babysitting2",
    "difficulty": 7.0,
    "level": 6,
    "rating": [],
    "released": "2016-07-01",
    "version": 0,
    "song_id": 14,
    "created_at": "2020-07-09T09:48:42.508608",
    "last_modified_at": "2020-07-09T09:48:42.508611"
}
```
#### [PATCH] /api/v1/songs/<song_id>
Updates an existing songs record
```bash
curl --location --request PATCH 'http://localhost:3500/api/v1/songs/14' \
--header 'Content-Type: application/json' \
--data-raw '{
    "artist": "My Test Song modified",
    "title": "modified title"
}'
```

```json
{
    "artist": "My Test Song modified",
    "title": "modified title",
    "difficulty": 7.0,
    "level": 6,
    "rating": [],
    "released": "2016-07-01",
    "version": 1,
    "song_id": 14,
    "created_at": "2020-07-09T09:48:42.508000",
    "last_modified_at": "2020-07-09T09:49:51.757000"
}
```
#### [DELETE] /api/v1/songs/<song_id>
Deletes an existing song record
```curl
curl --location --request DELETE 'http://localhost:3500/api/v1/songs/13'
```
Returns ``204 No Content``

#### [POST] /api/v1/songs/<uploads>
Batch upload multiple songs in the database. 
```bash
curl --location --request POST 'http://localhost:3500/api/v1/songs/uploads' \
--header 'Content-Type: application/json' \
--data-raw '{
    "songs": [
        {
            "artist": "The Yousicians",
            "title": "Lycanthropic Metamorphosis",
            "difficulty": 14.6,
            "level": 13,
            "released": "2016-10-26"
        },
        {
            "artist": "The Yousicians",
            "title": "A New Kennel",
            "difficulty": 9.1,
            "level": 9,
            "released": "2010-02-03"
        },
        {
            "artist": "Mr Fastfinger",
            "title": "Awaki-Waki",
            "difficulty": 15,
            "level": 13,
            "released": "2012-05-11"
        },
        {
            "artist": "The Yousicians",
            "title": "You'\''ve Got The Power",
            "difficulty": 13.22,
            "level": 13,
            "released": "2014-12-20"
        },
        {
            "artist": "The Yousicians",
            "title": "Wishing In The Night",
            "difficulty": 10.98,
            "level": 9,
            "released": "2016-01-01"
        },
        {
            "artist": "The Yousicians",
            "title": "Opa Opa Ta Bouzoukia",
            "difficulty": 14.66,
            "level": 13,
            "released": "2013-04-27"
        },
        {
            "artist": "The Yousicians",
            "title": "Greasy Fingers - boss level",
            "difficulty": 2,
            "level": 3,
            "released": "2016-03-01"
        },
        {
            "artist": "The Yousicians",
            "title": "Alabama Sunrise",
            "difficulty": 5,
            "level": 6,
            "released": "2016-04-01"
        },
        {
            "artist": "The Yousicians",
            "title": "Can'\''t Buy Me Skills",
            "difficulty": 9,
            "level": 9,
            "released": "2016-05-01"
        },
        {
            "artist": "The Yousicians",
            "title": "Vivaldi Allegro Mashup",
            "difficulty": 13,
            "level": 13,
            "released": "2016-06-01"
        },
        {
            "artist": "The Yousicians",
            "title": "Babysitting",
            "difficulty": 7,
            "level": 6,
            "released": "2016-07-01"
        }
    ]
}'
```

```json
{
    "newly_created_songs": 11,
    "new_song_ids": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11
    ],
    "existing_song_ids": []
}
```
Response returned if only all records are added successfully, but because we do not raise ``409 Conflict`` for
 duplicate song , we can retry using the same payload, and new (preivously unadded) songs will be added to the database.
In the response, ID for the song which exists already are provided in ``existing_song_ids`` field. 

#### [POST] /api/v1/songs/uploadfile
This endpoint takes a file where each line contains a valid json item containing song date. This file is similar
 to the example file ``songs.json`` was provided with this assignment.
```curl
curl --location --request POST 'http://localhost:3500/api/v1/songs/uploadfile' \
--form 'file=@/path/to/file/songs.json'
```
```json
{
    "newly_created_songs": 0,
    "new_song_ids": [],
    "existing_song_ids": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11
    ]
}
```
You can see that no new songs were added to database because the file contained same songs (as json) which were added
 in previous call to ``[POST] /api/v1/songs/<uploads>`` API call. 
#### [GET] /api/status
This endpoint can be used for monitoring purposes. For every request, it creates, reads, and deletes a new song in
 database to ensure that database connectivity is up, and service is up and running in expected manner.

```bash
curl --location --request GET 'http://localhost:3500/api/status'
```

```json
{
    "message": "Service is up",
    "status": "ok"
}
```
