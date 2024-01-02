from dataclasses import dataclass
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from gridfs import GridFS
from bson import ObjectId

from typing import TypedDict
from werkzeug.datastructures import FileStorage

from modules.config import config
from modules.errors import Error

class Metadict(TypedDict):
    id: str
    filename: str
    tag: str
    original: str | None
    uploadDate: str


@dataclass
class FileAccess:

    def __post_init__(self):
        username = config.get('access_usr')
        pwd = config.get('access_pwd')

        mongo_host = config.get('mongo_host')
        mongo_port = config.get('mongo_port')

        try:
            print('Connect to MongoDB ...') 
            client = MongoClient(f'mongodb://{username}:{pwd}@{mongo_host}:{mongo_port}?authSource=admin', serverSelectionTimeoutMS=5000)
            self.db = client['image_records']
            self.fs = GridFS(self.db)
        except ConnectionFailure:
            print('Cannot connect to MongoDB, closing server ...')
            exit()



    def create_fs(self, owner_id: str, f: bytes | FileStorage, filename:str, **kwargs):
        try:
            fs_id = self.fs.put(f, owner_id=owner_id, filename=filename, **kwargs)
            return str(fs_id)
        except Exception as e:
            # log(f'Error from create_fs: \n{str(e)}', level='critical', tag='file_access error')
            return Error('fs_error', 'Cannot upload file to MongoDB')


    def read_fs(self, fs_id:str):
        """
        Returns filename and bytes array of a gridfs
        """
        try:
            f = self.fs.get(ObjectId(fs_id))
            return f.filename, f.read()
        except Exception as e:
            # log(f'Error from read_fs: \n{str(e)}', level='critical', tag='file_access error')
            return Error('fs_error', 'File does not existed')


    def delete_fs(self, fs_id:str):
        try:
            self.fs.delete(ObjectId(fs_id))
        except Exception as e:
            # log(f'Error from delete_fs: \n{str(e)}', level='critical', tag='file_access error')
            return Error('fs_error', 'Cannot delete file')


    def retrieve_file_metadata(self, fs_id:str):
        """
        Meta data cannot be access through gridfs Object,
        but through physical `fs.files` collection in MongoDB
        """
        fs_files = self.db.get_collection('fs.files')
        metadata = fs_files.find_one({"_id": ObjectId(fs_id)})
        return metadata


    def filter_fs(self, by:str, value:str):
        fs_files = self.db.get_collection('fs.files')
        metadata = fs_files.find({by: value})
        return metadata

    def list_imgs(self, owner_id: str):
        metadict:list[Metadict] = []
        for i in self.filter_fs('owner_id', owner_id):
            format_string = "%H:%M on %d/%m/%Y"
            metadict.append({
                'id': str(i.get('_id')),
                'filename': i.get('filename'),
                'tag': i.get('tag'),
                'uploadDate': datetime.strftime(i.get('uploadDate'), format_string),
                'original': i.get('original')
                })
        return metadict
    
    