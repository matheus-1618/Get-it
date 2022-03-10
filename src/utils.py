import json
import data.database as database

def extract_route(string):
    first = string.find("/")
    end = string.find("HTTP")
    return string[first+1:end-1]

def read_file(path):
    with open(path,"r+b") as file:
        try:
            return file.read()
        except Exception as erro:
            print(erro)

def load_data(db):
    notes = db.get_all()
    #print(notes)
    # with open(f"data/{name}",'r') as file:
    #     out = json.load(file)
    # return out
    return notes

def load_specific_data(db,id):
    note = db.get(id)
    return note

def load_template(template):
     path = "templates/"+str(template)
     with open(path,'r', encoding = "utf-8") as file:
         return file.read()

def salvar_dados(db,file):
    db.add(database.Note(content=file["detalhes"], title=file["titulo"]))
    
def delete(db,id):
    db.delete(id)

def update(db,id,title,details):
    note = database.Note(id=id,title=title,content=details)
    db.update(note)

def build_response(body='', code=200, reason='OK', headers=''):
    if headers != "":
        return f'HTTP/1.1 {code} {reason}\n{headers}\n\n{body}'.encode()
    return f'HTTP/1.1 {code} {reason}\n\n{body}'.encode()
        
