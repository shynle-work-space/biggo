from instantiation import file_access
from modules.img_process import compress_img
from instantiation import app_log
from microgo.errors import Error

def upload_controller(owner_id:str, request):
    f = request.files.get('data')
    if f is None:
        return Error('fs_error', 'Upload file is missing')
    fs_id = file_access.create_fs(owner_id=owner_id, f=f, filename=f.filename)
    if isinstance(fs_id, Error):
        app_log('Error upload file', 'error', fs_id.code)
        return fs_id
    app_log(f'Begin process `{fs_id}`', 'info', 'img process')
    process_result = compress_img(fs_id, owner_id)
    if isinstance(process_result, Error):
        app_log(f'Fail to process `{fs_id}`', 'info', 'img process')
    app_log(f'Complete processing `{fs_id}`', 'info', 'img process')
    # task_producer.dispatch_img_task(fs_id=fs_id, owner_id=owner_id)
    return process_result