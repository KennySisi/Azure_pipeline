import os
from fastapi import FastAPI
import pyodbc
# from azure.applicationinsights import applicationinsights

from azure.servicebus import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.identity import DefaultAzureCredential
import time

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
# from azure.mgmt.sql import SqlManagementClient

import redis
import redis.exceptions

credential = DefaultAzureCredential()

subscription_id = 'd90899a9-7716-4f55-88fe-22720fe4d18a'
resource_group = 'rg-spoke-kenny-myapp-ea'
server_name = 'sql-srv-kenny-all-ea'
database_name = 'sql-db-main-kenny-all-ea'


FULLY_QUALIFIED_NAMESPACE = "sb-main-myapp-prod-ea.servicebus.windows.net"
QUEUE_NAME = "test_queue_kenny"
TOPIC_NAME = "test_topics_kenny"
SUBSCRIPTION_NAME="test_subscription_kenny"

# sql_client = SqlManagementClient(credential, subscription_id)

# server = sql_client.servers.get(resource_group, server_name)
# connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{server.fully_qualified_domain_name};Database={database_name};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryMSI"

conn_str_system_assigned_iden = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sql-srv-kenny-all-ea.database.windows.net;"
    "DATABASE=sql-db-main-kenny-all-ea;"
    #"UID=zhangsi@kennyisagoodman.top;"
    #"PWD=Zs850605:);"
    "Authentication=ActiveDirectoryMsi;"
    #"Authentication=ActiveDirectoryPassword;"
)

conn_str_hardcode = "Driver={ODBC Driver 17 for SQL Server};Server=sql-srv-kenny-all-ea.database.windows.net;Database=sql-db-main-kenny-all-ea;UID=zhangsi@kennyisagoodman.top;PWD=Zs850605:);Authentication=ActiveDirectoryPassword;"

app = FastAPI()
# instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')
# if instrumentation_key:
#     azure_app_insights = applicationinsights(instrumentation_key=instrumentation_key)
#     azure_app_insights.init_app(app)

#Global redis cache
redis_access_key = "jlpWO3oECK3BOn5ZHP7BFbZUfSVyBLjc4AzCaC2HB5A=" #os.environ.get('REDIS_ACCESS_KEY') #None
redis_cache_with_password = None


@app.get("/Add/{number1}")
def add_two(number1):
    return {f"backend env: Your input is: {number1}"}

@app.get("/global/{global_name}")
def queryEnvString(global_name: str):
    return f"{global_name}"

@app.get("/env/{env_name}")
def queryEnvString(env_name: str):
    env_value = os.environ.get(env_name)
    return env_value

@app.get("/dbtest")
def queryDataBase():
    start_time = time.perf_counter()
    global redis_access_key
    global redis_cache_with_password
    if redis_cache_with_password is None:
        try:
            redis_cache_with_password = redis.StrictRedis(host="kenny.redis.cache.windows.net", 
                                                            port=6380, 
                                                            password=redis_access_key,
                                                            ssl=True)
        except redis.exceptions.RedisError: #redis.exceptions.ConnectionError:
            return "Timeout connecting to redis server!"
        
    if redis_cache_with_password is not None:
        redis_result = redis_cache_with_password.get("dbtest")
        if redis_result is not None:
            end_time = time.perf_counter() - start_time
            return "Result from redis cache: " + str(redis_result) + "consuming time(ms): " + str(end_time*1000)

    # @Microsoft.KeyVault(SecretUri=https://test-key-vault-ea.vault.azure.net/secrets/DB-Kenny-Conn-Str/63abcb49cb264a1a852cd192f4377ffd)
    connection_str_from_env = os.environ.get('DB_KENNY_CONN_STR')
    conn = pyodbc.connect(connection_str_from_env)
    curor = conn.cursor()
    curor.execute("select * from students") 
    rows = curor.fetchall()
    for row in rows:
        print(str(row))

    curor.close()
    conn.close()

    string_result = str(rows)
    if string_result is not None:
        if redis_cache_with_password is not None:
            redis_cache_with_password.set(f"dbtest", string_result, ex=300)

    end_time = time.perf_counter() - start_time
    return "Result from SQL Server Database: " + string_result + ", consuming time(ms): " + str(end_time*1000)

@app.get('/rediskey/{value}')
def setRedisKey(value:str):
    global redis_access_key
    redis_access_key = value
    if redis_access_key == "None":
        redis_access_key = None
    
    global redis_cache_with_password
    if redis_cache_with_password is not None:
        redis_cache_with_password.flushall()
        redis_cache_with_password = None
    
    try:
        redis_cache_with_password = redis.StrictRedis(host="kenny.redis.cache.windows.net", 
                                                        port=6380, 
                                                        password=redis_access_key,
                                                        ssl=True)
    except redis.exceptions.RedisError:
        return "Timeout connecting to redis server!"
    
    return "redis_cache_with_password reset with new access key: " + value

@app.get("/redis/clear")
def clearRedisCache():
    global redis_cache_with_password
    if redis_cache_with_password is not None:
        redis_cache_with_password.flushall()
        redis_cache_with_password = None
    
    return "redis cache cleared"

@app.get("/dbtest/ping")
def pingDB():
    global redis_access_key
    global redis_cache_with_password
    if redis_cache_with_password is None:
        try:
            redis_cache_with_password = redis.StrictRedis(host="kenny.redis.cache.windows.net", 
                                                            port=6380, 
                                                            password=redis_access_key,
                                                            ssl=True)
        except redis.exceptions.RedisError:
            return "Timeout connecting to redis server!"
        
    if redis_cache_with_password is not None:
        result_ping = redis_cache_with_password.ping()
        return "Ping returned : " + str(result_ping)

@app.get("/dbtest/{userID}")
def dbcontentWithCache(userID:str):
    start_time = time.perf_counter()
    global redis_access_key
    global redis_cache_with_password
    if redis_cache_with_password is None:
        try:
            redis_cache_with_password = redis.StrictRedis(host="kenny.redis.cache.windows.net", 
                                                            port=6380, 
                                                            password=redis_access_key,
                                                            ssl=True)
        except redis.exceptions.RedisError:
            return "Timeout connecting to redis server!"
        
    if redis_cache_with_password is not None:
        redis_result = redis_cache_with_password.get(f"dbtest/{userID}")
        if redis_result is not None:
            end_time = time.perf_counter() - start_time
            return "Result from redis cache: " + str(redis_result) + ", consuming time(ms): " + str(end_time*1000)


    connection_str_from_env = os.environ.get('DB_KENNY_CONN_STR')
    conn = pyodbc.connect(connection_str_from_env)
    curor = conn.cursor()
    curor.execute(f"select * from students where id = {userID}") 
    rows = curor.fetchall()
    for row in rows:
        print(str(row))

    curor.close()
    conn.close()

    string_result = str(rows)
    if string_result is not None:
        if redis_cache_with_password is not None:
            redis_cache_with_password.set(f"dbtest/{userID}", string_result, ex=300)

    end_time = time.perf_counter() - start_time
    return "Result from SQL Server Database: " + string_result + ", consuming time(ms): " + str(end_time*1000)


@app.get("/storagetest/{item_name}")
def queryStorageAccount(item_name: str):
    account_name = "stvmkennymyappea"
    container_name = "testcontainer"
    blob_name = item_name #"stex_initial_setup.ps1"
    #account_key="+cXhEDQmxmUafIp4qHtc7qkx7GdRwUXBrdec1bfJveOfyv5Wb6dLa9kAI/Y8uuBFXWBUjhZE4+PV+AStrzKApQ=="

    #AccountKey={account_key};
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};EndpointSuffix=core.windows.net"
    #connection_string = "DefaultEndpointsProtocol=https;AccountName=stvmkennymyappea;AccountKey=+cXhEDQmxmUafIp4qHtc7qkx7GdRwUXBrdec1bfJveOfyv5Wb6dLa9kAI/Y8uuBFXWBUjhZE4+PV+AStrzKApQ==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string, credential=credential) 
    #(f"https://{account_name}.blob.core.windows.net/", credential)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob() #container_client.list_blobs("stex_") #list_blob_names()
    content = blob_data.readall()
    return content

    # ret = ''
    # for blob_name in blob_list:
    #     ret = ret + blob_name + ";<br>"
    
    # return ret

@app.get("/")
def rootFunction():
    return "Hello 3, visitor new deploy triggered"


@app.get("/sender")
def serviceBusSender():
    servicebus_client = ServiceBusClient(fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE, credential=credential, logging_enable = True)
    #sender = servicevys_client.get_queue_sender(queue_name=const.TOPIC_NAME)
    sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
    count = 1
    output = "sent messages: "
    while count < 5:
        message = ServiceBusMessage(f"Sean {count} is a good man.")
        output += str(message)
        output += "    "
        print("sent message: " + str(message))
        sender.send_messages(message=message)
        time.sleep(1)
        count +=1

    servicebus_client.close()
    sender.close()
    credential.close()

    return output

@app.get("/receiver")
def serviceBusReceiver():
    servicebus_client = ServiceBusClient(fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
                                credential=credential,
                                logging_enable = True)
    #receiver = servicevys_client.get_queue_receiver(queue_name=const.QUEUE_NAME)

    receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME, 
                                                            subscription_name=SUBSCRIPTION_NAME)
    messages = receiver.receive_messages(max_message_count=5,max_wait_time=20)
    time.sleep(3)
    output = "Received messages: "
    for message in messages:
        print("Received message: " + str(message))
        output += str(message)
        output += "    "
        receiver.complete_message(message=message)

    servicebus_client.close()
    receiver.close()
    credential.close()
    # messages = asyncio.run(receive_messages_async())
    # print(str(messages))

    return output