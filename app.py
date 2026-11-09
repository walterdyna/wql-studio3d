import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='WQL-Studio3D - Sistema Sofia', page_icon='🪐', layout='wide')
st.title('🪐 Sistema Sofia - Comando Central WQL-Studio3D')
st.subheader('Gerenciamento Inteligente de Impressão 3D e Vendas')

SUPABASE_URL = 'https://supabase.co'
headers = {'apikey': 'sb_publishable_kneViBo-K1niAdMIKApMoQ_forPnbxI', 'Authorization': 'Bearer sb_publishable_kneViBo-K1niAdMIKApMoQ_forPnbxI', 'Content-Type': 'application/json'}

aba_painel, aba_kaleb, aba_clara = st.tabs(['📊 Painel Geral', '🧩 Kaleb (Produção)', '💬 Clara (Atendimento)'])
with aba_painel:
    st.header('Análise de Custos e Margens (Helena)')
    try:
        res = requests.get(SUPABASE_URL, headers=headers)
        if res.status_code == 200:
            data = res.json()
            if data: st.dataframe(pd.DataFrame(data))
            else: st.info('Nenhuma peça na fila.')
        else: st.info('Nenhuma peça na fila.')
    except Exception as e: st.error(f'Erro: {e}')
with aba_kaleb:
    st.header('Área do Kaleb')
    with st.form('f'):
        n = st.text_input('Nome do Modelo', value='Vaso Canelado')
        p = st.number_input('Peso (g)', value=150)
        t = st.number_input('Tempo (h)', value=4.5)
        if st.form_submit_button('🚀 Enviar'):
            payload = {'peso_gramas': int(p), 'tempo_impressao_horas': float(t), 'status_producao': 'Aguardando Impressão'}
            res = requests.post(SUPABASE_URL, headers=headers, json=payload)
            if res.status_code < 300: st.success('🔥 Enviado com sucesso ao Supabase!')
            else: st.error(f'Erro ao enviar: Código {res.status_code}')
with aba_clara:
    st.header('💬 Central de Vendas da Clara')
    st.write('Gere mensagens prontas de orçamento e vendas para disparar direto no WhatsApp do cliente!')
    txt = 'Olá! Seguem os detalhes do seu pedido da WQL-Studio3D. Fabricado com alta tecnologia de impressão 3D! ✨' 
    st.text_area('Copia o texto aqui:', txt, height=120)
    st.markdown('[🚀 Abrir e Enviar Direto no WhatsApp](https://wa.me)')