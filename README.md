### Features

1. **Local Authentication** using email and password with [allauth](https://pypi.org/project/django-allauth/)
2. **Rest API** using [django rest framework](http://www.django-rest-framework.org/)
3. **Forgot Password**
4. Bootstrap4
5. Toast Notification
6. *Inline content editor in homepage*
7. Trash cycle
8. 

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
        

### potential conflicts.
```
$ pipenv uninstall asgiref pyjwt djangochannelsrestframework asgi-redis channels-redis django djangorestframework djangorestframework-simplejwt
$ pipenv install asgiref pyjwt
$ pipenv install  djangochannelsrestframework asgi-redis channels-redis django djangorestframework djangorestframework-simplejwt
```