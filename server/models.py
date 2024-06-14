from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_author_name(self, key, name):
        if name == None or len(name) == 0:
            raise ValueError('Name is required.')
        if Author.query.filter_by(name = f'{name}').first():
            raise ValueError('Name must be unique.')
        return name
    
    @validates('phone_number')
    def validate_author_phone_number(self, key, pnumber):
        if len(str(pnumber)) != 10:
            raise ValueError('Phone number must be 10 digits.')
        if pnumber.isnumeric() == False:
            raise ValueError('Phone number must contain only numbers')
        return pnumber

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_post_content(self, key, content):
        if content != None:
            if len(content) >= 250:
                return content
            else:
                raise ValueError('Content must be a minimum of 250 characters')
        else:
            raise ValueError('Content must be a minimum of 250 characters')
        
    @validates('summary')
    def validate_summary_content(self, key, summary):
        if summary != None:
            if len(summary) <= 250:
                return summary
            else:
                raise ValueError('Summary must not be more than 250 characters.')
        else:
            raise ValueError('Summary must not be more than 250 characters.')
        
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category must be either Fiction or Non-Fiction')
        return category
            
        
    @validates('title')
    def validate_title(slef, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
