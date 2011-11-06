from flaskext.mongoalchemy import MongoAlchemy

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password = StringField(max_length=50)
    
    
class Page(EmbeddedDocument):
    content = StringField()
    
    
class Presentation(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    pages = ListField(EmbeddedDocumentField(Page))

    
class Presentation(Document):
    use_dot_notation = True,
    __collection__ = 'presos'
    __database__ = 'presentations'
    structure = {
    'title' : unicode,
    'body'  : unicode
    
    }