from instantiation import file_access
from werkzeug.datastructures.file_storage import FileStorage


def upload_controller(owner_id:str, f: bytes | FileStorage):
    fs_id = file_access.create_fs(owner_id=owner_id, f=f, filename=f.filename)
    # task_producer.dispatch_img_task(fs_id=fs_id, owner_id=owner_id)
    return fs_id