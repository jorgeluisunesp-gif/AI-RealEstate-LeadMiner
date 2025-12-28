import time
import pandas as pd
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- CONFIGURAÇÃO VIA AMBIENTE ---
TARGET_URL = os.getenv("IDEALISTA_URL", "https://www.idealista.pt/agencias-imobiliarias/faro-distrito/imobiliarias")
OUTPUT_CSV = "data/leads_brutos.csv"
OUTPUT_EXCEL = "data/leads_backup.xlsx"

def setup_driver():
    """Configura o navegador Edge de forma resiliente."""
    caminho_driver = os.path.join(os.getcwd(), "msedgedriver.exe") 
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    if not os.path.exists(caminho_driver):
        raise FileNotFoundError("O msedgedriver.exe deve estar na raiz do projeto.")
    
    service = Service(executable_path=caminho_driver)
    return webdriver.Edge(service=service, options=options)

def main():
    print("🚀 Iniciando Extração: Mapeamento de Agências no Idealista...")
    
    if not os.path.exists("data"):
        os.makedirs("data")

    driver = setup_driver()
    driver.get(TARGET_URL)
    time.sleep(4)

    # Aceitar Cookies se aparecerem
    try:
        driver.find_element(By.ID, "didomi-notice-agree-button").click()
    except:
        pass

    leads = []
    links_unicos = set()
    pagina = 1

    try:
        while True:
            print(f"📄 Processando Página {pagina}...", end=" ", flush=True)
            elementos = driver.find_elements(By.CSS_SELECTOR, "span.agency-name a")
            
            cont_novos = 0
            for elem in elementos:
                link = elem.get_attribute("href")
                nome = elem.text.strip() or elem.get_attribute("textContent").strip()

                if link and link not in links_unicos:
                    links_unicos.add(link)
                    leads.append({"Nome": nome, "Link_Perfil": link})
                    cont_novos += 1
            
            print(f"({cont_novos} novos leads)")
            
            # Navegação para próxima página
            try:
                botao_prox = driver.find_element(By.CSS_SELECTOR, "li.next a")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_prox)
                time.sleep(1)
                botao_prox.click()
                pagina += 1
                time.sleep(3)
            except:
                print("🏁 Fim da paginação encontrado.")
                break

    except KeyboardInterrupt:
        print("\n⚠️ Interrupção manual detectada. Salvando progresso...")

    # Extração de detalhes (Telefone/Site)
    print("\n🔍 Iniciando Fase de Detalhamento...")
    for i, lead in enumerate(leads):
        print(f"[{i+1}/{len(leads)}] Extraindo: {lead['Nome']}...", end=" ", flush=True)
        try:
            driver.get(lead['Link_Perfil'])
            if "captcha" in driver.title.lower():
                input("\n🚨 Captcha detectado! Resolva-o no navegador e pressione Enter aqui...")
            
            lead['Telefone_Base'] = "Não encontrado"
            try:
                driver.execute_script("document.querySelector('.show-phone').click()")
                time.sleep(0.3)
                lead['Telefone_Base'] = driver.find_element(By.CSS_SELECTOR, ".hidden-contact-phones_formatted-phone").text
            except: pass
            
            try:
                lead['Website'] = driver.find_element(By.CSS_SELECTOR, "a.icon-new-tab").get_attribute("href")
            except: 
                lead['Website'] = ""
            
            print("OK")
        except Exception as e:
            print(f"Erro: {e}")
        
        # Salvamento incremental de segurança
        if i % 10 == 0:
            pd.DataFrame(leads).to_csv(OUTPUT_CSV, index=False)

    # Salvamento Final
    df = pd.DataFrame(leads)
    df.to_csv(OUTPUT_CSV, index=False)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"\n✅ Concluído! Dados salvos em {OUTPUT_CSV}")
    driver.quit()

if __name__ == "__main__":
    main()