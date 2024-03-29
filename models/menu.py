# -*- coding: utf-8 -*-


lista_registros = [(T('Registros Geral'), False, URL('acs_registro', 'index'), []),
            (T('Registros Sequencial'), False, URL('acs_registro', 'sequencial'), []),
            (T('Recebimentos Atrasados'), False, URL('acs_registro', 'atrasados', args=['entrada']), []),
            (T('Pagamentos Atrasados'), False, URL('acs_registro', 'atrasados', args=['saida']), []),
        ]
lista_agrupamentos_sindicato =[
            (T('Usuarios'), False, URL('acs_usuario', 'index'), []),
            (T('Delegacias'), False, URL('acs_delegacia', 'index'), []),
            (T('Classes'), False, URL('acs_classificacao', 'index'), []),
        ]

lista_agrupamentos =[
            (T('Usuarios'), False, URL('acs_usuario', 'index'), []),
#             (T('Delegacias'), False, URL('acs_delegacia', 'index'), []),
            (T('Classes'), False, URL('acs_classificacao', 'index'), []),
        ]
    
if auth.user:
    response.menu = [
        (T('Empresa'), False, URL('acs_empresa', 'index'), []),
#         (T('Clientes'), False, URL('acs_cliente', 'index'), []),
#         (T('Associados'), False, URL('acs_associado', 'index'), []),
        (T('Registros'), False, None, lista_registros ),
        (T('Agrupamentos'), False, None, lista_agrupamentos),
        (T('Relatório'), False, URL('acs_relatorio', 'balanco'), []),
        (T('Manual'), False, URL('acs_manual', 'index'), [])
    ]
    if auth.user.id==14564654:
        response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('Community'), False, None, [
            (T('Groups'), False,
             'http://www.web2py.com/examples/default/usergroups'),
            (T('Twitter'), False, 'http://twitter.com/web2py'),
            (T('Live Chat'), False,
             'http://webchat.freenode.net/?channels=web2py'),
        ]),
    ]


else:
    response.menu = [
        (T('Manual'), False, URL('acs_manual', 'index'), [])
    ]
