# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    """
    Função: index
    Descrição: Página principal após o login, redireciona para diferentes páginas baseado no tipo de usuário logado.
    """
    # Verifica se o usuário está associado a uma empresa
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    if not usuario:
        redirect(URL('acs_empresa', 'cadastrar'))  # Redireciona para a página de cadastro de empresa se não estiver associado

    # Redireciona para páginas específicas baseado no tipo de usuário
    elif usuario.tipo == "Atendente":
        redirect(URL('acs_registro', 'index'))  # Redireciona para a página de registro se for um atendente
    elif usuario.tipo == "Representante":
        redirect(URL('acs_representante', 'index'))  # Redireciona para a página do representante se for um representante

    # Obtém informações da empresa associada ao usuário logado
    empresa = db.empresa(usuario.empresa)
    if not empresa.q_usuarios:
        empresa.q_usuarios=2
        empresa.update_record()
    paginacao = empresa.q_usuarios  # Número de registros por página

    # Lógica de paginação
    if len(request.args) == 0:
        pagina = 1  # Define a página como 1 se não houver argumentos na URL
    else:
        try:
            pagina = int(request.args[0])  # Obtém o número da página da URL
        except ValueError:
            redirect(URL('erro', vars={'msg': 'Número da página inválido'}))  # Redireciona para erro se o número da página for inválido

    if pagina <= 0:
        pagina = 1  # Corrige o número da página se for menor ou igual a zero

    # Obtém o número total de registros da empresa para calcular o número de páginas
    total = db((db.usuario_empresa.empresa == empresa.id)& (db.usuario_empresa.usuario != 1)).count()
    paginas = total // paginacao  # Calcula o número total de páginas
    if total % paginacao:
        paginas += 1  # Incrementa uma página se houver resto na divisão

    if total == 0:
        paginas = 1  # Define como uma página se não houver registros

    if pagina > paginas:
        redirect(URL(args=[paginas]))  # Redireciona para a última página se a página atual for maior que o número de páginas

    # Limites para exibir os registros na página atual
    limites = (paginacao * (pagina - 1), (paginacao * pagina))
    registros = db((db.usuario_empresa.empresa == empresa.id) & (db.usuario_empresa.usuario != 1)).select(
        limitby=limites,
        orderby=~db.usuario_empresa.id
    )  # Obtém os registros da empresa

    consul = (request.args(1))  # Parâmetro opcional para consultas
    liberado = True  # Flag para controle de permissão

    # Retorna um dicionário de dados para a view
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul, liberado=liberado, empresa=empresa)

@auth.requires_login()
def alterar():
    """
    Função: alterar
    Descrição: Permite alterar os dados de um usuário específico.
    """

    try:
        # Define a view a ser renderizada como 'generic.html'
        response.view = 'generic.html'

        # Define a função atual como 'Alterar'
        request.function = 'Alterar'

        # Obtém o usuário da empresa com base no argumento da URL
        usuario_empresa = db.usuario_empresa(request.args(0, cast=int))
        if auth.user.id==1:
            db.usuario_empresa.empresa.writable = True
            db.usuario_empresa.empresa.readable = True
            db.usuario_empresa.empresa.label = "#Empresa"

        # Cria um formulário para alterar os dados do usuário
        form = SQLFORM(db.usuario_empresa, request.args(0, cast=int), deletable=False)

        if form.process().accepted:
            # Se o formulário for aceito, redireciona para a página de alteração do usuário
            redirect(URL('alterar_user', args=usuario_empresa.usuario))
        elif form.errors:
            # Se houver erros no formulário, exibe uma mensagem de flash informando que o formulário não foi aceito
            response.flash = 'Formulário não aceito'
    except:
        # Em caso de exceção, redireciona para a página de alteração do usuário
        redirect(URL('alterar_user', args=usuario_empresa.usuario))

    # Retorna o formulário para a view
    return dict(form=form)

@auth.requires_login()
def alterar_user():
    """
    Função: alterar_user
    Descrição: Permite a alteração dos dados de um usuário específico.
    """

    try:
        # Define a view a ser renderizada como 'generic.html'
        response.view = 'generic.html'

        # Define a função atual como 'Alterar'
        request.function = 'Alterar'

        # Obtém o usuário a partir do argumento da URL
        usuario = db.auth_user(request.args(0, cast=int))
        
        deletar=False
        if auth.user.id==1:
            deletar=True

        # Cria um formulário para alterar os dados do usuário
        form = SQLFORM(db.auth_user, request.args(0, cast=int), deletable=deletar)

        if form.process().accepted:
            # Se o formulário for aceito, redireciona para a página inicial
            redirect(URL('index'))
        elif form.errors:
            # Se houver erros no formulário, exibe uma mensagem de flash informando que o formulário não foi aceito
            response.flash = 'Formulário não aceito'
    except:
        # Em caso de exceção, redireciona para a página inicial
        redirect(URL('index'))

    # Retorna o formulário para a view
    return dict(form=form)

@auth.requires_login()
def cadastrar():
    """
    Função: cadastrar
    Descrição: Permite o cadastro de um novo usuário.
    """
    
    # Define a view a ser renderizada como 'generic.html'
    response.view = 'generic.html'

    # Verifica se o usuário está associado a uma empresa
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    if not usuario:
        redirect(URL('acs_empresa', 'cadastrar'))  # Redireciona para a página de cadastro de empresa se não estiver associado

    # Obtém informações da empresa associada ao usuário logado
    empresa = db.empresa(usuario.empresa)
    total = db((db.usuario_empresa.empresa == empresa.id)).count()
    if (total)>=empresa.q_usuarios:
        redirect(URL('index'))
        
    # Cria um formulário para cadastrar um novo usuário
    form = SQLFORM(db.auth_user).process()

    if form.accepted:
        # Se o formulário for aceito, exibe uma mensagem de flash informando que o formulário foi aceito
        response.flash = 'Formulário aceito'
        # Redireciona para a página de vinculação do novo usuário à empresa
        redirect(URL('vincular_login', args=[empresa.id, form.vars.id]))
    elif form.errors:
        # Se houver erros no formulário, exibe uma mensagem de flash informando que o formulário não foi aceito
        response.flash = 'Formulário não aceito'
    else:
        # Se o formulário ainda não foi preenchido, exibe uma mensagem para preenchê-lo
        response.flash = 'Preencha o formulário'

    # Retorna o formulário para a view
    return dict(form=form)

@auth.requires_login()
def vincular_login():
    """
    Função: vincular_login
    Descrição: Vincula um novo usuário a uma empresa.
    """

    # Define a view a ser renderizada como 'generic.html'
    response.view = 'generic.html'

    # Obtém a empresa e o usuário a partir dos argumentos da URL
    empresa = db.empresa(request.args(0, cast=int))
    usuario = db.auth_user(request.args(1, cast=int))
    total = db((db.usuario_empresa.empresa == empresa.id)).count()
    if (total)>=empresa.q_usuarios:
        redirect(URL('index'))
    # Define os valores padrão para o novo vínculo entre usuário e empresa
    db.usuario_empresa.empresa.default = request.args(0, cast=int)
    db.usuario_empresa.usuario.default = request.args(1, cast=int)
    db.usuario_empresa.tipo.default = "Administrador"

    # Cria um formulário para vincular o novo usuário à empresa
    form = SQLFORM(db.usuario_empresa).process()

    if form.accepted:
        # Se o formulário for aceito, redireciona para a página inicial
        redirect(URL('index'))
    elif form.errors:
        # Se houver erros no formulário, exibe uma mensagem de flash informando que o formulário não foi aceito
        response.flash = 'Formulário não aceito'

    # Retorna o formulário para a view
    return dict(form=form)
