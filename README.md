# **🎯 AI-Powered Real Estate Lead Miner**

![Demonstração do Robô em Ação](demo.gif)

Sistema híbrido de **Data Mining** e **Inteligência Artificial** para prospecção automatizada de leads qualificados no setor imobiliário.

## **🎯 Objetivo**

Este projeto automatiza a captura e o enriquecimento de leads imobiliários, resolvendo o problema de dados incompletos em portais públicos. O sistema atua em duas fases: extração resiliente de dados brutos e enriquecimento cognitivo via IA para localizar emails e moradas oficiais.

**Destaques para Auditoria/Controle:**

* **Rastreabilidade:** Geração de logs e backups incrementais em CSV/Excel.  
* **Inteligência de Dados:** Uso de **Gemini 2.0 Flash** com *Google Search Grounding* para validação de contactos.  
* **Segurança:** Gestão de credenciais de API e URLs via variáveis de ambiente (.env).

## **🛠️ Funcionalidades**

* **Extração Automática:** Navegação completa no portal Idealista com bypass de cookies e paginação.  
* **Enriquecimento Cognitivo:** Localização de emails e websites oficiais via IA, reduzindo o trabalho manual de pesquisa.  
* **Bypass de Proteção:** Detecção inteligente de Captcha e emulação de comportamento humano.  
* **Exportação Empresarial:** Entrega de ficheiros prontos para uso em CRM ou campanhas de vendas.

## **⚙️ Tecnologias Utilizadas**

* **Linguagem:** Python 3.10+  
* **Automação:** Selenium Webdriver (Edge)  
* **Inteligência Artificial:** Google Vertex AI (Gemini 2.0 Flash)  
* **Data Science:** Pandas & Openpyxl  
* **Ambiente:** Python-dotenv

## **🚀 Instalação e Uso**

1. **Clone o repositório**  
   git clone \[https://github.com/jorgeluisunesp-gif/AI-RealEstate-LeadMiner.git\](https://github.com/jorgeluisunesp-gif/AI-RealEstate-LeadMiner.git)  
   cd AI-RealEstate-LeadMiner

2. **Instale as dependências**  
   pip install \-r requirements.txt

3. Configuração  
   Renomeie o ficheiro .env.example para .env e preencha com o seu GCP\_PROJECT\_ID.  
4. **Execute**  
   \# Fase 1: Coleta bruta  
   python 01\_scraper\_idealista.py

   \# Fase 2: Enriquecimento via IA  
   python 02\_enriquecimento\_ia.py

## **👨‍💻 Sobre o Autor**

**Jorge Luis Carneiro Junior**

Profissional com trajetória multidisciplinar, unindo experiência sólida na administração pública e tecnologia. Atualmente atua como **Auxiliar de Promotoria no Ministério Público de São Paulo (MPSP)**, com foco em fiscalização e legalidade de processos administrativos.

* **Formação:** Tecnólogo em Gestão Pública e Graduando em Bacharelado em Tecnologia da Informação.  
* **Especializações:** Pós-graduado em Direito Tributário, em Ciências Contábeis, Auditoria e Perícia Contábil e Auditoria e Controladoria no Setor Público.  
* **Expertise:** Desenvolvimento de soluções de automação para os setores jurídico, fiscal e de auditoria, aplicando Python e IA para otimização de fluxos de trabalho e inteligência de dados.

## **🛡️ Disclaimer Ético**

Este software foi desenvolvido para fins de **estudo e produtividade**. O autor recomenda o uso responsável da ferramenta, respeitando os termos de serviço das plataformas acessadas e as normas de proteção de dados (LGPD/GDPR).

## **📄 Licença**

Distribuído sob a licença MIT. Veja LICENSE para mais detalhes.