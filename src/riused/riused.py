import os
import sys
import json
import boto3
from prettytable import PrettyTable

def main():
    pass

def normalize(instance,ri):
    data = {
            "nano": 0.25,
            "micro": 0.5,
            "small": 1,
            "medium": 2,
            "large": 4,
            "xlarge": 8,
            "2xlarge": 16,
            "3xlarge": 24,
            "4xlarge": 32,
            "6xlarge": 48,
            "8xlarge": 64,
            "9xlarge": 72,
            "10xlarge": 80,
            "12xlarge": 96,
            "16xlarge": 128,
            "18xlarge": 144,
            "24xlarge": 192,
            "32xlarge": 256
            }

    result = data[instance] / data[ri]
    return result



# Fetches all instances
# Creates a list with key, values (name,type)
def fetchEC2():
    pag = boto3.client('ec2').get_paginator('describe_instances')

    results = []

    for page in pag.paginate():
        for res in page['Reservations']:
            for inst in res['Instances']:
                if inst['State']['Name'] == 'running':
                    instanceType = inst['InstanceType']
                    for tags in inst['Tags']:
                        if tags['Key'] == 'Name':
                            instanceName = tags['Value']
                    results.append({'name': instanceName, 'type': instanceType,'RI': False,'Cost': 'N/A'})
    print(len(results))
    return results


# Fetches all reserved instances
# Creates a list with key, valus (type, count)
def fetchReservedInstances():
    results = {}
    client = boto3.client('ec2')
    ri = client.describe_reserved_instances(Filters=[{'Name':'state','Values':['active']}])
    for r in ri['ReservedInstances']:
        if r['InstanceType'] in results:
            results[r['InstanceType']] += r['InstanceCount']
        else:
            results[r['InstanceType']] = r['InstanceCount']

    return results

def PrintTable(instances,reservedInstances):
    x = PrettyTable()
    x.field_names = ["Name","Type","Reserved","Credits Used"]

    for instance in instances:
        instFamily = instance['type'].split('.')[0]
        instSize = instance['type'].split('.')[1]
        for ri in reservedInstances:
            riFamily = ri.split('.')[0]
            riSize = ri.split('.')[1]
            cost = normalize(instSize,riSize)
            if instFamily == riFamily and instance['RI'] == False and reservedInstances[ri] > 0:
                reservedInstances[ri] -= cost
                instance['RI'] = True
                instance['test'] = ri
                instance['Cost'] = cost

        x.add_row([instance['name'],instance['type'],instance['RI'],instance['Cost']])

    x.sortby="Reserved"
    x.reversesort = True

    print(x)


reservedInstances = fetchReservedInstances()
reservedInstances2 = fetchReservedInstances()

allEC2s = fetchEC2()

print("------------------ EC2 ---------------------")
PrintTable(allEC2s,reservedInstances)

print("------------- Reservations -----------------")
y = PrettyTable()
y.field_names = ['Type','Credits','Total']

for ri in reservedInstances:
    y.add_row([ri,reservedInstances[ri],reservedInstances2[ri]])

print(y)
