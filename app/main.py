import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.core.config import *

app = FastAPI()


@app.get("/")
async def main():
    return {"message": "Hello World!"}


@app.get("/files")
async def views_bucket_files():

    try:
        response = s3.list_objects(Bucket=BUCKET_NAME)

        if "Contents" in response:

            file_names = [obj["Key"] for obj in response["Contents"]]
            return {"files": file_names}
        else:
            return {"message": "No files found in the bucket"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/files/upload")
async def upload_file_to_storage(file_path: str):

    if not os.path.exists(file_path):
        return {"message": "The file was not found"}

    try:
        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as file:
            s3.upload_fileobj(file, BUCKET_NAME, file_name)
        return {"message": f"The file {file_path} has been uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/download")
async def download_file_from_storage(file_path: str):

    try:
        file_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_path)
        temp_file_path = f"/tmp/{os.path.basename(file_path)}"

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_object["Body"].read())
        return FileResponse(temp_file_path, filename=os.path.basename(file_path))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/delete")
async def delete_file_from_storage(file_path: str):

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_path)
        return {"message": f"The file {file_path} has been deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
