    gr.Markdown('# ?? WQL-Studio3D — Comando Central')
with gr.Blocks(theme=gr.themes.Soft(primary_hue='orange', secondary_hue='slate')) as demo:
    return rel, '? Defina o preço de venda para salvar.'
        return rel, f'?? LANÇADO!\\n{st}\\n?? Marina e Ricardo acionados!'
        else: st = '? Offline.'
            except: st = '?? Erro ou item duplicado.'
                st = '?? Gravado no Supabase!'
                supabase.table('produtos').insert({'codigo': codigo, 'nome': nome, 'preco_venda': pr_v, 'descricao': 'Painel Central'}).execute()
            try:
        if supabase:
    if pr_v > 0:
    rel = f'?? CUSTOS:\\nMaterial: R$ {c_m:.2f}\\nEnergia: R$ {c_e:.2f}\\nDesgaste: R$ {c_d:.2f}\\n?? TOTAL: R$ {tot:.2f}'
    tot = (c_m + c_e + c_d) * 1.05
    c_d = (val / vid) * (tempo / 60.0)
    c_e = ((pot / 1000.0) * (tempo / 60.0)) * TARIFA_KWH
    c_m = peso * (pr_f / 1000.0)
    vid = 12000 if imps == 'Bambu Lab A1' else 10000 if imps == 'Bambu Lab A1 Mini' else 15000
    val = 3900 if imps == 'Bambu Lab A1' else 2700 if imps == 'Bambu Lab A1 Mini' else 9500
    pot = 195 if imps == 'Bambu Lab A1' else 150 if imps == 'Bambu Lab A1 Mini' else 350
    if not nome or not codigo: return '?? Erro: Dados faltantes!', gr.update()
def calcular_e_salvar(nome, codigo, imps, peso, tempo, pr_f, pr_v):
