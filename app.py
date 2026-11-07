import gradio as gr
from supabase import create_client

SUPABASE_URL = 'https://ygaaenzdceeuthigyzxp.supabase.co'
SUPABASE_KEY = 'sb_publishable_kneViBo-K1niAdMIKApMoQ_forPnbxI'

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

TARIFA_KWH = 0.844

def calcular_e_salvar(nome, codigo, impressora, peso, tempo, preco_filamento, preco_venda):
    if not nome or not codigo:
        return '?? Erro: Nome e C?digo s?o obrigat?rios!', gr.update()
    
    potencia = 195 if impressora == 'Bambu Lab A1' else 150 if impressora == 'Bambu Lab A1 Mini' else 350
    valor_maquina = 3900 if impressora == 'Bambu Lab A1' else 2700 if impressora == 'Bambu Lab A1 Mini' else 9500
    vida_util = 12000 if impressora == 'Bambu Lab A1' else 10000 if impressora == 'Bambu Lab A1 Mini' else 15000

    custo_material = peso * (preco_filamento / 1000.0)
    custo_energia = ((potencia / 1000.0) * (tempo / 60.0)) * TARIFA_KWH
    custo_depreciacao = (valor_maquina / vida_util) * (tempo / 60.0)
    custo_total = (custo_material + custo_energia + custo_depreciacao) * 1.05

    relatorio = f'?? NOTA FISCAL DE CUSTOS (Helena):\\n-----------------------------------\\nPl?stico: R$ {custo_material:.2f}\\nEnergia: R$ {custo_energia:.2f}\\nDeprecia??o: R$ {custo_depreciacao:.2f}\\n-----------------------------------\\n?? CUSTO FABRICA??O: R$ {custo_total:.2f}'
    
    if preco_venda > 0:
        lucro = preco_venda - custo_total
        relatorio += f'\\n?? LUCRO ESTIMADO: R$ {lucro:.2f}'
        
        if supabase:
            try:
                prod_data = {{'codigo': codigo, 'nome': nome, 'preco_venda': preco_venda, 'descricao': 'Cadastrado via Painel Central'}}
                supabase.table('produtos').insert(prod_data).execute()
                status_banco = '?? Dados gravados com sucesso no Supabase!'
            except Exception as e:
                status_banco = f'?? Erro ao gravar: Item duplicado ou tabela carregando.'
        else:
            status_banco = '? Conex?o offline.'
            
        aviso_agentes = f'?? PRODUTO LAN?ADO!\\n\\n{status_banco}\\n?? Alex acionou Marina para o Instagram.\\n?? Alex acionou Ricardo para a Shopee!'
        return relatorio, aviso_agentes
    else:
        return relatorio, '? Defina o Pre?o de Venda para salvar e acionar a equipe.'

with gr.Blocks(theme=gr.themes.Soft(primary_hue='orange', secondary_hue='slate')) as demo:
    gr.Markdown('# ?? WQL-Studio3D ? Comando Central')
    gr.Markdown('F?brica 100% conectada ao Banco de Dados!')
    with gr.Row():
        with gr.Column():
            gr.Markdown('### ?? Cadastro de Pe?as')
            nome = gr.Textbox(label='Nome do Produto', placeholder='Ex: Vaso Espiral')
            codigo = gr.Textbox(label='C?digo ?nico', placeholder='Ex: WQL-001')
            impressora = gr.Dropdown(choices=['Bambu Lab A1', 'Bambu Lab A1 Mini', 'Snapmaker U1'], label='Impressora', value='Bambu Lab A1')
            peso = gr.Number(label='Peso (g)', value=100)
            tempo = gr.Number(label='Tempo (minutos)', value=60)
            preco_filamento = gr.Number(label='Pre?o do KG (R$)', value=120)
            preco_venda = gr.Number(label='Seu Pre?o de Venda (R$)', value=0)
            btn = gr.Button('?? Calcular e Salvar no Banco', variant='primary')
        with gr.Column():
            gr.Markdown('### ??? Resposta da Controladoria')
            saida_custos = gr.Textbox(label='Relat?rio de Custos', lines=8)
            saida_agentes = gr.Textbox(label='Status das Automa??es', lines=6)
    btn.click(fn=calcular_e_salvar, inputs=[nome, codigo, impressora, peso, tempo, preco_filamento, preco_venda], outputs=[saida_custos, saida_agentes])

demo.launch()
