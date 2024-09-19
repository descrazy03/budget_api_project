from fastapi import FastAPI, status
import db_dependencies
from db_setup import engine
import uvicorn
import api_routers

#initialize FastAPI application
app = FastAPI()

app.include_router(api_routers.categories_router)
app.include_router(api_routers.goals_router)
app.include_router(api_routers.records_router)
app.include_router(api_routers.users_router)

@app.get('/', tags=['Home'], status_code=status.HTTP_200_OK)
def home():
    return {'detail': 'success'}

db_dependencies.Base.metadata.create_all(bind=engine)
 

if __name__ == '__main__':
    pass
    #uvicorn.run('api_main:app', host='127.0.0.1', port=8000, reload=True)