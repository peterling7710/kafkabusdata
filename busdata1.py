from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time

#READ COORDINATES FROM GEOJSON
input_file = open('./data/bus1.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

#KAFKA PRODUCER
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geoDataFinal']
producer = topic.get_sync_producer()

def generate_uuid():
    return uuid.uuid4()

#CONSTRUCT MESSAGE AND SEND TO KAFKA
def generate_checkpoint(coordinates):

    i = 0
    while i < len(coordinates):
        data = {}
        data['busline'] = '00001'
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)

        #IF REACHES LAST CHECKPOINT, START FROM BEGINNING
        i += 1

        if i == len(coordinates)-1:
            i = 0

generate_checkpoint(coordinates)

