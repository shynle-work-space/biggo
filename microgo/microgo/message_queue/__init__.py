from celery import Celery
from dataclasses import dataclass

def get_celery_worker_status(app):
    print('Checking connection to Celery worker and broker ...')
    inspection = app.control.inspect()
    if inspection.ping() is None:
        print('Error set up celery: Worker or Broker is not available')
        exit()

@dataclass
class TaskProducer:
    config: dict

    def __post_init__(self):
        username = self.config.get('ACCESS_USR')
        pwd = self.config.get('ACCESS_PWD')

        broker_host = self.config.get('BROKER_HOST')
        broker_port = self.config.get('BROKER_PORT')
        broker_vhost = self.config.get('BROKER_VHOST')

        backend_host = self.config.get('MONGO_HOST')
        backend_port = self.config.get('MONGO_PORT')

        BROKER_URL = f'amqp://{username}:{pwd}@{broker_host}:{broker_port}/{broker_vhost}'
        BACKEND_URL = f'mongodb://{username}:{pwd}@{backend_host}:{backend_port}?authSource=admin'

        self.task_producer = Celery('task_producer', broker=BROKER_URL, backend=BACKEND_URL)

        self.task_producer.conf.task_routes = {
            "process_img": {"exchange": "celery_images", "routing_key": "celery_images"},
        }
        get_celery_worker_status(self.task_producer)

    def dispatch_img_task(self, fs_id, owner_id):
        self.task_producer.send_task('img_process', 
                                     route_name='process_img',
                                     kwargs={"fs_id": fs_id, "owner_id": owner_id}, 
                                     )