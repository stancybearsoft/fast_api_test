Implementation of common API integration

The api has the following format: api.vehicle.com/v1/vehicle/get/<vin_code>,
 that returns information about vehicle by vin code, the link is not a valid address.

The following response is returned as json:{ "id": 1, "model_id": 1, "manufacturer_id": 1}


database settings in file settings.py

swagger doc

http://0.0.0.0:8000/docs

