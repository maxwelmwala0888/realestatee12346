import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

# Import your database and model configurations
from backend.database import Base, SessionLocal, engine
from backend.models import Project, Comment

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. Mount Static Folders
# Ensure these folders exist so FastAPI can serve them
os.makedirs("uploads", exist_ok=True)
os.makedirs("frontend", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 2. Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Create necessary folders on startup
@app.on_event("startup")
def create_upload_folders():
    for folder in ["uploads/completed", "uploads/progress", "uploads/before", "uploads/after"]:
        os.makedirs(folder, exist_ok=True)

# 4. Serve index.html at root
@app.get("/", response_class=HTMLResponse)
async def read_index():
    file_path = os.path.join("frontend", "index.html")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>index.html not found in /frontend folder!</h1>")

# 5. Fixed Project Upload (Matches index.html exactly)
@app.post("/upload/project")
async def upload_project(
    title: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    section: str = Form(...), # 'completed' or 'progress'
    db: Session = Depends(get_db),
    file: UploadFile = File(...)
):
    try:
        # Create web-friendly path
        folder_path = f"uploads/{section}"
        os.makedirs(folder_path, exist_ok=True)
        
        filename = f"{datetime.now().timestamp()}_{file.filename}"
        save_path = os.path.join(folder_path, filename)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Use forward slashes for the database so the browser can read it
        db_image_path = f"/{folder_path}/{filename}".replace("\\", "/")

        new_project = Project(
            title=title,
            location=location,
            description=description,
            section=section,
            image_path=db_image_path
        )
        
        db.add(new_project)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # Save to Database
        # Note: Added start_date handling since your JS sends it
        new_project = Project(
            title=title,
            location=location,
            description=description,
            section=section,
            image_path=f"/{file_path.replace(os.sep, '/')}" # Ensures forward slashes for URL
        )
        
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        
        return {"status": "success", "image_path": new_project.image_path}
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 6. Fetch Projects by Section
@app.get("/projects/{section}")
async def get_projects(section: str, db: Session = Depends(get_db)):
    projects = db.query(Project).filter(Project.section == section).all()
    return projects

# 7. Comment Endpoints
@app.post("/upload/comment")
async def add_comment(
    name: str = Form(...),
    email: str = Form(...),
    comment: str = Form(...),
    db: Session = Depends(get_db)
):
    new_comment = Comment(name=name, email=email, comment=comment)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"status": "success", "id": new_comment.id}

@app.get("/comments")
async def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).order_by(Comment.id.desc()).all()


