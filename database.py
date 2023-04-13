
import sqlite3
# from werkzeug.datastructures import ImmutableMultiDict


def get_db_connection():
    conn = sqlite3.connect('app/instance/biblioteko.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_notes(filtre):
    DBCon = get_db_connection()

    # print("=================================")
    # Ouvrir un curseur
    ltable = DBCon.cursor()
    # print(filtre)
    if filtre == "*":
        notes = ltable.execute("select * from libroj").fetchall()
    else:
        filtre="%"+filtre.upper()+"%"
        # print(filtre)
        notes = ltable.execute("select * from libroj where upper(titolo) like ?",[filtre,]).fetchall()# print(notes)
        # print(notes)

    ltable.close()
    DBCon.close()
    # print("=================================")
    return  notes

def list_users():
    DBCon = get_db_connection()

    # print("=================================")
    # Ouvrir un curseur
    ltable = DBCon.cursor()

    users = ltable.execute("select * from utilisateur").fetchall()

    ltable.close()
    DBCon.close()
    # print("=================================")
    return  users


def get_livres(filtre):
    DBCon = get_db_connection()

    # print("=================================")
    # Ouvrir un curseur
    ltable = DBCon.cursor()
    # print(filtre)
    if filtre == "*":
        notes = ltable.execute("select * from libroj where pretaal is null").fetchall()
    else:
        filtre="%"+filtre.upper()+"%"
        # print(filtre)
        notes = ltable.execute("select * from libroj where length(pretaal) is null and upper(titolo) like ?",[filtre,]).fetchall()# print(notes)
        # print(notes)

    ltable.close()
    DBCon.close()
    # print("=================================")
    return  notes

def get_livresprete(filtre):
    DBCon = get_db_connection()

    # print("=================================")
    # Ouvrir un curseur
    ltable = DBCon.cursor()
    # print(filtre)
    if filtre == "*":
        notes = ltable.execute("select * from libroj where pretaal is not null").fetchall()
    else:
        filtre="%"+filtre.upper()+"%"
        # print(filtre)
        notes = ltable.execute("select * from libroj where length(pretaal) is not null and upper(titolo) like ?",[filtre,]).fetchall()# print(notes)
        # print(notes)

    ltable.close()
    DBCon.close()
    # print("=================================")
    return  notes



def get_notes_user(filtre):
    DBCon = get_db_connection()

    # print("=================================")
    # Ouvrir un curseur
    ltable = DBCon.cursor()
    # print(filtre)
    if filtre == "*":
        notes = ltable.execute("select * from libroj").fetchall()
    else:
        filtre="%"+filtre.upper()+"%"
        # print(filtre)
        notes = ltable.execute("select * from libroj where upper(Autoro) like ?",[filtre,]).fetchall()# print(notes)
        # print(notes)

    ltable.close()
    DBCon.close()
    # print("=================================")
    return  notes


def add_notes(col1,col2,col3,col4,col5):
    DBCon = get_db_connection()
    # print("=================================")
    # Ouvrir un curseur
    updtable = DBCon.cursor()
    data = [col1,col2,col3,col4,col5]
    # add_notes(txt_id, txt_titre,txt_rubrique,txt_auteur, txt_editeur)
    updtable.execute("insert into libroj (ĉefŝlosilo, titolo,rubrikoj,autoro,eldono,dcreate) values (?, ?, ?, ?,?, date())", data)
    DBCon.commit()
    updtable.close()
    DBCon.close()
    return

def rezervu_libro(id,nomo):
    conn = get_db_connection()
    conn.execute('UPDATE libroj SET pretaal = ?, datepret = date() WHERE ĉefŝlosilo = ?', (nomo, id))
    conn.commit()
    conn.close()

def redonu_libro(id):
    #print(id)
    conn = get_db_connection()
    conn.execute('UPDATE libroj SET pretaal = NULL , datepret = date() WHERE ĉefŝlosilo = ?', [id] )
    conn.commit()
    conn.close()

def add_user(nom,mdp):
    DBCon = get_db_connection()
    # print("=================================")

    updtable = DBCon.cursor()
    data = [nom,mdp]
    updtable.execute("insert into utilisateur (nom,modif, hashpwd) values (?, date(),?)", data)
    DBCon.commit()
    updtable.close()
    DBCon.close()
    return

def upd_user(nom,mdp):
    DBCon = get_db_connection()
        # print("=================================")
    updtable = DBCon.cursor()
    data = [mdp,nom]
    print (mdp)
    print(nom)
    print(data)
    updtable.execute("update utilisateur set hashpwd=? where nom = ?", data)
    DBCon.commit()
    updtable.close()
    DBCon.close()
    return

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM libroj WHERE ĉefŝlosilo = ?',
                        (post_id,)).fetchall()
    conn.close()
    # print(post)
    if post is None:
        abort(404)
    return post

def get_user(nom):
    conn = get_db_connection()
    mdp = conn.execute('SELECT hashpwd FROM utilisateur WHERE nom = ?',(nom,)).fetchone()
    conn.close()
    return mdp

def is_admin(nom):
    conn = get_db_connection()
    admin = conn.execute('SELECT admin FROM utilisateur WHERE nom = ?',(nom,)).fetchone()
    conn.close()
    return admin

def update_note(autoro, titolo, enhavo, id):
    conn = get_db_connection()
    conn.execute('UPDATE libroj SET titolo = ?, autoro = ?, Eldono=? '
                 ' WHERE ĉefŝlosilo = ?', (titolo, autoro, enhavo, id))
    conn.commit()
    conn.close()

def delete_livre(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM libroj WHERE ĉefŝlosilo = ?', (id,))
    conn.commit()
    conn.close()

def forigi_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM utilisateur WHERE id = ?', [id])
    conn.commit()
    conn.close()
