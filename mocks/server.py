
from fastapi import FastAPI
import uvicorn
import json
import os
import threading

ARQUIVO_DADOS = os.path.join(os.path.dirname(__file__), "data.json")
lock_dados = threading.Lock()

with open(ARQUIVO_DADOS, "r", encoding="utf-8") as file:
    data = json.load(file)
    
dataERP = data['listaProdutosEstoqueERP']
dataLoja = data['listaProdutosEstoqueLoja']

def salvarDados():
    """
    Persiste o estado atual de dataERP e dataLoja de volta no data.json de forma thread-safe.
    """
    with lock_dados:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

app = FastAPI()

@app.get("/erp/produtos", status_code=200)
async def retornarProdutosERP():
    """
    Retorna todos os produtos do estoque do ERP
    """
    response = dataERP
    return response

@app.get("/loja/produtos", status_code=200)
async def retornarProdutosLoja():
    """
    Retorna todos os produtos do estoque da loja
    """
    response = dataLoja
    return response

@app.get("/erp/produto/{id}", status_code=200)
async def retornarProdutoERP(id: int):
    """
    Retorna um produto específico do estoque do ERP
    """
    if id:
        response = dataERP
        produto = filter(lambda produto: produto['id'] == id, response)
        if produto:
            produto = list(produto)
            response = {"status": 200, "produto": produto}
        else:
            response = {"status": 404, "mensagem": "Produto não encontrado"}
    else:
        response = {"status": 400, "mensagem": "ID do produto não fornecido"}
    
    return response

@app.get("/loja/produto/{id}")
async def retornarProdutoLoja(id: int):
    """
    Retorna um produto específico do estoque da loja
    """
    if id:
        response = dataLoja
        produto = filter(lambda produto: produto['id'] == id, response)
        if produto:
            produto = list(produto)
            response = {"status": 200, "produto": produto}
        else:
            response = {"status": 404, "mensagem": "Produto não encontrado"}
    else:
        response = {"status": 400, "mensagem": "ID do produto não fornecido"}

    return response

@app.patch("/loja/produto/venda/{id}", status_code=200)
async def vendaLoja(id: int, quantidade: int):
    """
    Atualiza a venda de um produto específico do estoque da loja
    """
    if quantidade <= 0:
        return {"status": 400, "mensagem": "Quantidade inválida para venda"}

    produtos = list(filter(lambda produto: produto['id'] == id, dataLoja))
    
    if produtos:
        produto = produtos[0]
        if produto['quantidade'] >= quantidade:
            produto['quantidade'] -= quantidade
            salvarDados()
            response = {"status": 200, "mensagem": "Venda realizada com sucesso"}
        else:
            response = {"status": 400, "mensagem": "Quantidade insuficiente em estoque da loja"}
    else:
        response = {"status": 404, "mensagem": "Produto não encontrado"}
    
    return response

@app.patch("/erp/produto/venda/{id}", status_code=200)
async def vendaERP(id: int, quantidade: int):
    """
    Atualiza a venda de um produto específico do estoque do ERP
    """
    if quantidade <= 0:
        return {"status": 400, "mensagem": "Quantidade inválida para venda"}

    produtos = list(filter(lambda produto: produto['id'] == id, dataERP))
    
    if produtos:
        produto = produtos[0]
        if produto['quantidade'] >= quantidade:
            produto['quantidade'] -= quantidade
            salvarDados()
            response = {"status": 200, "mensagem": "Venda realizada com sucesso"}
        else:
            response = {"status": 400, "mensagem": "Quantidade insuficiente em estoque do ERP"}
    else:
        response = {"status": 404, "mensagem": "Produto não encontrado"}
    
    return response

@app.patch("/loja/estoque/produto/{id}/atualizar", status_code=200)
async def atualizarProdutoLoja(id: int, quantidade: int):
    """
    Atualiza a quantidade em estoque de um produto específico da loja
    """
    if quantidade < 0:
        return {"status": 400, "mensagem": "Quantidade inválida para estoque"}

    produtos = list(filter(lambda produto: produto['id'] == id, dataLoja))
    
    if produtos:
        produto = produtos[0]
        produto['quantidade'] = quantidade
        salvarDados()
        response = {"status": 200, "mensagem": "Estoque da loja atualizado com sucesso"}
    else:
        response = {"status": 404, "mensagem": "Produto não encontrado"}
    
    return response

@app.patch("/erp/estoque/produto/{id}/atualizar", status_code=200)
async def atualizarProdutoERP(id: int, quantidade: int):
    """
    Atualiza a quantidade em estoque de um produto específico do ERP
    """
    if quantidade < 0:
        return {"status": 400, "mensagem": "Quantidade inválida para estoque"}

    produtos = list(filter(lambda produto: produto['id'] == id, dataERP))
    
    if produtos:
        produto = produtos[0]
        produto['quantidade'] = quantidade
        salvarDados()
        response = {"status": 200, "mensagem": "Estoque do ERP atualizado com sucesso"}
    else:
        response = {"status": 404, "mensagem": "Produto não encontrado"}
    
    return response

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=4000, reload=True, reload_includes=["*.py"])


