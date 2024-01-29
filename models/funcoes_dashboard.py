# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
import calendar

def contar_registros_financeiros(id_associado):
    # Substitua 'associado' e 'registro_financeiro' pelos seus nomes reais de tabelas
    # e substitua 'id_associado' pelo campo correto que relaciona as tabelas
    registros_financeiros_associado = db(db.registro_financeiro.associado == id_associado).count()

    return registros_financeiros_associado


def calcular_total_registros(id_empresa, tipo_classe, status):
    '''
    Calcula o total da soma de todos os registros financeiros da empresa que têm a classificação com o tipo e o status fornecidos.

    Args:
    - id_empresa: ID da empresa para a qual deseja-se calcular o total dos registros financeiros.
    - tipo_classe: Tipo da classificação desejada (entrada ou saída).
    - status: Status desejado dos registros financeiros (True ou False).

    Returns:
    - total: O total da soma dos valores dos registros financeiros correspondentes, ou 0 se não houver registros.
    '''
    # Encontrar todos os IDs das classificações com o tipo desejado
    classificacao_ids = db(
        (db.classificacao.empresa == id_empresa) &
        (db.classificacao.tipo == tipo_classe)
    ).select(db.classificacao.id)

    if classificacao_ids:
        # Calcular o total dos registros financeiros relacionados a cada classificação
        query = (db.registro_financeiro.classificacao.belongs(classificacao_ids)) & (db.registro_financeiro.liquidado == status)

        total = db(query).select(db.registro_financeiro.valor.sum()).first()[db.registro_financeiro.valor.sum()]
        return total or 0  # Retorna o total ou 0 se não houver registros
    else:
        return 0  # Retorna 0 se não encontrar nenhuma classificação com o tipo especificado


def primeiro_ultimo_dia_do_mes(index):
    data_atual = datetime.now()

    max_anos = 100
    novo_ano = data_atual.year + (index // 12)
    novo_mes = data_atual.month + (index % 12)
    if novo_mes <= 0:
        novo_mes += 12
        novo_ano -= 1

    if abs(index) // 12 > max_anos:
        index = max_anos * 12 if index > 0 else -max_anos * 12

    primeiro_dia = datetime(novo_ano, novo_mes, 1)

    ultimo_dia = calendar.monthrange(novo_ano, novo_mes)[1]

    return primeiro_dia, datetime(novo_ano, novo_mes, ultimo_dia)

def calcular_total_registros_intervalo(id_empresa, tipo_classe, status, index):
    '''
    Calcula o total da soma de todos os registros financeiros da empresa que têm a classificação com o tipo e o status fornecidos,
    dentro do intervalo de datas do primeiro ao último dia do mês determinado pelo índice.

    Args:
    - id_empresa: ID da empresa para a qual deseja-se calcular o total dos registros financeiros.
    - tipo_classe: Tipo da classificação desejada (entrada ou saída).
    - status: Status desejado dos registros financeiros (True ou False).
    - index: Índice para determinar o mês a ser considerado para o intervalo de datas.

    Returns:
    - total: O total da soma dos valores dos registros financeiros correspondentes dentro do intervalo de datas,
    ou 0 se não houver registros.
    '''
    # Obter as datas do primeiro e último dia do mês com base no índice
    primeiro_dia, ultimo_dia = primeiro_ultimo_dia_do_mes(index)

    # Encontrar todos os IDs das classificações com o tipo desejado
    classificacao_ids = db(
        (db.classificacao.empresa == id_empresa) &
        (db.classificacao.tipo == tipo_classe)
    ).select(db.classificacao.id)

    if classificacao_ids:
        # Calcular o total dos registros financeiros relacionados a cada classificação e dentro do intervalo de datas
        query = (db.registro_financeiro.classificacao.belongs(classificacao_ids)) & (db.registro_financeiro.liquidado == status) & (db.registro_financeiro.data_vencimento >= primeiro_dia) & (db.registro_financeiro.data_vencimento <= ultimo_dia)

        total = db(query).select(db.registro_financeiro.valor.sum()).first()[db.registro_financeiro.valor.sum()]
        return total or 0  # Retorna o total ou 0 se não houver registros
    else:
        return 0  # Retorna 0 se não encontrar nenhuma classificação com o tipo especificado

def formatar_periodo_mes(index):
    # Obter as datas do primeiro e último dia do mês com base no índice
    primeiro_dia, ultimo_dia = primeiro_ultimo_dia_do_mes(index)

    # Formatar as datas para exibição
    periodo_formatado = primeiro_dia.strftime('%d/%m') + ' à ' + ultimo_dia.strftime('%d/%m/%Y')

    return periodo_formatado


def ultimo_dia_do_mes(index):
    if index == 0:
        # Se o índice for 0, retorna o número inteiro do mês atual
        return datetime.now().month
    else:
        # Se o índice for diferente de 0, usa a função primeiro_ultimo_dia_do_mes(index) para obter o último dia do mês
        _, ultimo_dia = primeiro_ultimo_dia_do_mes(index)
        return ultimo_dia.day  # Retorna o número inteiro do último dia do mês

def dia_do_mes(index):
    '''
    Retorna o dia do mês com base no índice fornecido.

    Args:
    - index: Índice para determinar o mês.

    Returns:
    - dia: O dia do mês correspondente ao índice.
    '''

    if index > 0:
        # Retorna 1 se o índice for maior que 0
        return 1
    elif index == 0:
        # Retorna o dia do mês atual se o índice for igual a 0
        return datetime.now().day
    else:
        # Utiliza a função primeiro_ultimo_dia_do_mes para obter o último dia do mês
        primeiro_dia, ultimo_dia = primeiro_ultimo_dia_do_mes(index)
        return ultimo_dia.day

def dinheiro(numero):
    """
    Formata um número como uma string no formato de moeda (Real brasileiro).

    Esta função recebe um número e o formata como uma string no formato de moeda,
    com o símbolo "R$" e duas casas decimais separadas por vírgula.

    Args:
        numero (float): O número a ser formatado como moeda.

    Returns:
        str: A representação formatada do número como moeda (ou "0" se a conversão falhar).
    """
    try:
        numero = float(numero)
        retorno = "R$ {:,.2f}".format(round(numero, 2)).replace(",", "#").replace(".", ",").replace("#", ".")
    except:
        retorno = "0"
    return retorno


def adicionar_um_mes(data):
    # Se já for um objeto datetime.date, converte para string
    if isinstance(data, date):
        data = data.strftime('%d/%m/%Y')

    # Converte a string para um objeto datetime
    data_obj = datetime.strptime(data, '%d/%m/%Y')

    # Adiciona um mês
    nova_data_obj = data_obj + timedelta(days=31)

    # Ajusta para o último dia do mês seguinte
    primeiro_dia_proximo_mes = nova_data_obj.replace(day=1)
    ultimo_dia = (primeiro_dia_proximo_mes + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Ajusta para o último dia do mês se necessário e limita o dia para 28
    nova_data_obj = min(ultimo_dia, nova_data_obj.replace(day=28))

    return nova_data_obj


def mes_referencia(numero):
    meses = {
        1: 'janeiro',
        2: 'fevereiro',
        3: 'março',
        4: 'abril',
        5: 'maio',
        6: 'junho',
        7: 'julho',
        8: 'agosto',
        9: 'setembro',
        10: 'outubro',
        11: 'novembro',
        12: 'dezembro'
    }
    return meses.get(numero, 'Mês inválido')


def q_usuarios_empresa(id_empresa):
    # Verifica se o id da empresa é válido
    empresa = db.empresa(id_empresa)
    if empresa is None:
        return None  # Retorna None se o id da empresa não existir

    # Consulta o número de usuários associados a essa empresa
    query = ((db.usuario_empresa.empresa == id_empresa)&((db.usuario_empresa.usuario != 1)))
    numero_usuarios = db(query).count()

    return numero_usuarios


def soma_registros_por_classificacao(id_classificacao, index=0):
    # Verifica se o id da classificação é válido
    classificacao = db.classificacao(id_classificacao)
    if classificacao is None:
        return None  # Retorna None se o id da classificação não existir

    # Obtém o período de datas com base no índice fornecido
    primeiro_dia, ultimo_dia = primeiro_ultimo_dia_do_mes(index)

    # Consulta a soma dos registros financeiros associados a essa classificação e dentro do período
    query = (db.registro_financeiro.classificacao == id_classificacao) & (db.registro_financeiro.data_vencimento >= primeiro_dia) & (db.registro_financeiro.data_vencimento <= ultimo_dia) & (db.registro_financeiro.liquidado == True)
    
    soma_registros = db(query).select(db.registro_financeiro.valor.sum()).first()[db.registro_financeiro.valor.sum()]

    return soma_registros or 0  # Retorna 0 se não houver registros financeiros associados a essa classificação no período fornecido
