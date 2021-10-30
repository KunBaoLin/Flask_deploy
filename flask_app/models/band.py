from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from . import user

class Band:
    db = 'band_together'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.city = data['city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None #this is going to be where the user object will be put later


    @classmethod  #save query new band
    def save(cls,data):
        query = "INSERT INTO bands (name, genre, city, user_id) VALUES (%(name)s,%(genre)s,%(city)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod # get all from table bands
    def get_all(cls):
        query = "SELECT * FROM bands LEFT JOIN users on users.id = user_id;"
        #goal:  turn a list of dict into a list of objects with each band object associated with a user object
        results =  connectToMySQL(cls.db).query_db(query) #list of dict
        all_bands = [] # list of objects
        print(results)
        for row in results:
            # make a class instance of band
            this_band = cls(row)
            # make a data dict for the user
            user_info ={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            # make a user insance 
            this_user = user.User(user_info)
            # add that user object to the band attribute "user"
            this_band.user = this_user
            # append band into "all_bands"
            all_bands.append(this_band)
        return all_bands
    
    @classmethod  #get one band by id
    def get_one(cls,data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod  #update band
    def update(cls, data):
        query = "UPDATE bands SET name=%(name)s, genre=%(genre)s, city=%(city)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod  #delete bands
    def destroy(cls,data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod #get bands that relate to user
    def get_user_bands(cls,data):
        query = 'select * from bands left join users on bands.user_id = users.id where users.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        bands = []
        for band in results:
            bands.append(cls(band))
        return bands

    @staticmethod
    def validate_band(band):
        is_valid = True
        if len(band['name']) < 3:
            is_valid = False
            flash("Band Name must be at least 3 characters","band")
        if len(band['genre']) < 3:
            is_valid = False
            flash("Music Genre must be at least 3 characters","band")
        if len(band['city']) < 3:
            is_valid = False
            flash("Home City must be at least 3 characters","band")
        return is_valid
