import pandas as pd
import time
import json
import vertexai
import os
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel

# Carregar configurações
load_dotenv()

# --- CONFIGURAÇÕES DO GOOGLE CLOUD ---
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
INPUT_FILE = "data/leads_brutos.csv"
FINAL_FILE = "data/entrega_final_enriquecida.xlsx"

def init_vertex():
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID não definido no arquivo .env")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    return GenerativeModel("gemini-2.0-flash-001")

def enriquecer_com_ia(model, nome_agencia, link_perfil):
    """Utiliza IA para buscar dados oficiais via Grounding (Google Search)."""
    prompt = f"""
    Atue como um analista de dados especializado em inteligência imobiliária.
    Pesquise a agência "{nome_agencia}" em Faro, Portugal. Link de referência: {link_perfil}.
    
    Localize o Email oficial, Telefone atualizado (formato +351) e Endereço físico.
    
    Retorne ESTRITAMENTE um JSON:
    {{
        "Telefone": "número",
        "Email": "email",
        "Endereco": "endereço completo",
        "Website_Oficial": "url"
    }}
    Use "Não encontrado" para campos vazios.
    """
    
    try:
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        limpo = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(limpo)
    except:
        return None

def main():
    print("🧠 Iniciando Enriquecimento Cognitivo via Vertex AI...")
    model = init_vertex()

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erro: {INPUT_FILE} não encontrado.")
        return

    df = pd.read_csv(INPUT_FILE)
    novas_colunas = ['IA_Email', 'IA_Telefone', 'IA_Endereco', 'IA_Website']
    for col in novas_colunas:
        if col not in df.columns: df[col] = ""

    for index, row in df.iterrows():
        if str(row['IA_Email']) != "": continue # Pula os já processados

        print(f"🔍 Investigando [{index+1}/{len(df)}]: {row['Nome']}...", end=" ", flush=True)
        resultado = enriquecer_com_ia(model, row['Nome'], row['Link_Perfil'])
        
        if resultado:
            df.at[index, 'IA_Email'] = resultado.get('Email')
            df.at[index, 'IA_Telefone'] = resultado.get('Telefone')
            df.at[index, 'IA_Endereco'] = resultado.get('Endereco')
            df.at[index, 'IA_Website'] = resultado.get('Website_Oficial')
            print("Sucesso ✅")
        else:
            print("Falha na consulta ⚠️")

        # Salva backup a cada 5 consultas
        if index % 5 == 0:
            df.to_excel(FINAL_FILE, index=False)
        
        time.sleep(1) # Respeito às cotas da API

    df.to_excel(FINAL_FILE, index=False)
    print(f"\n🏆 Processo finalizado! Arquivo pronto: {FINAL_FILE}")

if __name__ == "__main__":
    main()