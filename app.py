import gradio as gr

# Banco de dados temporário simulando as gavetas da Sofia enquanto conectamos o n8n
produtos_cadastrados = []
TARIFA_KWH = 0.844

def calcular_e_salvar(nome, codigo, impressora, peso, tempo, preco_filamento, preco_venda):
    if not nome or not codigo:
        return "⚠️ Erro: Preencha o nome e o código do produto!", gr.update()
    
    # Parâmetros definidos pela Helena para o cálculo industrial
    potencia = 195 if impressora == "Bambu Lab A1" else 150 if impressora == "Bambu Lab A1 Mini" else 350
    valor_maquina = 3900 if impressora == "Bambu Lab A1" else 2700 if impressora == "Bambu Lab A1 Mini" else 9500
    vida_util = 12000 if impressora == "Bambu Lab A1" else 10000 if impressora == "Bambu Lab A1 Mini" else 15000

    # Lógica Matemática da Helena Engine
    custo_material = peso * (preco_filamento / 1000.0)
    custo_energia = ((potencia / 1000.0) * (tempo / 60.0)) * TARIFA_KWH
    custo_depreciacao = (valor_maquina / vida_util) * (tempo / 60.0)
    custo_total = (custo_material + custo_energia + custo_depreciacao) * 1.05 # 5% perda

    # Relatório detalhado para o painel do chefe
    relatorio = f"""
    📊 NOTA FISCAL DE CUSTOS (Agente Helena):
    --------------------------------------------------
    Plástico Utilizado: R$ {custo_material:.2f}
    Energia Consumida: R$ {custo_energia:.2f}
    Desgaste da Máquina: R$ {custo_depreciacao:.2f}
    --------------------------------------------------
    💰 CUSTO TOTAL DE FABRICAÇÃO: R$ {custo_total:.2f}
    """
    
    if preco_venda > 0:
        lucro = preco_venda - custo_total
        relatorio += f"\n📈 LUCRO ESTIMADO POR PEÇA: R$ {lucro:.2f}"
        
        # Simula o Alex distribuindo as tarefas para Marina e Ricardo
        aviso_agentes = f"""
        🟢 PRODUTO LANÇADO COM SUCESSO!
        
        📢 Alex notificou Marina para criar a publicação do '{nome}' no Instagram.
        🛒 Alex notificou Ricardo para otimizar o anúncio de R$ {preco_venda:.2f} na Shopee e Mercado Livre!
        """
        return relatorio, aviso_agentes
    else:
        return relatorio, "⏳ Aguardando você definir o Preço de Venda para acionar Marina e Ricardo..."

# Construindo a interface moderna com fundo escuro (Tema Soft)
with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="slate")) as demo:
    gr.Markdown("# 🪐 WQL-Studio3D — Comando Central")
    gr.Markdown("Bem-vindo ao painel da sua fábrica inteligente, Chefe Walter!")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📦 Cadastro de Peças (Agente Sofia)")
            nome = gr.Textbox(label="Nome do Produto", placeholder="Ex: Vaso Espiral")
            codigo = gr.Textbox(label="Código Único", placeholder="Ex: WQL-001")
            impressora = gr.Dropdown(choices=["Bambu Lab A1", "Bambu Lab A1 Mini", "Snapmaker U1"], label="Selecione a Impressora", value="Bambu Lab A1")
            
            peso = gr.Number(label="Peso em Gramas (g)", value=100)
            tempo = gr.Number(label="Tempo de Impressão (em minutos)", value=60)
            preco_filamento = gr.Number(label="Preço do KG do Filamento (R$)", value=120)
            
            gr.Markdown("### 💰 Decisão Estratégica")
            preco_venda = gr.Number(label="Seu Preço de Venda (R$)", value=0)
            
            btn = gr.Button("🟢 Calcular e Enviar para os Agentes", variant="primary")
            
        with gr.Column():
            gr.Markdown("### 🎛️ Resposta da Controladoria (Agente Helena)")
            saida_custos = gr.Textbox(label="Relatório de Custos", lines=8)
            saida_agentes = gr.Textbox(label="Status das Automações (Agente Alex)", lines=6)

    btn.click(fn=calcular_e_salvar, inputs=[nome, codigo, impressora, peso, tempo, preco_filamento, preco_venda], outputs=[saida_custos, saida_agentes])

demo.launch()
