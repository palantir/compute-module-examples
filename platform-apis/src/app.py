# - This file is the main entry point into your Compute Module
# - All functions defined in this file are callable using the function name as the 'queryType'
# - Each function must take 2 args, with the 2nd param being the actual "payload" of your function
# - Each function must return something serializable by `json.dumps`
#
# See the README page of this repo for more details

import logging
import requests
import os

from dataclasses import dataclass
from compute_modules.logging import get_logger
from compute_modules.annotations
from compute_modules.auth import oauth


# [SETUP REQUIRED] Share the dataset you want to read/write from with your service user inside Foundry
TOKEN = oauth("swirl.palantirfoundry.com", ["api:datasets-read", "api:datasets-write"])

# [SETUP REQUIRED] Add Foundry URL to your container's env vars
BASE_URL = f"https://{os.getenv('FOUNDRY_URL')}"

logger = get_logger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class UploadFileRequest:
    file_path: str
    file_content: str
    dataset_rid: str

@dataclass
class UploadFileResponse:
    status: int

@dataclass
class GetFileRequest:
    dataset_rid: str
    file_path: str

@dataclass
class GetFileResponse:
    status: int
    file_content: bytes


"""
Write a file to a dataset. 

https://www.palantir.com/docs/foundry/api/v2/datasets-v2-resources/files/upload-file/
"""
def upload_file(context, event: UploadFileRequest) -> UploadFileResponse:
    logger.info(f"Uploading file to {event.file_path}")
    url = f"{BASE_URL}/api/v2/datasets/{event.dataset_rid}/files/{event.file_path}/upload"
    response = requests.post(
        url,
        params={"transactionType": "APPEND", "branchName": "master"},
        headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/octet-stream"
        },
        data=event.file_content
    )
    return UploadFileResponse(status=response.status_code) 


"""
Read contents of a file written to a dataset. 

https://www.palantir.com/docs/foundry/api/v2/datasets-v2-resources/files/get-file-content/
"""
def get_file(context, event: GetFileRequest) -> GetFileResponse:
    logger.info(f"Getting file from {event.file_path}")
    url = f"{BASE_URL}/api/v2/datasets/{event.dataset_rid}/files/{event.file_path}/content"
    logger.info(url)
    dataset_response = requests.get(
        url,
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    return GetFileResponse(
        status=dataset_response.status_code,
        file_content=dataset_response.content
        )


# EXAMPLE USAGE:
# if __name__ == "__main__":
#     file_path = "myfilename.csv"
#     file_content = b"this is my file content"

#     UPLOAD YOUR FILE TO THE DATASET
#     upload_response = upload_file({}, UploadFileRequest(dataset_rid="ri.foundry.main.dataset.7eed06cf-3c86-4916-8237-09d17ae30f98", file_path=file_path, file_content=file_content))
#     assert(upload_response.status == 200)

#     READ FILE CONTENT FROM THE DATASET 
#     response = get_file({}, GetFileRequest(dataset_rid="ri.foundry.main.dataset.7eed06cf-3c86-4916-8237-09d17ae30f98", file_path=file_path))
#     assert(response.file_content == file_content)