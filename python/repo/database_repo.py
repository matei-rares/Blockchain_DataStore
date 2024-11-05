from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from CustomException import CustomException

# Daca devine enervant warningu ala
# import warnings
# warnings.filterwarnings("ignore")
file_path = 'repo/users.db'
engine = create_engine(f'sqlite:///{file_path}')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    company = Column(String)
    role = Column(String)  # 'ADMIN' / 'USER'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


#parola = "parola"
# session.add(User(id=2,username="admin", name="TestAdmin", password="a80b568a237f50391d2f1f97beaf99564e33d2e1c8a2e5cac21ceda701570312", company="TestSRL", role="ADMIN"))
# session.commit()
# verifica daca utilizatorul este deja
def add_user(username, name, password, company, role):
    user = session.query(User).filter_by(username=username).first()
    if user:
        raise CustomException("User with this username already exists!", 409)
    else:
        user = User(username=username, name=name, password=password, company=company, role=role)
        session.add(user)
        session.commit()
        return user


def get_user_by_id(id):
    user = session.query(User).filter_by(id=id).first()
    return user
    # if user:
    #     return user
    # raise CustomException("User not found!", 404)


def get_user_by_username(username):
    user = session.query(User).filter_by(username=username).first()
    return user
    #raise CustomException("User not found!", 404)


def get_all_users():
    users = session.query(User).filter_by(role="USER").all()
    return users


def delete_all():
    session.query(User).delete()
    session.commit()


def delete_by_ids(ids):
    for i in ids:
        session.query(User).filter_by(id=i).delete()
    session.commit()


def deactivate_user_by_id(id):
    user = get_user_by_id(id)
    user.is_active = False
    session.commit()
    return "ok"


def close_session():
    session.commit()
    session.close()


def update_password_by_username(username, new_password):
    user = get_user_by_username(username)
    user.password = new_password
    session.commit()
    return True


def update_password_by_id(id, new_password):
    user = get_user_by_id(id)
    user.password = new_password
    session.commit()
    return True
def update_is_active_by_id(id, is_active):
    user = get_user_by_id(id)
    user.is_active = is_active
    session.commit()
    return True

# add_user(username, name, password, company, role)
# delete_by_ids([2,3,4])
# get_user_by_id(4)
# user1 = User(username='Alice', password="30")
# user2 = User(username='Bob', password="25")
# session.add_all([user1, user2])
# session.commit()
