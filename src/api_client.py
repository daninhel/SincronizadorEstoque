import requests
from dotenv import load_dotenv
import os


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

def atualizarEstoqueLoja(id: int, nome: str, quantidade: int):
    """
    Atualiza a venda de um produto específico do estoque da loja
    """
    response = requests.patch(f"{URLAPISERVER}/loja/produto/venda/{id}", json={"produto": nome, "quantidade": quantidade}).json()
    return response

def atualizarEstoqueERP(id: int, nome: str, quantidade: int):
    """
    Atualiza a venda de um produto específico do estoque do ERP
    """
    response = requests.patch(f"{URLAPISERVER}/erp/produto/venda/{id}", json={"produto": nome, "quantidade": quantidade}).json()
    return response