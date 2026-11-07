import os  
os.system('pip install --upgrade huggingface_hub')  
import gradio as gr  
from supabase import create_client  
SUPABASE_URL = 'https://supabase.co'  
SUPABASE_KEY = 'sb_publishable_kneViBo-K1niAdMIKApMoQ_forPnbxI'  
try:  
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)  
except:  
    supabase = None  
TARIFA_KWH = 0.844  
def calcular_e_salvar(nome, codigo, imps, peso, tempo, pr_f, pr_v):  
    if not nome or not codigo: return 'Erro', gr.update()  
    pot = 195 if imps == 'Bambu Lab A1' else 150 if imps == 'Bambu Lab A1 Mini' else 350  
    val = 3900 if imps == 'Bambu Lab A1' else 2700 if imps == 'Bambu Lab A1 Mini' else 9500  
    vid = 12000 if imps == 'Bambu Lab A1' else 10000 if imps == 'Bambu Lab A1 Mini' else 15000  
    c_m = peso * (pr_f / 1000.0)  
    c_e = ((pot / 1000.0) * (tempo / 60.0)) * TARIFA_KWH  
    c_d = (val / vid) * (tempo / 60.0)  
    tot = (c_m + c_e + c_d) * 1.05  
    rel = f'Custos:\\nMaterial: R$ {c_m:.2f}\\nEnergia: R$ {c_e:.2f}\\nTotal: R$ {tot:.2f}'  
    if pr_v > 0:  
        if supabase:  
            try:  
                supabase.table('produtos').insert({'codigo': codigo, 'nome': nome, 'preco_venda': pr_v}).execute()  
                st = 'Salvo!'  
            except: st = 'Erro Banco'  
        return rel, f'Lancado! {st}'  
    return rel, 'Aguardando'  
with gr.Blocks() as demo:  
    gr.Markdown('# WQL-Studio3D')  
    with gr.Row():  
        with gr.Column():  
            nome = gr.Textbox(label='Nome')  
            codigo = gr.Textbox(label='Codigo')  
            imps = gr.Dropdown(choices=['Bambu Lab A1', 'Bambu Lab A1 Mini', 'Snapmaker U1'], label='Impressora', value='Bambu Lab A1')  
            peso = gr.Number(label='Peso', value=100)  
            tempo = gr.Number(label='Tempo', value=60)  
            pr_f = gr.Number(label='Preco Filamento', value=120)  
            pr_v = gr.Number(label='Preco Venda', value=0)  
            btn = gr.Button('Calcular')  
        with gr.Column():  
            saida_c = gr.Textbox(label='Helena')  
            saida_a = gr.Textbox(label='Alex')  
    btn.click(fn=calcular_e_salvar, inputs=[nome, codigo, imps, peso, tempo, pr_f, pr_v], outputs=[saida_c, saida_a])  
demo.launch() 
