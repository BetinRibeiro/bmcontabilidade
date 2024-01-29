# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if usuario.ativo == False:
        redirect(URL('default', 'index'))

    # Configurações de paginação e verificação dos parâmetros da URL
    paginacao = 35
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))

    # Lógica de cálculo de páginas e limites
    if pagina <= 0:
        pagina = 1
    total = db((db.empresa.id>0)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    # Consulta os registros dos registros financeiros da empresa, incluindo filtro de pesquisa
    registros = db((db.empresa.id>0)).select(
        limitby=limites, orderby=~db.empresa.ativo | db.empresa.id)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


@auth.requires_login()
def cadastrar():
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Cadastro de registro'  # define o título da página
    if auth.user.id==1:
        db.empresa.tipo.writable = True
        db.empresa.tipo.readable = True
        db.empresa.tipo.label = "#tipo"

        db.empresa.ativo.writable = True
        db.empresa.ativo.readable = True
        db.empresa.ativo.label = "#ativo"

        db.empresa.paginacao.writable = True
        db.empresa.paginacao.readable = True
        db.empresa.paginacao.label = "#paginacao"

        db.empresa.q_usuarios.writable = True
        db.empresa.q_usuarios.readable = True
        db.empresa.q_usuarios.label = "#q_usuarios"


        db.empresa.q_classes.writable = True
        db.empresa.q_classes.readable = True
        db.empresa.q_classes.label = "#q_classes"

        db.empresa.nome_oficial.writable = True
        db.empresa.nome_oficial.readable = True
        db.empresa.nome_oficial.label = "#nome_oficial"

        db.empresa.observacao.writable = True
        db.empresa.observacao.readable = True
        db.empresa.observacao.label = "#observacao"
    # Define o valor padrão da empresa no formulário e processa o formulário
    form = SQLFORM(db.empresa).process()

    # Redireciona para a página principal após aceitar o formulário
    if form.accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)
@auth.requires_login()
def alterar():
    # Busca o usuário e registro relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(request.args(0, cast=int))

    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Alterar Empresa'  # define o título da página
    # Redireciona se o registro não pertencer à empresa do usuário
    if auth.user.id!=1:
        redirect(URL('index'))
    else:
        db.empresa.tipo.writable = True
        db.empresa.tipo.readable = True
        db.empresa.tipo.label = "#tipo"

        db.empresa.ativo.writable = True
        db.empresa.ativo.readable = True
        db.empresa.ativo.label = "#ativo"

        db.empresa.paginacao.writable = True
        db.empresa.paginacao.readable = True
        db.empresa.paginacao.label = "#paginacao"

        db.empresa.q_usuarios.writable = True
        db.empresa.q_usuarios.readable = True
        db.empresa.q_usuarios.label = "#q_usuarios"


        db.empresa.q_classes.writable = True
        db.empresa.q_classes.readable = True
        db.empresa.q_classes.label = "#q_classes"

        db.empresa.nome_oficial.writable = True
        db.empresa.nome_oficial.readable = True
        db.empresa.nome_oficial.label = "#nome_oficial"

        db.empresa.observacao.writable = True
        db.empresa.observacao.readable = True
        db.empresa.observacao.label = "#observacao"
    # Cria e processa o formulário de alteração
    form = SQLFORM(db.empresa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)


def vincular():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(request.args(0, cast=int))
    usuario.empresa=empresa.id
    usuario.update_record()
    return redirect(URL('acs_empresa','index'))
    

def vincular_usuarios():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(request.args(0, cast=int))
    usuario.empresa=empresa.id
    usuario.update_record()
    return redirect(URL('acs_usuario','index'))
