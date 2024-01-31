# -*- coding: utf-8 -*-

@auth.requires_login()
def balanco_patrimonial():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if usuario.ativo == False:
        redirect(URL('default', 'index'))
    return locals()

@auth.requires_login()
def receber():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if not usuario.ativo:
        redirect(URL('default', 'index'))

    # Configurações de paginação e verificação dos parâmetros da URL
    paginacao = empresa.paginacao
    pagina = int(request.args[0]) if request.args and request.args[0].isdigit() else 1

    if pagina <= 0:
        pagina = 1

    limites = (paginacao * (pagina - 1), paginacao * pagina)

    # Consulta os registros dos registros financeiros da empresa, incluindo filtro de pesquisa
    classificacao_ids = db(
        (db.classificacao.empresa == empresa.id) &
        (db.classificacao.tipo == "Entrada")
    ).select(db.classificacao.id)

    if classificacao_ids:
        query = (
            (db.registro_financeiro.classificacao.belongs(classificacao_ids)) &
            (db.registro_financeiro.liquidado == False)
        )

        total_registros = db(query).count()
        paginas = (total_registros + paginacao - 1) // paginacao

        if total_registros == 0:
            paginas = 1

        registros = db(query).select(
            limitby=limites, orderby=db.registro_financeiro.data_vencimento
        )
    else:
        redirect(URL('acs_empresa', 'index'))

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total_registros, empresa=empresa)


@auth.requires_login()
def pagar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if not usuario.ativo:
        redirect(URL('default', 'index'))

    # Configurações de paginação e verificação dos parâmetros da URL
    paginacao = empresa.paginacao
    pagina = int(request.args[0]) if request.args and request.args[0].isdigit() else 1

    if pagina <= 0:
        pagina = 1

    limites = (paginacao * (pagina - 1), paginacao * pagina)

    # Consulta os registros dos registros financeiros da empresa, incluindo filtro de pesquisa
    classificacao_ids = db(
        (db.classificacao.empresa == empresa.id) &
        (db.classificacao.tipo == "Entrada")
    ).select(db.classificacao.id)

    if classificacao_ids:
        query = (
            (db.registro_financeiro.classificacao.belongs(classificacao_ids)) &
            (db.registro_financeiro.liquidado == False)
        )

        total_registros = db(query).count()
        paginas = (total_registros + paginacao - 1) // paginacao

        if total_registros == 0:
            paginas = 1

        registros = db(query).select(
            limitby=limites, orderby=db.registro_financeiro.data_vencimento
        )
    else:
        redirect(URL('acs_empresa', 'index'))

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total_registros, empresa=empresa)


@auth.requires_login()
def mes():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    tipo = request.args(0, cast=str)

    if len(request.args) == 1:
        index = 0
    else:
        index = int(request.args[1])

    primeiro, ultimo = primeiro_ultimo_dia_do_mes(index)
    classificacao_ids = db(
        (db.classificacao.empresa == usuario.empresa) &
        (db.classificacao.tipo == tipo.title())
    ).select(db.classificacao.id)

    if classificacao_ids:
        # Consulta ao banco de dados para obter registros financeiros
        rows = db(
            (db.registro_financeiro.classificacao.belongs(classificacao_ids)) &
            (db.registro_financeiro.empresa == empresa.id) &
            (db.registro_financeiro.data_vencimento >= primeiro) &
            (db.registro_financeiro.data_vencimento <= ultimo)
        ).select(
            orderby=db.registro_financeiro.data_vencimento
        )
    else:
        rows= []
    pagina=1
    paginas=1
    total=db(
        (db.registro_financeiro.empresa == usuario.empresa) &
        (db.registro_financeiro.data_vencimento >= primeiro) &
        (db.registro_financeiro.data_vencimento <= ultimo)
    ).count()
    return locals()

@auth.requires_login()
def liquidar():
    # Busca o usuário e registro relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    registro_financeiro = db.registro_financeiro(request.args(0, cast=int))
    associado = db.associado(registro_financeiro.associado)
    if len(request.args) == 1:
        pagina = 1
        tipo = 'receber'
    else:
        pagina = int(request.args[1])
        tipo = str(request.args[2])

    # Redireciona se o registro não pertencer à empresa do usuário
    if registro_financeiro.empresa != usuario.empresa:
        redirect(URL('index'))
    db.associado.delegacia.writable=True
    db.associado.delegacia.readable=True
    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Alterar registro'  # define o título da página

    # Cria e processa o formulário de alteração
    if registro_financeiro.liquidado==True:
        registro_financeiro.liquidado=False
    else:
        registro_financeiro.liquidado=True
    registro_financeiro.update_record()

    # Retorna o formulário para a visualização
#     return locals()
    return redirect(URL(tipo, args=[pagina]))


@auth.requires_login()
def balanco():
    # Busca o usuário e registro relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)
    rows = db(db.classificacao.empresa==empresa.id).select(orderby=db.classificacao.tipo)
    if len(request.args) == 0:
        index = 0
    else:
        index = int(request.args[0])

    primeiro, ultimo = primeiro_ultimo_dia_do_mes(index)
    return locals()
