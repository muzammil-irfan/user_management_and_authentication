from fastapi import FastAPI
from app.router.user import user_router
from app.router.student_router import student_router
from app.router.oauth_router import oauth_router
from app.router.auth_router import auth_router
from app.router.teacher import teacher_router
from app.database import create_db_and_tables
from typing import AsyncIterator

# lifespan function
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        create_db_and_tables()
        yield
    except Exception as e:
        print(f"Error during startup: {e}")

# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan, title="Panaversity User Management and Authentication", 
    version="0.0.1",
    prefix="/api/v1",
    servers=[
            {
                "url": "http://localhost:8000/", # ADD NGROK URL Here Before Creating GPT Action
                "description": "Development Server"
            },
            {
                "url": "http://api.panaversity.com/",
                "description": "Production Server"
            }
        ]
    ) 


@app.get("/", tags=["Root"])
def root():
    return {"message": "This is just an authentication service. Please visit http://localhost:8000/docs to see the API documentation."}

# Include routers
app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(teacher_router, prefix="/api/v1/teacher", tags=["Teacher"])
app.include_router(student_router, prefix="/api/v1/student", tags=["Student"])
app.include_router(oauth_router, prefix="/api/v1/oauth", tags=["OAuth"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
