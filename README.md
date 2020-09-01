## Panaruana President wants to know

This repo, shows how I learned Flask, to help the president gather some data about Paranuara.

### The Diagram

```console				

+--------+	         +----- Flask ------+     	      +------------------+
| client +- http: /v1 -->| Application      |                 |         Company  |   
+--------+               | /v1             (Storage) ---------+ MySQL   Person   |
	                 | config   	    |                 |                  |
		         +------------------+		      +------------------+
```	
### Install

The application runs inside a docker container, also the assumption is that you have Docker installed on you machine.
(This has been developed on an OSX machine, Windows is not an OS).

Run start.sh file : ./start.sh
This will build an image and run an instance of it, and exposes port 5000.


To load the database with sample data use the following commands:
```
curl -F 'file=@resources/people.json' http://127.0.0.1:5000/v1/upload/people
curl -F 'file=@resources/companies.json' http://127.0.0.1:5000/v1/upload/companies
``` 
### Quickstart

Now with data loaded, the api can be called, here are some templates, replace <..> with appropriate index numbers:

To see the employees of a company, identified by company_index:
```
curl -X GET http://127.0.0.1:5000/v1/company/<company_index>/employees
```
To see a person's diet, identified by person_index:
```
curl -X GET http://127.0.0.1:5000/v1/people/<person_index>/diet
```
To see common friends of person1_index, and person1_index: 
```
curl -X GET http://127.0.0.1:5000/v1/people/<person1_index>/common_friends_with?other_index=<person2_index>
```
To remove all data from database:

```
curl -X POST http://127.0.0.1:5000/v1/clear_data
```

### Clean up 
run the follwing command to identify the container id
```
docker ps --filter ancestor=para_api 
```

take the id shown for para_api image
```
docker stop <container id> 
```



 

 

