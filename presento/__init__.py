from flask import Flask, request,session, g, redirect, url_for, \
    abort, render_template, flash
from mongoengine import *
from flask import json
import re

#configuration
MONGODB_HOST='localhost'
MONGODB_PORT = 27017
DATABASE = 'preso.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['MONGO_DB']='presento'
print "starting .."
app.secret_key = '\xa8m\x88\xd2\x97\xeb\xbdv\xbf2\xb7\xd1\x8f\x97\x96\x81]\xfd\xe3k\x89\xf6\xa7\xb6'



class User(Document):
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    
    
class Page(EmbeddedDocument):
    title = StringField()
    content = StringField()
    pagenum = IntField()
    def __str__(self):
        return 'content: %s pagenum: %d title: %s' % (self.content,self.pagenum,self.title)
    
    
class Presentation(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    pages = ListField(EmbeddedDocumentField(Page, required=False))
    tags = ListField(StringField(max_length=120, required=False))
    presid = IntField(required=True)
    current_page = IntField(required=False)
    def __str__(self):
        return 'Title:%s author:%s  id:%d currentPage:%d pages %s' % ( self.title, self.author,self.presid,self.current_page, self.pages)

class Meta(Document):
    presid = IntField()
    

@app.before_request
def before_request():
    #startup activities
  #  x = g.session
  #  if x  is None:
    connect(app.config['MONGO_DB'])
    #meta = Meta.objects.first()
    #print "presid is %d" meta.presid
  

@app.route('/newpreso')
def newpreso():
    #presentation.save()
    print "rendering preso.html"
    return render_template('preso.html')
    
@app.route('/meta', methods=['POST'])
def meta():
    print "***** in metta!!!!!!"
    title = request.form['title']
    tags = request.form['tags']
    #FIXME - always use admin for now
    u = User(first_name="sid", last_name="ram")
    u.save()
    # create the presentation
    p = Presentation(author=u, title = title)
    p.tags= p.tags.append(tags)   
    #increment the global id, and set the current presentation id to it
    Meta.objects.first().update(inc__presid=1)
    p.presid = Meta.objects.first().presid
    p.current_page = 0
    session['presid'] = p.presid
    print "mypresid is" + str(p.presid)
    p.save()
    return render_template('preso.html')

def done(pres):
    pages = pres.pages
    print "===pages===" + str(pres)
    pagelist = []
    for page in pages:
        pagelist.append([{"pagenum":page.pagenum, "content": page.content,"title":page.title}]);
   # print "===========json======="
    #print json.dumps(pagelist)
    #print "======================"
    #return json.dumps(pagelist)
    return render_template('deck.html', pages=pagelist, title=pres.title, first=pres.author.first_name, last=pres.author.last_name);

    
   
@app.route('/add_page',methods=['POST'])
def add_page():
    pres_id = session['presid']
    print "got presid" + str(pres_id)
     
    print request.form
    
    title = request.form['title']
    print title
    
    data = request.form['text']
    print data
    
    # fetch the presentation
    p = Presentation.objects(presid=pres_id).first()
    print "current page is %d" % (p.current_page)
    newpage = p.current_page+1
    p.update(inc__current_page=1)
    #add new page
    print "new page is %d" % (newpage)
    
    page = Page(content=data, pagenum=newpage,title=title)

    print "page is"
    print page
    print "end page"
    p.update(push__pages=page)
    print "before save: pres is" + str(p)
    p.save()
    
    p = Presentation.objects(presid=pres_id).first()
    
    print "pres is"
    print p
    print "end pres"
    
    if 'done' in request.form:
        print "done!"
        return done(p)
        
        
    elif 'newpage' in request.form:
        print "newpage"
        return render_template('preso.html')
    
 
 
   
    query= g.session.query(Presentation).filter(Presentation.id==pres_id)
    print query
    
    #presentation = query.filter(Presentation.id==pres_id).first()
    query.inc(Presentation.current_page,1).execute()
    print "++++"
    print query.one()
    
    #have to see if presenentation exists for this session
    # and retrieve it
    #page = Page(content=data,pagenum=1)
    #page.save()
    presentation = query.one()
    
    page = Page(content=data,pagenum=presentation.current_page)
    g.session.insert(page)
  #  if presentation.pages is not None:
   #     page = Page(content=data,pagenum=currentPage)
   #     g.session.insert(page)
   # else:
    #    page = Page(content=data,pagenum=currentPage)
     #   presentation.pages =page;
        # add a new row to page

        
    presentation.save()
    #session['pres_id'] = presentation._id
    #presentation.pages.save(pagenum=1, content=data)    
    print title
    print data
    #print presentation
    return render_template('preso.html')
    
@app.route('/')
def show_entries():
    print "in show entries"
    #sid = User(email='Sid@nayna.org', first_name='sid', last_name='ram', password='sid')
    #sid.save()
#   def show_entries():
#    cur = query_db('select creator,pagecount from preso')
#    print cur
    titles = []
    for p in Presentation.objects:
        #y = re.sub('"','', p.title)
        print p.title        
        titles.append([{"title":p.title, "presid":p.presid}])
    return render_template('show_presentations.html', titles=titles)
    
    
@app.route('/present')
def present():
    

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    #g.db.execute('insert into preso (creator,pagecount) values (?,?)',
                           # [request.form['title'], request.form['text']])
    #g.db.commit()
    flash('Added new Presentation')
    #return redirect(url_for('show_entries'))
    dict = {'title'}
    return render_template('create_presentation.html' )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['user'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


#if __name__ == '__main__':
#    print "*****"

#    app.run()
    
   
