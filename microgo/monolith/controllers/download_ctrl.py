from instantiation import file_access
from modules.errors import Error
from io import BytesIO


def download_controller(fs_id:str, access_user:str):
    read_result = file_access.read_fs(fs_id)
    if isinstance(read_result, Error):
        return read_result
    filename, file_bytes = read_result
    metadata = file_access.retrieve_file_metadata(fs_id)
    if metadata['owner_id'] != access_user:
        return Error('auth_error', 'User Unauthorized')
    imgIO = BytesIO(file_bytes)
    return filename, imgIO