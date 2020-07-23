import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from config import as_container_name,as_blob_name,as_account_key,ai_workspace,get_sas


def download(target_ws,dirPath,filename):
    block_blob_service = BlockBlobService(account_name=as_container_name,
                                          sas_token=get_sas())
    full_path_to_file2 = os.path.join(target_ws, filename)
    block_blob_service.get_blob_to_path(
        as_blob_name, ".\\"+dirPath+"\\"+filename,
        full_path_to_file2)

def updateSource(dirPath,source_file,filename):
    block_blob_service = BlockBlobService(
        account_name=as_container_name,
        sas_token=get_sas()
    )
    block_blob_service.create_blob_from_path(
        as_blob_name, ".\\"+dirPath+"\\"+filename,
        source_file)

def upload(dirPath,source_file,filename):
    block_blob_service = BlockBlobService(
        account_name=as_container_name,
        sas_token=get_sas()
    )
    block_blob_service.create_blob_from_path(
        as_blob_name, ".\\"+dirPath+"\\result\\"+filename,
        source_file)