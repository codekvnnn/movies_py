from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db="movies_schema"
    
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movies =[]
        
# create
    @classmethod
    def save(cls, data):
        query="""
            INSERT INTO users (first_name, last_name, email, password)
            VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,);
        """
        return connectToMySQL(cls.db).query_db(query, data)

# read
    @classmethod
    def get_user_by_email(cls,data):
        query="""
            SELECT * FROM users
            WHERE email=%(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)

        if len(results) < 1:
            return False
        
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query="""
            SELECT * FROM users
            WHERE id=%(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)

        return cls(results[0])
        
        
# update





# delete



# validations

    @staticmethod
    def validate_registration(data):
        is_valid=True
        one_user=User.get_user_by_email(data)
        
        if one_user:
            is_valid=False
            flash('Please log in', 'reg')
        if len(data['first_name']) ==0:
            is_valid=False
            flash('First Name cannot be left empty', 'reg')
        if len(data['last_name']) ==0:
            is_valid=False
            flash('Last Name cannot be left empty', 'reg')
        if len(data['email']) ==0:
            is_valid=False
            flash('email cannot be left empty', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid=False
            flash('Invalid email format', 'reg')
        if len(data['password']) ==0:
            is_valid=False
            flash('Password Name cannot be left empty', 'reg')
        if len(data['confirm_password']) ==0:
            is_valid=False
            flash('Confirm Password cannot be left empty', 'reg')
        if data['password'] != data['confirm_password']:
            is_valid=False
            flash('Password do not match', 'reg')
        return is_valid
            
            
    @staticmethod
    def validate_login(data):
        one_user=User.get_user_by_email(data)
        
        if not one_user:
            flash('Please register', 'login')
            return False
        if not bcrypt.check_password_hash(one_user.password. data['password']):
            flash('Invalid Credentials', 'login')
            return False
        return one_user
        
        