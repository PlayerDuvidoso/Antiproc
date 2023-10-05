import sqlite3
import datetime

class Lembretes:

    data_agora = datetime.datetime.now()
    data_delta = datetime.timedelta(days=1)
    data_padrao = data_agora + data_delta

    def __init__(self) -> None:

        self.con = sqlite3.connect("lembretes.db")
        self.cur = self.con.cursor()

        self.res = self.cur.execute("SELECT name FROM sqlite_master")

        if self.res.fetchone() is None: #Caso a tabela não exista, será criada
            self.cur.execute("CREATE TABLE lembretes(id, titulo, desc, data, repetir, periodo)")
        
    
    #Retorna o ID mais alto
    def ultimo_id(self):
        id = self.cur.execute("SELECT MAX(id) AS member_id FROM lembretes").fetchone()
        if id is None: id = 0
        return id[0]
    
    #Tenta retornar o ID pelo titulo
    def id_do_titulo(self, titulo):
        id = self.cur.execute("SELECT id FROM lembretes WHERE titulo=?", (titulo,)).fetchone()
        if id is None: return False
        return id[0]

    def adicionar_lembrete(self, titulo, desc=str(), data=data_padrao, repetir=0, periodo=0):

        id = self.ultimo_id() + 1

        self.cur.execute("INSERT INTO lembretes VALUES(?, ?, ?, ?, ?, ?)", (id, titulo, desc, data, repetir, periodo,))
        self.con.commit()

    def ler_lembrete(self, tituloid=str(), todos=False):
        if todos:
            todos_lembretes = self.cur.execute("SELECT titulo, desc, data, repetir, periodo FROM lembretes").fetchall()

            for index, lembrete in enumerate(todos_lembretes):
                lembrete_lista = list(lembrete)
                lembrete_lista[2] = datetime.datetime.strptime(lembrete_lista[2], r"%Y-%m-%d %H:%M:%S.%f").strftime(r"%d/%m/%Y - %H:%M")
                lembrete = tuple(lembrete_lista)
                todos_lembretes[index] = lembrete

            return todos_lembretes

        id = self.id_do_titulo(tituloid)
        if not id: return ('Lembrete não encontrado!','',self.data_padrao.strftime(r"%Y-%m-%d %H:%M:%S.%f"),0,0)

        titulo, desc, data, repetir, periodo = self.cur.execute("SELECT titulo, desc, data, repetir, periodo FROM lembretes WHERE id=?", (id,)).fetchone()
        data = datetime.datetime.strptime(data, r"%Y-%m-%d %H:%M:%S.%f")
        return (titulo, desc, data, repetir, periodo)
    
    def deletar_lembrete(self, tituloid):
        id = self.id_do_titulo(tituloid)
        if not id: return False
        print(id)
        self.cur.execute("DELETE FROM lembretes WHERE id=?", (id,))
        self.con.commit()

    def editar_lembrete(self, tituloid, novoTitulo=None, novaDesc=None, novaData=None, novoRepetir=None, novoPeriodo=None):
        id = self.id_do_titulo(tituloid)
        if not id: return False
        antigoTitulo, antigaDesc, antigaData, antigoRepetir, antigoPeriodo = self.ler_lembrete(tituloid)
        if not novoTitulo: novoTitulo = antigoTitulo
        if not novaDesc: novaDesc = antigaDesc
        if not novaData: novaData = antigaData
        if not novoRepetir: novoRepetir = antigoRepetir
        if not novoPeriodo: novoPeriodo = antigoPeriodo
        self.cur.execute("UPDATE lembretes SET titulo=?, desc=?, data=?, repetir=?, periodo=? WHERE id=?", (novoTitulo, novaDesc, novaData, novoRepetir, novoPeriodo, id))
        self.con.commit()

#   -----   Area de testes  -----

lembretes = Lembretes()
#lembretes.adicionar_lembrete('O TRESTE', 'Tudo SENDO free fire')
#lembretes.editar_lembrete('O TESTE', novaDesc='Tudo sendo CS')
#lembrete = lembretes.ler_lembrete('O TILTE DA VIDA 2')
#print(f"""
#    Titulo: {lembrete[0]}
#    Descrição: {lembrete[1]}
#    Em: {lembrete[2].strftime(r"%d/%m/%Y - %H:%M")}
#""")
#lembretes.deletar_lembrete('O TILTE DA VIDA')
todos_lembretes = lembretes.ler_lembrete(todos=True)

for lembrete in todos_lembretes:
    print(lembrete[0], ' | ', lembrete[2])