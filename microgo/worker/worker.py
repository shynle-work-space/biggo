from celery import Celery
from publisher import send_message
from os import environ

access_user = environ.get("ACCESS_USR")
access_pwd = environ.get("ACCESS_PWD")
rb_host = environ.get("RABBITMQ_HOST")
rb_port = environ.get("RABBITMQ_PORT")
rb_vhost = environ.get("RABBITMQ_VHOST")

mongo_host = environ.get("MONGO_HOST")
mongo_port = environ.get("MONGO_PORT")

# from PIL import Image
# from time import sleep
# from io import BytesIO
# from errors import Error
# from file_access import FileAccess
# from config import config

BROKER_URL = f'amqp://{access_user}:{access_pwd}@{rb_host}:{rb_port}/{rb_vhost}'
BACKEND_URL = f'mongodb://{access_user}:{access_pwd}@{mongo_host}:{mongo_port}?authSource=admin'

# file_access = FileAccess(config)
task_consumer = Celery('task_consumer', broker=BROKER_URL, backend=BACKEND_URL)

@task_consumer.task(name='ping', queue='celery_receiver_queue')
def ping(message:str):
    print(f'Worker receive message: {message}')
    if message == 'hello from golang':
        send_message(BROKER_URL, {'message': 'Ping success'})
    return message

# @task_consumer.task(name='img_process')
# def img_process(fs_id:str, owner_id:str):
#     print(f'Receiving {fs_id}')
#     compress_img(fs_id, owner_id)
#     print(f'{fs_id} process successfully')
#     return fs_id


if __name__ == '__main__':
    args = ['worker', '-Q', 'celery_receiver_queue,celery_images', '--loglevel=INFO', '--concurrency=2']
    task_consumer.worker_main(argv=args)