/ufo_api/ - contains django api for classifier. logic handling post requests can be found in ufo_api/App/views.py

Running django api:

1. install requirements listed in Pipfile
2. cd ufo_api
3. python manage.py runserver
4. send POST requests to this route: /App/predict/ (must have trailing slash)

Requests must be json with the following form:

{
	"datetime": string,
	"duration": int or string
}

The values should adhere to standards listed below. These standards are in accordance with the given data set:

Datetime: String of the form "mm/mm/yyyy H:M", ex. "10/10/1949 20:30"
Duration: Duration in seconds, integer or string (ex. 2400 and "2400" are both accepted)
	
Sample request:

{
    "datetime": "10/10/1999 10:00",
    "duration": 3
}

Sample response:

{
    
    "shape": "round"

}
