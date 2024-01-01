from instantiation import file_access
from werkzeug.datastructures.file_storage import FileStorage
from img_process import compress_img
from instantiation import app_log
from errors import Error

def upload_controller(owner_id:str, f: bytes | FileStorage):
    fs_id = file_access.create_fs(owner_id=owner_id, f=f, filename=f.filename)
    app_log(f'Begin process `{fs_id}`', 'info', 'img process')
    process_result = compress_img(fs_id, owner_id)
    if isinstance(process_result, Error):
        app_log(f'Fail to process `{fs_id}`', 'info', 'img process')
    app_log(f'Complete processing `{fs_id}`', 'info', 'img process')


    # task_producer.dispatch_img_task(fs_id=fs_id, owner_id=owner_id)
    return process_result