
# Mytodo Design

### Web API

#### URL for web pages


* /auth/login  
  - ```GET```: prompt for logging in  
  - ```POST [token]```: log user in with provided ```token```.

* /auth/register
  - ```GET```: prompt for getting a token  
  - ```POST []```: display the token that identifies the use.
  
* /  
  - ```login_required = True```  
  - Main display of all todos. It supports all kinds of views 
  of users' todos.
  
#### URL for resources
* /content/range  
  - ```login_required = True```  
  - ```GET [start_date, end_date]```:  
    return the user's todos from start date to end date in json format.

* /content/add_todo  
  - ```login_required = True```
  - ```POST [date, start_time, end_time, title, description]```:  
    Add one todo of the user to the database. ```start_time``` and 
    ```end_time``` are optional.

