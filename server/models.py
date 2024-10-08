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

    # Add validators
    @validates('name')
    def checking_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty ")
        naming = Author.query.filter_by(name=name).first()
        if naming and naming!= self:
            raise ValueError("Author Name must be new and unique")
        return name
    
    @validates('phone_number')
    def checking_phone(self,key,phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('The length of the phone number should be 10 ')

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

    # Add validators  
    @validates('title')
    def checking_posts(self, key, title):
        if not title:
            raise ValueError('Title must be present')
        clickbait = ["Won't Believe", "Secret","Top", "Guess"]
        if not any(word in title for word in clickbait):
            raise ValueError("Post title must contain one of the following:\n > 'Won't Believe', \n >'Secret', \n >'Top', \n >'Guess'")
        return title
    
    @validates('content')
    def checking_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be more than 250 characters')
        return content
    
    @validates('summary')
    def checking_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be less than or equal to 250 characters')
        return summary
    @validates('category')
    def checking_category(self, key, category):
        if category not in ['Fiction' , 'Non-Fiction']:
            raise ValueError("Category must only have a fiction or non-fiction option")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
