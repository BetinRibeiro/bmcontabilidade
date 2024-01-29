# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

    
    # Desativa a edição e leitura do campo ID da tabela auth_user
db.auth_user.id.writable = False
db.auth_user.id.readable = False

# Define a tabela 'empresa'
db.define_table('empresa',
                Field('nome', 'string', label='Nome', requires=IS_UPPER()),
                Field('nome_oficial', 'string', label='Nome Oficial', writable=False, readable=False, requires=IS_UPPER()),
                Field('tipo', 'string', label='Tipo', default="GERAL", writable=False, readable=False,  requires=IS_IN_SET(['GERAL', 'SINDICATO', 'COMERCIO','OUTRO'])),
                Field('ativo', 'boolean', writable=False, readable=False, default=True, label='Ativo'),
                Field('paginacao', 'integer', writable=False, readable=False, default=30),
                Field('q_usuarios', 'integer', writable=False, readable=False, default=2),
                Field('q_classes', 'integer', writable=False, readable=False, default=8),
                Field('observacao', 'text', label='Observação', writable=False, readable=False),
                auth.signature,
                format='%(nome_oficial)s')

# Desativa a edição e leitura do campo ID da tabela empresa
db.empresa.id.writable = False
db.empresa.id.readable = False

# Define a tabela 'usuario_empresa'
db.define_table('usuario_empresa',
                Field('usuario', 'reference auth_user', writable=False, readable=False, label='Usuário'),
                Field('empresa', 'reference empresa', writable=False, readable=False, label='Empresa'),
                Field('tipo', 'string', label='Tipo', default='Proprietário', requires=IS_IN_SET(['Programador', 'Proprietário', 'Administrador'])),
                Field('ativo', 'boolean', writable=True, readable=True, default=True, label='Ativo'))

# Desativa a edição e leitura do campo ID da tabela usuario_empresa
db.usuario_empresa.id.writable = False
db.usuario_empresa.id.readable = False

# Documentação das tabelas
"""
Tabela auth_user:
- Campos:
  - id: ID do usuário (não editável/visível)
  - ... outros campos padrão do auth (não documentados aqui)

Tabela empresa:
- Campos:
  - id: ID da empresa (não editável/visível)
  - nome: Nome da empresa (obrigatório, formato em maiúsculas)
  - ativo: Indica se a empresa está ativa (não editável/visível, padrão: True)
  - observacao: Observação da empresa (não editável/visível)
  - ... outros campos padrão do auth (não documentados aqui)

Tabela usuario_empresa:
- Campos:
  - id: ID do relacionamento usuário-empresa (não editável/visível)
  - usuario: Usuário associado (não editável/visível)
  - empresa: Empresa associada (não editável/visível)
  - tipo: Tipo do usuário na empresa (Padrão: 'Proprietário', opções: 'Programador', 'Proprietário', 'Administrador')
  - ativo: Indica se o usuário está ativo na empresa (editável, padrão: True)
"""
