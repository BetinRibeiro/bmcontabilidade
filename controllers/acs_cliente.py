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
    paginacao = empresa.paginacao
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
    total = db((db.cliente.empresa == empresa.id)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    # Consulta os registros dos registros financeiros da empresa, incluindo filtro de pesquisa
    registros = db((db.cliente.empresa == empresa.id)).select(
        limitby=limites, orderby=db.cliente.id | db.cliente.nome)
    consul = request.args(1)
    if consul:
        registros = db((db.cliente.empresa == empresa.id) & (
            (db.cliente.nome.contains(consul)) | (db.cliente.nome.contains(consul)))).select(
            limitby=limites, orderby=db.cliente.nome)

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


@auth.requires_login()
def cadastrar():
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Cadastro de registro'  # define o título da página

    # Define o valor padrão da empresa no formulário e processa o formulário
    db.cliente.empresa.default = usuario.empresa
    form = SQLFORM(db.cliente).process()

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
    cliente = db.cliente(request.args(0, cast=int))

    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    # Redireciona se o registro não pertencer à empresa do usuário
    if cliente.empresa != usuario.empresa:
        redirect(URL('index'))

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Alterar registro'  # define o título da página

    # Cria e processa o formulário de alteração
    form = SQLFORM(db.cliente, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)
