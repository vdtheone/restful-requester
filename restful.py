#!/usr/bin/env python3
import requests
import argparse
import json
import csv

class RestfulClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}")
        return response

    def post_data(self, endpoint, data):
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        return response

    def process_request(self, method, endpoint, data=None, output=None):
        if method == 'get':
            response = self.get_data(endpoint)
        elif method == 'post':
            if data is None:
                print("Data is required for POST method.")
            try:
                response = self.post_data(endpoint, data)
            except json.JSONDecodeError:
                print("Invalid JSON format for data.")
        
        if not (200 <= response.status_code < 300):
            print(f"Error: Request failed with HTTP Status Code - {response.status_code}")

        self.handle_response(response, output)
        
        
    def handle_response(self, response, output):
        print(f"HTTP Status Code: {response.status_code}")

        if not response.ok:
            print(f"Error: {response.text}")
            exit(1)

        if output:
            self.save_output(response, output)
        else:
            print(json.dumps(response.json(), indent=2))



    def save_output(self, response, output):
        if output.endswith('.json'):
            with open(output, 'w') as json_file:
                json.dump(response.json(), json_file, indent=2)
        elif output.endswith('.csv'):
            data = response.json()
            if isinstance(data, list):

                keys = data[0].keys() if data else []

                with open(output, 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
            else:
                print("Invalid data format for CSV output.")
        else:
            print("Unsupported output format.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple CLI RESTful client for JSONPlaceholder")
    parser.add_argument('method', choices=['get', 'post'], help='Request method')
    parser.add_argument('endpoint', help='Request endpoint URI fragment')
    parser.add_argument('-d', '--data', type=json.loads, help='Data to send with the request (JSON format)')
    parser.add_argument('-o', '--output', help='Output to .json or .csv file (default: dump to stdout)')

    args = parser.parse_args()

    client = RestfulClient('https://jsonplaceholder.typicode.com')
    client.process_request(args.method, args.endpoint, args.data, args.output)   



# All requests with post data
    
# ./restful.py -h
# ./restful.py get /posts
# ./restful.py get /posts -o test.json
# ./restful.py get /posts -o test.csv
# ./restful.py get /posts/1
# ./restful.py post /posts --data '{"title": "Treesha Rocks!", "body": "It really really rocks.", "userId": 1}'
# ./restful.py post /posts -d '{"title": "Treesha Rocks!", "body": "It really really rocks.", "userId": 1}' -o test_all.json