import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self,nome_banco):
        self.conn = sqlite3.connect("data/"+nome_banco+".db")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY,
                                            title TEXT,
                                            content TEXT NOT NULL);""")
                                            
        self.conn.commit()

    def add(self,note):
        # self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}','{note.content}');")
        self.conn.execute(f"INSERT INTO note (title, content) VALUES (?,?);",(note.title,note.content))
        self.conn.commit()
    
    def get(self,note_id):
        cursor = self.conn.execute(f"SELECT id, title, content FROM note WHERE id = ?",(int(note_id),))
        self.conn.commit()
        lista = []
        for linha in cursor:
            lista.append(Note(id=linha[0],title=linha[1],content=linha[2]))
        return lista

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        self.conn.commit()
        lista = []
        for linha in cursor:
            lista.append(Note(id=linha[0],title=linha[1],content=linha[2]))
        return lista

    def update(self,entry):
        self.conn.execute(f"UPDATE note SET id = ?, title = ?,  content = ?  WHERE id = ?",(entry.id,entry.title,entry.content,entry.id))
        self.conn.commit()
    
    def delete(self,note_id):
        self.conn.execute(f"DELETE FROM note where id=?",(note_id,))
        self.conn.commit()
