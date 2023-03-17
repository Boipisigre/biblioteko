
import sqlite3
# from werkzeug.datastructures import ImmutableMultiDict


def get_db_connection():
    conn = sqlite3.connect('app/static/db/biblioteko.db')
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
    updtable.execute("insert into libroj (ĉefŝlosilo, titolo,rubrikoj,autoro,eldono,ŝanĝi) values (?, ?, ?, ?,?, date())", data)
    DBCon.commit()
    updtable.close()
    DBCon.close()
    return

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

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM notes WHERE id = ?',
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

def update_note(titolo, enhavo, id):
    conn = get_db_connection()
    conn.execute('UPDATE notes SET titre = ?, corps = ?, modif=date()'
                 ' WHERE id = ?', (titolo, enhavo, id))
    conn.commit()
    conn.close()
