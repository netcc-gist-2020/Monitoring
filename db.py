from influxdb import InfluxDBClient
from datetime import datetime

class DB:
	def __init__(self):
		self.client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

	def create_table(self):
		self.client.create_database('example')

	def insert(self, key, exp, eye_dir):
		json_body = [
			{
				"measurement": "record",
				"tags": {
					"key": key,
				},
				# "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				"fields": {
					"expression": exp, 
					"eye_dir": eye_dir
				}
			}
		]
		return self.client.write_points(json_body)

	def query(self):
		return self.client.query("select * from record")

	def delete_all(self):
		self.client.query("delete from record")
