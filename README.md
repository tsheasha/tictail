tictail
==============

## The TicTail Todo List [Deployed Version](http://tictail.herokuapp.com/)


## API Architecture:

This part was by far the most interesting part of the test, designing a RESTful API 
and its URLs is one of the most controversial topics in my opinion. However, 
I tried my best to produce an API that I feel comfortable with. 
I will explain the reasoning behind the architecture of each step. 
I have done a lot of discussions with myself regarding the architecture, 
however, these are too long to write down, so I will discuss them during or follow-up. 


* I used a separate url for the api, to maintain a scalable system that can 
accommodate several versions. 

* The choice of a separate url was not my top preference, however ideally, it would have been better to make the api
into a subdomain, so “api.tictail.herokuapp.com”  instead of “tictail.herokuapp.com/api/“. 
The reason I would prefer the latter is to balance the loads on the servers and dedicate server(s) for the web
service and serves(s) for the api service, however, due to the limitation of this programming test and that I
could not create a subdomain I chose the first way. In a real environment I would go for the sub-domain solution.

* URLs were maintained as RESTful as possible as can be seen in the API documentation below.

* I chose the option of specifying the response type and API version to be part of the HTTP Header instead of
being part of the url, I found the HTTP header option to be more elegant and RESTful.

* JSON responses are gzipped and the HTTP response Content-Encoding Header specifies this.

* Optional parameters for listing todos (limit, offset)


     I have worked my hardest into meaning the API as RESTful as possible, maintaining RESTful URLs along the way.

### API Documentation
List Todos
          
     GET /api/todos
          
Parameters
     
| Name        | Type           | Description  |
| ------------- |:-------------:|:-----|
| limit      | int      |   The number of todos to return, defaults to 50. |
| offset | int      |    The offset from the beginning of the list to start retrieving todos from. |
     
Response
     
```json
     {
       "todos": [
         {
           "completed": false, 
           "id": 1, 
           "order": 1, 
           "title": "Discuss report with John", 
           "user": "tsheasha"
         }, 
         {
           "completed": false, 
           "id": 4, 
           "order": 4, 
           "title": "Check gym hours", 
           "user": "tsheasha"
         }, 
         {
           "completed": true, 
           "id": 2, 
           "order": 2, 
           "title": "Get a haircut", 
           "user": "tsheasha"
         }, 
         {
           "completed": true, 
           "id": 3, 
           "order": 3, 
           "title": "Pay electricity bill", 
           "user": "tsheasha"
         }
       ]
     }
    
```
    HTTP/1.1 200

Get a single Todo item
          
     GET /api/todos/ID

Response
     
```json
     {
       "completed": false, 
       "id": 1, 
       "order": 1, 
       "title": "Discuss report with John", 
       "user": "tsheasha"
     }
  
```     
    HTTP/1.1 200

Create a new todo
     
     POST /api/todos
     
Parameters
     
| Name        | Type           | Description  |
| ------------- |:-------------:|:-----|
| title | string      |  The content of the todo item. |
          
Response

          HTTP/1.1 201
          
Change order of a todo item
     
     PUT /api/todos/ID
     
Response

          HTTP/1.1 204
          

The code is also documented so that the person who reads it does not suffer
