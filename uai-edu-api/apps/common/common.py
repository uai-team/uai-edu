import os
import shutil
from datetime import datetime
from fastapi import UploadFile, Depends, APIRouter
from utils.response import SuccessResponse


app = APIRouter()

@app.post("/upload_file_local", summary="上传文件")
async def upload_file_local(file_type: str, file: UploadFile):
    # Get file extension from uploaded file
    file_ext = os.path.splitext(file.filename)[1]
    time_now = datetime.now()
    
    # Generate unique filename using timestamp
    timestamp = time_now.strftime("%Y%m%d%H%M%S")
    file_name = f"{timestamp}{file_ext}"
    
    # Set upload directory based on file type
    upload_dir = f"static/uploads/{file_type}/{time_now.strftime('%Y-%m-%d')}"
    
    # Create upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)
    
    # Full path for saving the file
    file_path = os.path.join(upload_dir, file_name)
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Prepare data for database
    data = {
        "file_name": file_name,
        "file_path": file_path,
        "media_url": file_path.replace("static/uploads","/media/uploads")
    }

    return SuccessResponse(data)
