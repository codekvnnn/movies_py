from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

from flask_app.models import user

class Movie:
    db="movies_schema"
    
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.release_year = data['release_year']
        self.rewatch = data['rewatch']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        
# CREATE
    @classmethod
    def save_movie(cls,data):
        query= """
            INSERT INTO movies(name, genre, release_year, rewatch, user_id)
            VALUES (%(name)s,%(genre)s,%(release_year)s,%(rewatch)s,%(user_id)s);
        """
        return connectToMySQL(cls,data).query_db(query, data)
    
# READ
    @classmethod
    def get_all_movies(cls):
        query="""
        SELECT * FROM movies
        JOIN users ON movies.user_id = users.id;
        """
        
        results = connectToMySQL(cls.db).query_db(query)
        
        all_movies=[]
        
        
        for row in results:
            one_movie= cls(row)
            
            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            
            one_movie.owner= user.User(user_data)
            all_movies.append(one_movie)
        return all_movies
    
    @classmethod
    def get_one_movie(cls,data):
        query="""
            SELECT * FROM movies
            JOIN users ON movies.user_id=user.id
            WHERE movies.id = %(id)s;
        """
        
        results = connectToMySQL(cls.db).query_db(query, data)
        
        one_movie = cls(results[0])
        
        user_data={
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
        }
        one_movie.user = user.User(user_data)
            
        return one_movie
    
# UPDATE 
    @classmethod
    def update_movie(cls, data):
        query= """
        UPDATE movies
        SET name=%(name)s,gente=%(genre)s,release_year=%(release_year)s,rewatch=%(rewatch)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)
    

# DELETE
    @classmethod
    def delete_movie(cls, data):
        query="""
        DELETE FROM movies
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
# VALIDATION

    @staticmethod
    def validate_movie(data):
        is_valid=True
        
        if len(data['name']) ==0:
            is_valid=False
            flash('Name cannot be left empty', 'movie')
        elif len(data['genre']) < 3:
            is_valid=False
            flash('Genre should be filled', 'movie')
        if len(data['release_year']) ==0:
            is_valid=False
            flash('Year cant be empty', 'movie')
        if "rewatch" not in data:
            is_valid=False
            flash('Rewatch needs to be told', 'movie')
            return is_valid