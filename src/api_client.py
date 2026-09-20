import requests
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv("../.env")
URLAPISERVER = os.getenv("URLAPISERVER")

print(f"URLAPISERVER: {URLAPISERVER}")

def retornarEstoqueERP():
    """
    Retorna todos os produtos do estoque do ERP
    """
    response = requests.get(f"{URLAPISERVER}/erp/produtos").json()
    return response

def retornarEstoqueLoja():
    """
    Retorna todos os produtos do estoque da loja
    """
    response = requests.get(f"{URLAPISERVER}/loja/produtos").json()
    return response

def retornarProdutoERP(id):
    """
    Retorna um produto específico do estoque do ERP
    """
    response = requests.get(f"{URLAPISERVER}/erp/produto/{id}").json()
    return response

def retornarProdutoLoja(id):
    """
    Retorna um produto específico do estoque da loja
    """
    response = requests.get(f"{URLAPISERVER}/loja/produto/{id}").json()
    return response

def atualizarEstoqueLoja(id: int, quantidade: int):
    """
    Atualiza a quantidade em estoque de um produto específico da loja
    """
    response = requests.patch(f"{URLAPISERVER}/loja/estoque/produto/{id}/atualizar", params={"quantidade": quantidade}).json()
    return response

def atualizarEstoqueERP(id: int, quantidade: int):
    """
    Atualiza a quantidade em estoque de um produto específico do ERP
    """
    response = requests.patch(f"{URLAPISERVER}/erp/estoque/produto/{id}/atualizar", params={"quantidade": quantidade}).json()
    return response

def vendaLoja(id: int, quantidade: int):
    """
    Realiza a venda de um produto específico no estoque da loja
    """
    response = requests.patch(f"{URLAPISERVER}/loja/produto/venda/{id}", params={"quantidade": quantidade}).json()
    return response

def vendaERP(id: int, quantidade: int):
    """
    Realiza a venda de um produto específico no estoque do ERP
    """
    response = requests.patch(f"{URLAPISERVER}/erp/produto/venda/{id}", params={"quantidade": quantidade}).json()
    return response