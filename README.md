# get started
1. with pipenv 
$ `python3.9 -m  pipenv install -r requirements.txt --skip-lock`
1. or with venv
$ `python3.9 -m pip install -r requirements.txt`



# api description
 - queries
    - 'fieldname__relationalField'
    - 'fieldname__gte=' ,'__in=', '__startwith=', ...etc
    - 'fieldname=' 
    - you also can add '?earliest=true' or '&latest=true', for the objects with date_created field
The end points that are not documeted in swagger.

## endpoints
1. `/patients/billings/`

    * **note**: patients will be renamed to manage_patients
    
    * you will need only **GET** **PUT**,
    * You wont need **DELTE** becuase this data will be immutable
    * You wont need **POST** because billes data will be created automaticly after a user request a servce.

1. `/alerts/` "convential I should name it notifcations"
    
    - **onmessage**
    ```
    
    ```
    
    - **send**
    ```
    {target:'events', id:1, is_seen:true}
    ```
    
1.  `/statistics/`
    
    - quick example "http://vytrac/statistics/?column__name=oxgyn&&field_value__lt=80"
    here you will get only the users with a history of oxygen level that reached under 80
    - quick example2 "http://vytrac/statistics/?column__name=oxgyn&&field_value__lt=80&date_created__gt=2021-06-09"
    now instead of getting all the users with a history of low oxygen, will get only the users that have currently or last measurement bellow 80
    - quick example3 "http://vytrac/statistics/?column__name=oxgyn&cal=min&number=10"
    you will get the 10 peaks of oxygen values
    - quick example4 "http://vytrac/statistics/?column__name=see_alerts&cal=duration"
    You will get how long the user spend before seeing each alert
    - Logic: calculate the time spent to change the value of the field `is_seen` from `false` to `true`
    - **GET** headers={}
    - the list view that look like the following as been sacrificed for the sake of aggregation and flexibility
        ```
            [{
                "name": "blood pressure",
                "user": 1,
                "column": [{
                "field_value": "22",
                "name": "ccc",
                "action": "added",
                "seen_by": [1],
                "date_created": "2021-06-09T10:42:41.458057Z"
                }, {
                "field_value": "44",
                "name": "ddd",
                "action": "added",
                "seen_by": [],
                "date_created": "2021-06-09T10:42:56.582589Z"
                }]
                }, {
                "name": "oxgyn",
                "user": 1,
                "column": [{
                "field_value": "11",
                "name": "",
                "action": "",
                "seen_by": [],
                "date_created": "2021-06-09T10:43:11.271641Z"
                }]
                }]
            ```
    - the aggrigaction friendly view
        ```
          [{
        "field_value": "22",
        "name": "ccc",
        "action": "added",
        "seen_by": [1],
        "date_created": "2021-06-09T10:42:41.458057Z",
        "column": {
        "name": "blood pressure",
        "user": 1
        }
        }, {
        "field_value": "44",
        "name": "ddd",
        "action": "added",
        "seen_by": [],
        "date_created": "2021-06-09T10:42:56.582589Z",
        "column": {
        "name": "blood pressure",
        "user": 1
        }
        }, {
        "field_value": "11",
        "name": "",
        "action": "",
        "seen_by": [],
        "date_created": "2021-06-09T10:43:11.271641Z",
        "column": {
        "name": "oxgyn",
        "user": 1
        }
        }]
        ```
    
    
1.  `'/trash/'`
    - all delete action will move the data to the trash,
    - **Note**: deleting items from the trash means they will go forever
    `$.get('/trash/')` will querie the trash content just like any qureis
    - `$.delete('/trash/?all=true')` wil empy the trash
        - id=<number> wil delete spsfic , Example: $.delete('/trash/?id=3')
        -  $.delete('/trash/?ids=<number>,<number>,') this will delete multi items
        


### for local use
```
$ python3.9 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver
# Note: postgres work only in the dockerized mode,
```


### potential conflicts.
```
# pyjwt
$ pipenv install djangorestframework  pipreqs  drf-yasg  aiohttp  aioredis  altgraph  ambition-django-timezone-field  aniso8601  anyjson  appdirs  astroid  async-timeout  attrs  auto-py-to-exe  autobahn  autopep8  boto3  botocore  bottle  bottle-websocket  certifi  cffi  channels-redis  chardet  click  colorama  constantly  coreapi  coreschema  coverage  cryptography  defusedxml  dill  distlib  dj-database-url  django-address  django-countries  django-crispy-forms  django-datetime-widget2  django-graphql-auth  django-graphql-jwt  django-heroku  django-language-field  django-model-utils  django-multiselectfield  django-pagination  django-rest-auth  django-rest-swagger  django-storages  django-timezone-field  django-widget-tweaks  djangochannelsrestframework  djangorestframework-jwt  djangorestframework-queryfields  djangorestframework-simplejwt  drf-renderer-xlsx  et-xmlfile  factory-boy  filelock  fleming  future  gevent  gevent-websocket  googletrans  graphene  graphene-django  graphql-core  graphql-relay  greenlet  gunicorn  h11  h2  hiredis  hpack  hstspreload  httpcore  httpx  hyperframe  hyperlink  idna  importlib-metadata  incremental  inflection  iniconfig  install  isort  itsdangerous  itypes  jmespath  lazy-object-proxy  macholib  mccabe  msgpack  msgpack-python  multidict  numpy  oauthlib  openapi-codec  openpyxl  pandas  path  pathlib  pep8  pipenv  pluggy  promise  psycopg2  pyasn1  pyasn1-modules  pycodestyle  pycparser  pyinstaller  pyinstaller-hooks-contrib  pyparsing  python-dateutil  python3-openid  pytz  redis  requests  requests-oauthlib  rfc3986  "ruamel.yaml"  "ruamel.yaml.clib"  s3transfer  selenium  service-identity  simplejson  singledispatch  six  sniffio  sqlparse  termcolor  text-unidecode  toml  txaio  typing-extensions  uritemplate  urllib3  virtualenv  virtualenv-clone  websockets  whichcraft  whitenoise  wrapt  yarl  zipp  "zope.event"  "zope.interface"  asgi_redis  Automat  Django-Abstract-Relations  Eel  Faker  Jinja2  Markdown  MarkupSafe  Pillow  PyJWT  pyOpenSSL  Rx  Twisted  Werkzeug
$ pipenv uninstall asgiref Django asgiref django-cors-headers django-safedelete channels daphne
$ pipenv lock --clear
$ pipenv lock --pre
$ pipenv install asgiref Django asgiref django-cors-headers django-safedelete channels daphne

```