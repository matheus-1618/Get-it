from src.utils import delete, load_data, load_template, salvar_dados, build_response, delete, update
import urllib

def index(request,db):
     # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            key,value = chave_valor.split("=")
            key = urllib.parse.unquote_plus(key)
            value = urllib.parse.unquote_plus(value)
            params[key] = value
            
        if params['verb']=='delete':
            delete(db,params['id'])
        elif params['verb']=='add':
            #if params['title']!="" and params['details']!='':
            salvar_dados(db,params)
        elif params['verb']=='update':
            #if params['title']!=""and params['details']!='':
            update(db,params['id'],params['title'],params['details'])
        
    # O RESTO DO CÓDIGO DA FUNÇÃO index CONTINUA DAQUI PARA BAIXO...
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in load_data(db)
    ]
    notes = '\n'.join(notes_li)
    
    if not request.startswith('POST'):
        js = """ $(document).on("click", ".button", function () {
                    var id = $(this).data('id');
                    var title = $(this).data('title');
                    var details = $(this).data('details');
                    $(".modal-footer #id").val(id);
                    $(".modal-title #title").val(title);
                    $(".modal-body #details").val(details);
                    }); 

                    $('#card-container').sortable({
                        animation: 150,
                        ghostClass: 'ghost',
                        ghostClass: 'blue-background-class'
                    });
                    """
        return build_response(load_template('index.html').format(notes=notes,js=js))
    return build_response(code=303, reason='See Other', headers='Location: /')