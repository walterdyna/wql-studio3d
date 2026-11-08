import gradio as gr
from supabase import create_client
import google.generativeai as genai

SUPABASE_URL = 'https://supabase.co'
SUPABASE_KEY = 'sb_publishable_kneViBo-K1niAdMIKApMoQ_forPnbxI'

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

TARIFA_KWH = 0.844

def calcular_e_marina(nome, codigo, imps, peso, tempo, pr_f, pr_v):
    if not nome or not codigo: return 'Erro: Dados faltantes!', gr.update()
    pot = 195 if imps == 'Bambu Lab A1' else 150 if imps == 'Bambu Lab A1 Mini' else 350
    val = 3900 if imps == 'Bambu Lab A1' else 2700 if imps == 'Bambu Lab A1 Mini' else 9500
    vid = 12000 if imps == 'Bambu Lab A1' else 10000 if imps == 'Bambu Lab A1 Mini' else 15000
    c_m = peso * (pr_f / 1000.0)
    c_e = ((pot / 1000.0) * (tempo / 60.0)) * TARIFA_KWH
    c_d = (val / vid) * (tempo / 60.0)
    tot = (c_m + c_e + c_d) * 1.05
    rel = f'📊 CUSTOS:\\nMaterial: R$ {c_m:.2f}\\nEnergia: R$ {c_e:.2f}\\nDesgaste: R$ {c_d:.2f}\\n💰 TOTAL: R$ {tot:.2f}'
    if pr_v > 0:
        st = 'Offline'
        if supabase:
            try:
                supabase.table('produtos').insert({'codigo': codigo, 'nome': nome, 'preco_venda': pr_v}).execute()
                st = '💾 Gravado no Supabase!'
            except: st = '⚠️ Erro ao gravar'
        copy_insta = f'📢 PROPOSTA DE LEGENDAS DA MARINA:\\n\\n✨ NOVIDADE NA AMOÊ DECOR! ✨\\n\\nOlha que espetáculo o nosso novo {nome}! Focado em design moderno e acabamento impecável em impressão 3D de alta resolução.\\n\\n💎 Exclusividade, sofisticação e o toque moderno que a sua casa merece.\\n🛒 Garanta o seu via direct pelo código único: {codigo}\\n\\n#impressao3d #decoracaointeriores #design #amoedecor #artesanatodeluxo'
        return rel, f'🟢 LANÇADO!\\n{st}\\n\\n{copy_insta}'
    return rel, '⏳ Defina o preço de venda para acionar a Marina.'

with gr.Blocks(theme=gr.themes.Soft(primary_hue='orange', secondary_hue='slate')) as demo:
    gr.Markdown('# 🪐 WQL-Studio3D — Comando Central')
    with gr.Row():
        with gr.Column():
            gr.Markdown('### 📦 Cadastro de Peças')
            nome = gr.Textbox(label='Nome do Produto')
            codigo = gr.Textbox(label='Código Único')
            imps = gr.Dropdown(choices=['Bambu Lab A1', 'Bambu Lab A1 Mini', 'Snapmaker U1'], label='Impressora', value='Bambu Lab A1')
            peso = gr.Number(label='Peso (g)', value=100)
            tempo = gr.Number(label='Tempo (minutos)', value=60)
            pr_f = gr.Number(label='Preço do KG (R$)', value=120)
            pr_v = gr.Number(label='Preço de Venda (R$)', value=0)
            btn = gr.Button('🟢 Calcular e Acionar Equipe', variant='primary')
        with gr.Column():
            saida_c = gr.Textbox(label='Controladoria (Helena)', lines=6)
            saida_a = gr.Textbox(label='Agente de Marketing (Marina)', lines=12)
    btn.click(fn=calcular_e_marina, inputs=[nome, codigo, imps, peso, tempo, pr_f, pr_v], outputs=[saida_c, saida_a])
demo.launch()