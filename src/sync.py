import time
from api_client import retornarEstoqueERP, retornarEstoqueLoja, atualizarEstoqueLoja, atualizarEstoqueERP
from utils.logger import logger

def sincronizarEstoque(prioridade: str = "ERP"):
    """
    Compara o estoque entre ERP e Loja e realiza a sincronização.
    Prioridade padrão: 'ERP' (atualiza Loja com o estoque do ERP).
    """
    logger.info("=== Iniciando ciclo de sincronização de estoque ===")
    
    try:
        produtos_erp = retornarEstoqueERP()
        produtos_loja = retornarEstoqueLoja()
    except Exception as e:
        logger.error(f"Erro ao obter dados de estoque: {e}")
        return

    # Mapeia produtos da Loja por ID para busca rápida
    mapa_loja = {p['id']: p for p in produtos_loja}
    mapa_erp = {p['id']: p for p in produtos_erp}

    total_divergencias = 0
    total_atualizados = 0

    for id_produto, produto_erp in mapa_erp.items():
        if id_produto not in mapa_loja:
            logger.warning(f"Produto ID {id_produto} ('{produto_erp['produto']}') presente no ERP mas não encontrado na Loja.")
            continue

        produto_loja = mapa_loja[id_produto]
        qtd_erp = produto_erp['quantidade']
        qtd_loja = produto_loja['quantidade']
        nome_produto = produto_erp['produto']

        if qtd_erp != qtd_loja:
            total_divergencias += 1
            logger.warning(
                f"Divergência encontrada - ID {id_produto} ('{nome_produto}'): "
                f"ERP={qtd_erp} vs Loja={qtd_loja}"
            )

            if prioridade.upper() == "ERP":
                logger.info(f"Sincronizando: Atualizando Loja para {qtd_erp} unidades (prioridade ERP)...")
                res = atualizarEstoqueLoja(id_produto, qtd_erp)
                if res.get("status") == 200:
                    total_atualizados += 1
                    logger.info(f"Loja atualizada com sucesso para o produto ID {id_produto}.")
                else:
                    logger.error(f"Falha ao atualizar Loja para o produto ID {id_produto}: {res}")

            elif prioridade.upper() == "LOJA":
                logger.info(f"Sincronizando: Atualizando ERP para {qtd_loja} unidades (prioridade LOJA)...")
                res = atualizarEstoqueERP(id_produto, qtd_loja)
                if res.get("status") == 200:
                    total_atualizados += 1
                    logger.info(f"ERP atualizado com sucesso para o produto ID {id_produto}.")
                else:
                    logger.error(f"Falha ao atualizar ERP para o produto ID {id_produto}: {res}")

    logger.info(
        f"Ciclo concluído. Divergências detectadas: {total_divergencias} | "
        f"Atualizações realizadas: {total_atualizados}"
    )

def executarLoopSincronizacao(intervalo_segundos: int = 10, prioridade: str = "ERP"):
    """
    Executa a sincronização periodicamente a cada 'intervalo_segundos'.
    """
    logger.info(f"Iniciando serviço contínuo de sincronização (intervalo: {intervalo_segundos}s)...")
    try:
        while True:
            sincronizarEstoque(prioridade=prioridade)
            time.sleep(intervalo_segundos)
    except KeyboardInterrupt:
        logger.info("Serviço de sincronização finalizado pelo usuário.")

if __name__ == "__main__":
    sincronizarEstoque(prioridade="ERP")