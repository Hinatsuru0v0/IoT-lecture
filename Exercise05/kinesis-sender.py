import boto3
import time
import sys
import datetime
import pytz
import json
import pandas as pd
from pandas import read_csv


client = boto3.client('kinesis', region_name = 'ap-northeast-1',
                     aws_access_key_id = 'AKIA4OIB5R45V26BEIOO',
                     aws_secret_access_key = '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'
)
def load_data_from_csv(filename):
	rdelim = '\n'
	cdelim = ','
	data  = pd.read_csv(filename)
	return data

def send_data_to_csv(filename, data):
	data.to_csv(filename)
	

i = 0
a = 'a'
data = load_data_from_csv('./cdot-old.csv')
datasorted = data.sort_values(by='timestamp')  #[0:1000]

def extract_all(row):
	key  = row['sensor']+'_'+row['parameter']
	return {key : [str(pd.to_datetime(row['timestamp'])), row['value']]}	


d = datasorted.apply(extract_all, axis=1)
print('d has length =%d'%len(d))
print(d[0:10])

def sendtoKinesis(row):
	data = json.dumps(row)
	#print data
	resp = client.put_record(
	    StreamName='cloudbook2',
	    Data= bytearray(data, 'utf8'),
	    PartitionKey = 'a',
	)
	#time.sleep(0.01)
	return True


x = d.apply(sendtoKinesis)
