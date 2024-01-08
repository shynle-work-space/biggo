from celery import Celery
# from PIL import Image
# from time import sleep
# from io import BytesIO
# from errors import Error
# from file_access import FileAccess
# from config import config

BROKER_URL = 'amqp://accessuser:accesspwd@localhost:5672/first-vhost'
BACKEND_URL = 'mongodb://accessuser:accesspwd@localhost:27017?authSource=admin'

task_publisher = Celery('task_publisher', broker=BROKER_URL, backend=BACKEND_URL)
task_publisher.conf.task_routes = {
    "ping": {"exchange": "celery_receiver_queue", "routing_key": "celery_receiver_queue"}
    }

def publish_task():
    print('Publishing task ...')
    id = task_publisher.send_task('ping', kwargs={"message": "hello world"}, route_name="ping")
    print(id)

if __name__ == '__main__':
    publish_task()

# # @task_consumer.task(name='img_process')
# # def img_process(fs_id:str, owner_id:str):
# #     print(f'Receiving {fs_id}')
# #     compress_img(fs_id, owner_id)
# #     print(f'{fs_id} process successfully')
# #     return fs_id


# if __name__ == '__main__':
#     args = ['worker', '-Q', 'celery_receiver_queue,celery_images', '--loglevel=INFO', '--concurrency=2']
#     task_consumer.worker_main(argv=args)