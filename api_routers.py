from fastapi import APIRouter, HTTPException, status
from db_dependencies import Categories, Goals, Records, Users, CategoryBase, GoalBase, RecordBase, UserBase, db_dependency
from uuid import UUID, uuid4
from datetime import date, datetime
from sqlalchemy import select, join, outerjoin

categories_router = APIRouter(prefix='/categories', tags=['Categories'])
goals_router = APIRouter(prefix='/goals', tags=['Goals'])
records_router = APIRouter(prefix='/records', tags=['Records'])
users_router  = APIRouter(prefix='/users', tags=['Users'])

#NEW ENDPOINTS FOR EACH TABLE
#-->refactor routers so that they use id's instead of titles
#-->in each POST endpoint, a uuid4 is made (like in records)
#-->GET USER INFO, returns all rows in given table with user_id parameter

#-->records table: GET USER endpoint FIX DATE ISSUE

# categories router
@categories_router.post('/', status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryBase, db: db_dependency):
    if db.query(Categories).filter(Categories.category == category.category, Categories.username == category.username).first() is not None:
        raise HTTPException(status_code=409, detail='Category Already Exists for User')
    db_category = Categories(**category.model_dump())
    db_category.category_id = uuid4()
    db.add(db_category)
    db.commit()

@categories_router.get('/', status_code=status.HTTP_200_OK)
def read_categories(db: db_dependency):
    categories = db.query(Categories).all()
    if len(categories) == 0:
        raise HTTPException(status_code=404, detail='No Categories Found')
    return categories
    
@categories_router.get('/{category_id}', status_code=status.HTTP_200_OK)
def read_category(category_id: UUID, db: db_dependency):
    cat = db.query(Categories).filter(Categories.category_id == category_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    return cat

@categories_router.get('/user/{username}', status_code=status.HTTP_200_OK)
def read_user_categories(username: str, db: db_dependency):
    cats = db.query(Categories).filter(Categories.username == username).all()
    if len(cats) == 0:
        raise HTTPException(status_code=404, detail='No Categories Found')
    return cats

@categories_router.delete('/', status_code=status.HTTP_200_OK)
def delete_categories(db: db_dependency):
    if len(db.query(Categories).all()) == 0:
        raise HTTPException(status_code=404, detail='No Categories Found')
    db.query(Categories).delete()
    db.commit()

@categories_router.delete('/{category_id}', status_code=status.HTTP_200_OK)
def delete_category(category_id: UUID, db: db_dependency):
    cat = db.query(Categories).filter(Categories.category_id == category_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    db.delete(cat)
    db.commit()

@categories_router.put('/{category_id}', status_code=status.HTTP_200_OK)
def update_category(category_id: UUID, cat_update: CategoryBase, db: db_dependency):
    cat = db.query(Categories).filter(Categories.category_id == category_id)
    if cat.first() is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    cat.update({'category_id': category_id, 'category': cat_update.category, 'income_cat': cat_update.income_cat, 'username': cat.first().username})
    db.commit()

#goals router
@goals_router.post('/', status_code=status.HTTP_201_CREATED)
def create_goal(goal: GoalBase, db: db_dependency):
    if db.query(Goals).filter(Goals.title == goal.title, Goals.username == goal.username).first() is not None:
        raise HTTPException(status_code=409, detail='Savings Goal Already Exists for User')
    db_goal = Goals(**goal.model_dump())
    db_goal.goal_id = uuid4()
    db.add(db_goal)
    db.commit()

@goals_router.get('/', status_code=status.HTTP_200_OK)
def read_goals(db: db_dependency):
    goals = db.query(Goals).all()
    if len(goals) == 0:
        raise HTTPException(status_code=404, detail='No Goals Found')
    return goals

@goals_router.get('/{goal_id}', status_code=status.HTTP_200_OK)
def read_goal(goal_id: UUID, db: db_dependency):
    goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()
    if goal is None:
        raise HTTPException(status_code=404, detail='Goal Not Found')
    return goal

@goals_router.get('/user/{username}', status_code=status.HTTP_200_OK)
def read_user_goals(username: str, db: db_dependency):
    goals = db.query(Goals).filter(Goals.username == username).all()
    if len(goals) == 0:
        raise HTTPException(status_code=404, detail='No Goals Found')
    return goals

@goals_router.delete('/', status_code=status.HTTP_200_OK)
def delete_goals(db: db_dependency):
    if len(db.query(Goals).all()) == 0:
        raise HTTPException(status_code=404, detail='No Goals Found')
    db.query(Goals).delete()
    db.commit()

@goals_router.delete('/{goal_id}', status_code=status.HTTP_200_OK)
def delete_goal(goal_id: UUID, db: db_dependency):
    goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()
    if goal is None:
        raise HTTPException(status_code=404, detail='Goal Not Found')
    db.delete(goal)
    db.commit()

@goals_router.put('/{goal_id}', status_code=status.HTTP_200_OK)
def update_goal(goal_id: UUID, goal_update: GoalBase, db: db_dependency):
    goal = db.query(Goals).filter(Goals.goal_id == goal_id)
    if goal.first() is None:
        raise HTTPException(status_code=404, detail='Goal Not Found')
    goal.update({'goal_id': goal_id, 'title': goal_update.title, 'amount': goal_update.amount, 'priority': goal_update.priority, 'username': goal.first().username})
    db.commit()

#records router
@records_router.post('/', status_code=status.HTTP_201_CREATED)
def create_record(record: RecordBase, db: db_dependency):
    db_record = Records(**record.model_dump())
    db_record.record_id = uuid4()
    db_record.date = date.today()
    db.add(db_record)
    db.commit()

@records_router.get('/', status_code=status.HTTP_200_OK)
def read_records(db: db_dependency):
    records = db.query(Records).all()
    if len(records) == 0:
        raise HTTPException(status_code=404, detail='No Records Found')
    return records

@records_router.get('/{record_id}', status_code=status.HTTP_200_OK)
def read_record(record_id: UUID, db: db_dependency):
    rec = db.query(Records).filter(Records.record_id == record_id).first()
    if rec is None:
        raise HTTPException(status_code=404, detail='Record Not Found')
    return rec

@records_router.get('/user/{username}', status_code=status.HTTP_200_OK)
def read_user_records(username: str, db: db_dependency):
    recs = db.query(Records).join(Categories).filter(Categories.username == username).all()
    if len(recs) == 0:
        raise HTTPException(status_code=404, detail='No Records Found')
    return recs

@records_router.delete('/', status_code=status.HTTP_200_OK)
def delete_records(db: db_dependency):
    if len(db.query(Records).all()) == 0:
        raise HTTPException(status_code=404, detail='No Records Found')
    db.query(Records).delete()
    db.commit()

@records_router.delete('/{record_id}', status_code=status.HTTP_200_OK)
def delete_record(record_id: UUID, db: db_dependency):
    rec = db.query(Records).filter(Records.record_id == record_id).first()
    if rec is None:
        raise HTTPException(status_code=404, detail='Record Not Found')
    db.delete(rec)
    db.commit()

@records_router.put('/{record_id}', status_code=status.HTTP_200_OK)
def update_record(record_id: UUID, rec_update: RecordBase, db: db_dependency):
    rec = db.query(Records).filter(Records.record_id == record_id)
    if rec.first() is None:
        raise HTTPException(status_code=404, detail='Record Not Found')
    rec.update({'record_id': record_id, 'date': datetime.strptime(rec_update.date, '%Y-%m-%d').date(), 'category_id': rec.first().category_id, 'description': rec_update.description, 'amount': rec_update.amount})
    db.commit()

#users router
@users_router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, db: db_dependency):
    db_user = Users(**user.model_dump())
    db.add(db_user)
    db.commit()

@users_router.get('/', status_code=status.HTTP_200_OK)
def get_users(db: db_dependency):
    users = db.query(Users).all()
    if len(users) == 0:
        raise HTTPException(status_code=404, detail='No Users Found')
    return users

@users_router.get('/{username}', status_code=status.HTTP_200_OK)
def get_user(username: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return user

@users_router.delete('/', status_code=status.HTTP_200_OK)
def delete_users(db: db_dependency):
    if len(db.query(Users).all()) == 0:
        raise HTTPException(status_code=404, detail='No Users Found')
    db.query(Users).delete()
    db.commit()

@users_router.delete('/{username}', status_code=status.HTTP_200_OK)
def delete_user(username: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    db.delete(user)
    db.commit()

@users_router.put('/{username}', status_code=status.HTTP_200_OK)
def update_user(username: str, user_update: UserBase, db: db_dependency):
    user = db.query(Users).filter(Users.username == username)
    if user.first() is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    user.update({'username': user_update.username, 'password': user_update.password, 'first_name': user_update.first_name, 'last_name': user_update.last_name})
    db.commit()