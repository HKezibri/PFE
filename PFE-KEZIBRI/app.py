from flask import Flask, render_template, request,flash, redirect, url_for,json,jsonify,session
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId

app = Flask(__name__)
Bootstrap(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'EventManager',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = 'pfe-DUT-2021'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Document):
    meta = {'collection': 'Admin'}
    email = db.StringField(max_length=30)
    password = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class Users(UserMixin, db.Document):
    meta = {'collection': 'users'}
    last_name = db.StringField()
    first_name = db.StringField()
    username = db.StringField()
    phone = db.StringField()
    email = db.StringField(max_length=30)
    password = db.StringField()
    date_reservation = db.DateTimeField()
    etat_reservation = db.StringField()
    titre_evenn = db.StringField()

class MyForm(FlaskForm):
    last_name = StringField(u'Nom ', validators=[InputRequired()])
    first_name  = StringField(u'Prenom', validators=[InputRequired()])
    username  = StringField(u'username', validators=[InputRequired()])
    phone = StringField(u'Numero de telephone ', validators=[InputRequired()])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class RegFormuser(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class Events(db.Document):
    titre = db.StringField(required=True)
    categorie = db.StringField(required=True)
    courte_description = db.StringField(required=True)
    description = db.StringField(required=True)
    lieu = db.StringField(max_length=50, required=True)
    pub_date = db.DateTimeField(datetime.now)
    date_debut = db.StringField()
    date_fin = db.StringField()

class Category(db.Document):
    meta = {'collection': 'category'}
    titre = db.StringField(required=True)


class CommitteNational(db.Document):
    meta = {'collection': 'committescientifiqnational'}
    nom = db.StringField(required=True)
    universite = db.StringField(required=True)

class CommitteInternational(db.Document):
    meta = {'collection': 'committescientifiq-international'}
    nom = db.StringField(required=True)
    universite = db.StringField(required=True)

class Parametre(db.Document):
    meta = {'collection': 'parametre'}
    slide_title = db.StringField(required=True)
    slide_title2 = db.StringField(required=True)

class Speakers(db.Document):
    meta = {'collection': 'speakers'}
    profession = db.StringField(required=True)
    nom = db.StringField(required=True)
    uni = db.StringField(required=True)
    titre = db.StringField(required=True)

class EquipeOrganisation(db.Document):
    meta = {'collection': 'EquipeOrganisation'}
    nom = db.StringField(required=True)
    apropos = db.StringField(required=True)
    tache = db.StringField(required=True)

class DateImportante(db.Document):
    meta = {'collection': 'DateImportante'}
    date1 = db.StringField(required=True)
    date2 = db.StringField(required=True)
    date3 = db.StringField(required=True)

'''class Reservation(db.Document):
    meta = {'collection': 'reservation'}
    nbr_places = StringField()
    date_reservation = db.DateTimeField(datetime.now)
    etat_reservation = db.StringField(default='pas de confirmation')
    titre_evenn = db.StringField()
    userid = ReferenceField('Users')'''



#PARTIE ADMIN

@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(email = form.email.data,password=hashpass).save()
                login_user(hey)
                return redirect(url_for('dashboard'))
                
    return render_template('admin/register.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    flash("vous etes connecte","info")
                    return redirect(url_for('dashboard'))
                

    return render_template('admin/login.html', form=form)

@app.route('/admin/dashboard')
@login_required
def dashboard():
    title = 'Admin-Tableau de Bord'
    nbr_users = Users.objects().count()
    nbr_events = Events.objects().count()
    nbr_categs = Category.objects().count()
    nbr_csn = CommitteNational.objects().count()
    nbr_csi = CommitteInternational.objects().count()
    nbr_speaker = Speakers.objects().count()
    nbr_date = DateImportante.objects().count()
    nbr_eq = EquipeOrganisation.objects().count()
    return render_template('admin/dashboard.html', name=current_user.email,nbr_users=nbr_users,nbr_events=nbr_events,nbr_categs = nbr_categs ,nbr_csi=nbr_csi,nbr_csn=nbr_csn,nbr_date=nbr_date,nbr_speaker=nbr_speaker, nbr_eq= nbr_eq,title=title)

@app.route('/admin/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin/events')
@login_required
def query_records():
    title = "Gestion Evennement par l'admin"
    events = Events.objects.all()
    return render_template('admin/gestion_event.html', events=events,name=current_user.email,title=title)
'''  
@app.route('/admin/updateevents', methods=['POST'])
def updateevents():
    pk = request.form['pk']
    titrepost = request.form['txttitre']
    categoriepost= request.form['txtcategorie']
    courte_descriptionpost= request.form['txtcourte_description']
    descriptionpost= request.form['txtdescription']
    lieupost= request.form['txtlieu']
    date_debutpost= request.form['txtdate_debut']
    date_finpost= request.form['txtdate_fin']
    value = request.form['value']
    events_rs = Events.objects(id=pk).first()
    if not events_rs:
        return json.dumps({'error':'data not found'})
    else:
        if titrepost == 'titre':
            events_rs.update(titre=value)
        elif categoriepost == 'categorie':
            events_rs.update(categorie=value)
        elif courte_descriptionpost == 'courte_description':
            events_rs.update(courte_description=value)
        elif descriptionpost == 'description':
            events_rs.update(description=value)
        elif lieupost == 'lieu':
            events_rs.update(lieu=value)
        elif date_debutpost == 'date_debut':
            events_rs.update(date_debut=value) 

        elif date_finpost == 'date_fin':
            events_rs.update(date_fin=value)


    return json.dumps({'status':'OK'})

@app.route('/admin/edit-event/<oid>',methods=['GET', 'POST'])
def editev(oid):
    
    titrepost = request.form['txttitre']
    categoriepost= request.form['txtcategorie']
    courte_descriptionpost= request.form['txtcourte_description']
    descriptionpost= request.form['editordata']
    lieupost= request.form['txtlieu']
    date_debutpost= request.form['txtdateD']
    date_finpost= request.form['txtdateF']
    
    events_rs = Events.objects.get(id=ObjectId(oid))
    if not events_rs:
        return json.dumps({'error':'data not found'})
    else:
        if titrepost == 'titre':
            events_rs.update(titre=titrepost)
        elif categoriepost == 'categorie':
            events_rs.update(categorie=categoriepost)
        elif courte_descriptionpost == 'courte_description':
            events_rs.update(courte_description=courte_descriptionpost)
        elif descriptionpost == 'description':
            events_rs.update(description=descriptionpost)
        elif lieupost == 'lieu':
            events_rs.update(lieu=lieupost)
        elif date_debutpost == 'date_debut':
            events_rs.update(date_debut=date_debutpost) 

        elif date_finpost == 'date_fin':
            events_rs.update(date_fin=date_finpost)


    return json.dumps({'status':'OK'})
'''
     
@app.route('/admin/add-events', methods=['GET', 'POST'])
@login_required
def create_record():
    txttitre = request.form['txttitre']
    txtcategorie = request.form['txtcategorie']
    txtcourte_description = request.form['txtcourte_description']
    txtdescription = request.form['editordata']
    txtlieu = request.form['txtlieu']
    txtdateD = request.form['txtdateD']
    txtdateF = request.form['txtdateF']
    
    eventssave = Events(titre=txttitre, categorie=txtcategorie, courte_description=txtcourte_description, description=txtdescription, lieu=txtlieu, date_debut=txtdateD, date_fin=txtdateF)
    eventssave.save()
    return redirect('/admin/events')



@app.route('/admin/delete-event/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_events(getid):
    print(getid)
    eventsrs = Events.objects(id=getid).first()
    if not eventsrs:
        return jsonify({'error': 'data not found'})
    else:
        eventsrs.delete() 
    return redirect('/admin/events')


@app.route('/admin/registred-users')
@login_required
def user_records():
    title = "registred-users"
    users = Users.objects.all()
    return render_template('admin/reguser.html', users=users,name=current_user.email,title=title)




@app.route('/admin/add-categories', methods=['GET', 'POST'])
@login_required
def create_category_records():
    txttitre = request.form['txttitre']
    categoryssave = Category(titre = txttitre)
    categoryssave.save()
    return redirect('/admin/categories')

@app.route('/admin/categories')
@login_required
def categ_records():
    title = "categories"
    categ = Category.objects.all()
    return render_template('admin/categories.html', categ=categ,name=current_user.email,title=title)
    
@app.route('/admin/delete-categ/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_categ(getid):
    print(getid)
    categsrs = Category.objects(id=getid).first()
    if not categsrs:
        return jsonify({'error': 'data not found'})
    else:
        categsrs.delete() 
    return redirect('/admin/categories')


@app.route('/admin/add-csn', methods=['GET', 'POST'])
@login_required
def create_committenational_records():
    txtnom = request.form['txtnom']
    txtuni = request.form['txtuni']
    committensave = CommitteNational(nom = txtnom, universite = txtuni)
    committensave.save()
    return redirect('/admin/committe-scientifique-national')

@app.route('/admin/committe-scientifique-national')
@login_required
def committenational_records():
    title = "Comité scientifique national"
    csn = CommitteNational.objects.all()
    return render_template('admin/csn.html', csn=csn,name=current_user.email,title=title)

@app.route('/admin/delete-commite-national/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_csn(getid):
    print(getid)
    csnsrs = CommitteNational.objects(id=getid).first()
    if not csnsrs:
        return jsonify({'error': 'data not found'})
    else:
        csnsrs.delete() 
    return redirect('/admin/committe-scientifique-national')


@app.route('/admin/add-csi', methods=['GET', 'POST'])
@login_required
def create_committeinternational_records():
    txtnom = request.form['txtnom']
    txtuni = request.form['txtuni']
    committeisave = CommitteInternational(nom = txtnom, universite = txtuni)
    committeisave.save()
    return redirect('/admin/committe-scientifique-international')

@app.route('/admin/committe-scientifique-international')
@login_required
def committeinternational_records():
    title = "Comité scientifique international"
    csi = CommitteInternational.objects.all()
    return render_template('admin/csi.html', csi=csi,name=current_user.email,title=title)

@app.route('/admin/delete-commite-international/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_csi(getid):
    print(getid)
    csisrs = CommitteInternational.objects(id=getid).first()
    if not csisrs:
        return jsonify({'error': 'data not found'})
    else:
        csisrs.delete() 
    return redirect('/admin/committe-scientifique-international')



@app.route('/admin/slide-parametre')
@login_required
def parametre_records():
    title = "Parametre"
    para = Parametre.objects.all()
    return render_template('admin/parametre.html', para=para,name=current_user.email,title=title)

@app.route('/admin/add-para', methods=['GET', 'POST'])
@login_required
def create_para_records():
    txttitre1 = request.form['txttitre1']
    txttitre2 = request.form['txttitre2']
    parasave = Parametre(slide_title = txttitre1, slide_title2 = txttitre2)
    parasave.save()
    return redirect('/admin/slide-parametre')


@app.route('/admin/delete-para/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_para(getid):
    print(getid)
    parasrs = Parametre.objects(id=getid).first()
    if not parasrs:
        return jsonify({'error': 'data not found'})
    else:
        parasrs.delete() 
    return redirect('/admin/slide-parametre')

@app.route('/admin/speakers')
@login_required
def speaker_records():
    title = "Speakers"
    spekr = Speakers.objects.all()
    return render_template('admin/speakers.html', spekr=spekr,name=current_user.email,title=title)


@app.route('/admin/add-speaker', methods=['GET', 'POST'])
@login_required
def create_speaker_records():
    txttitre1 = request.form['txttitre1']
    txttitre2 = request.form['txttitre2']
    txttitre3 = request.form['txttitre3']
    txttitre4 = request.form['txttitre4']
    spkrsave = Speakers(profession = txttitre1, nom = txttitre2, uni = txttitre3,titre= txttitre4)
    spkrsave.save()
    return redirect('/admin/speakers')

@app.route('/admin/delete-speaker/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_speaker(getid):
    print(getid)
    spkrsrs = Speakers.objects(id=getid).first()
    if not spkrsrs:
        return jsonify({'error': 'data not found'})
    else:
        spkrsrs.delete() 
    return redirect('/admin/speakers')





@app.route('/admin/equipe-organisation')
@login_required
def eq_records():
    title = "Equipe d'organisation"
    eq = EquipeOrganisation.objects.all()
    return render_template('admin/eq-orga.html', eq=eq,name=current_user.email,title=title)


@app.route('/admin/add-membre-organisation', methods=['GET', 'POST'])
@login_required
def create_mbr_records():
    txttitre1 = request.form['txttitre1']
    txttitre2 = request.form['txttitre2']
    txttitre3 = request.form['txttitre3']
    mbrsave = EquipeOrganisation(nom = txttitre1, apropos = txttitre2, tache = txttitre3)
    mbrsave.save()
    return redirect('/admin/equipe-organisation')

@app.route('/admin/delete-mbr/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_mbr(getid):
    print(getid)
    mbrsrs = EquipeOrganisation.objects(id=getid).first()
    if not mbrsrs:
        return mbrsrs({'error': 'data not found'})
    else:
        mbrsrs.delete() 
    return redirect('/admin/speaker')



@app.route('/admin/date-importante')
@login_required
def date_records():
    title = "Dates Importantes"
    dates = DateImportante.objects.all()
    return render_template('admin/dateimportante.html', dates=dates,name=current_user.email,title=title)


@app.route('/admin/add-date', methods=['GET', 'POST'])
@login_required
def create_date_records():
    txttitre1 = request.form['txttitre1']
    txttitre2 = request.form['txttitre2']
    txttitre3 = request.form['txttitre3']
    datesave = DateImportante(date1 = txttitre1, date2 = txttitre2, date3 = txttitre3)
    datesave.save()
    return redirect('/admin/date-importante')

@app.route('/admin/delete-date/<string:getid>', methods = ['POST','GET'])
@login_required
def delete_date(getid):
    print(getid)
    datesrs = DateImportante.objects(id=getid).first()
    if not datesrs:
        return datesrs({'error': 'data not found'})
    else:
        datesrs.delete() 
    return redirect('/admin/speaker')


@app.route('/admin/reservation')
@login_required
def reservation_records():
    title = "Reservation"
    return render_template('admin/reservation.html',name=current_user.email,title=title)





#PARTIE UTILISATEUR/VISITEUR
@app.route("/")
def home():
    titrep='HOME'
    events = Events.objects().limit(3)
    para = Parametre.objects.all()
    speakers = Speakers.objects().limit(4)
    categ = Category.objects.all()
    return render_template("site/page1.html",titrep=titrep,events=events,para=para,speakers=speakers,categ=categ)


@app.route("/s'inscrire",methods=['GET', 'POST'])
def sinscrire():
    titre="S'inscrire"
    categ = Category.objects.all()
    form = MyForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = Users.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = Users(last_name =form.last_name.data ,first_name =form.first_name.data ,username =form.username.data ,
                phone =form.phone.data ,email = form.email.data,password=hashpass).save()
                login_user(hey)
                return redirect(url_for('seconn'))
    return render_template("site/inscrire.html",form=form,titre=titre,categ=categ)


@app.route("/se-connecter",methods=['GET', 'POST'])
def seconn():
    titre='Se connecter'
    categ = Category.objects.all()
    if current_user.is_authenticated == True:
        #flash("vous etes connecte","danger")
        return redirect(url_for('profil'))
    form = RegFormuser()
    if request.method == 'POST':
        if form.validate():
            check_user = Users.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    #flash("vous etes connecte","info")
                    return redirect(url_for('profil'))

    return render_template("site/seconnecter.html",titre=titre,form=form,categ=categ)

@app.route("/se-deconnecter",methods=['GET'])
def deconn():
    logout_user()
    flash('vous etes deconnecte','danger')
    return redirect(url_for('home'))




@app.route("/moncompte",methods=['GET', 'POST'])
def profil():
    titre="Mon Compte/Profil"
    form = RegFormuser()
    return render_template("site/profil.html",titre=titre,form=form)



@app.route("/contact")
def contact():
    titre="contact"
    return render_template("site/contact.html",titre=titre)

@app.route("/evennement")
def evenn():
    titre="Evennements"
    events = Events.objects().all()
    categ = Category.objects.all()
    return render_template("site/listevent.html",titre=titre,events=events,categ=categ)


@app.route('/details-evennement/<oid>')
def detailsevenn(oid):
    titre="Evennements"
    categ = Category.objects.all()
    eventsrs = Events.objects.get(id=ObjectId(oid))
    return render_template("site/detailsevent.html",titre=titre,eventsrs=eventsrs,categ=categ)

'''


@app.route('/evennment-reservation/<oid>',methods=['GET','POST'])
def reservation_event(oid):
    eventsrc = Events.objects.get(id=ObjectId(oid))
    users_resr = Users.objects.get(id=ObjectI(oid))
    if "email" in session:
        id="'"+id+"'"
        nbr_res = request.form['nbr_res']
        reserssave = Reservation(nbr_places = nbr_res,date_reservation=datetime.now,userid=users_resr.name,titre_evenn=eventsrc.titre)
        reserssave.save()
        return redirect(url_for('list_res'))
    return redirect(url_for('seconn'))

@app.route('/evennement/liste-reservation')
def list_res():
    if "email" in session:
        reser = Reservation.objects.all()
        return render_template("site/mybooking.html",reser=reser)
    return redirect(url_for('seconn'))

'''



@app.route("/speakers")
def list_speaker():
    titre="Speakers"
    speakers = Speakers.objects().all()
    categ = Category.objects.all()
    return render_template("site/speakers.html",titre=titre,speakers=speakers,categ=categ)


@app.route("/comite")
def list_comite():
    titre="Comite"
    comite_n = CommitteNational.objects().all()
    comite_i = CommitteInternational.objects().all()
    categ = Category.objects.all()
    return render_template("site/comite.html",titre=titre,categ=categ,comite_n=comite_n,comite_i=comite_i)


@app.route("/eq-organisation")
def list_equipe():
    titre="Equipe d'organition"
    etudiants = EquipeOrganisation.objects(tache ="Etudiant")
    presidents = EquipeOrganisation.objects(tache = "President")
    categ = Category.objects.all()
    return render_template("site/eq_org.html",titre=titre,categ=categ,presidents=presidents,etudiants=etudiants)

@app.route("/date-importante")
def imp_date():
    titre="Date Importante"
    dates = DateImportante.objects.all()
    categ = Category.objects.all()
    return render_template("site/dateimpo.html",titre=titre,categ=categ,dates=dates)

@app.route('/pageESTE')
def page_records():
    titre = "ESTE"
    categ = Category.objects.all()
    return render_template('site/este.html',titre=titre,categ=categ)

if __name__=="__main__":
    app.run(debug=True)