# Calculadora-de-Investimento-CDI

Aplicação interativa em Python com interface gráfica (GUI) desenvolvida em Tkinter que permite simular a evolução de um investimento indexado ao CDI com base em dados reais do Banco Central do Brasil (BCB). O relatório gerado inclui gráficos e informações detalhadas exportadas em um arquivo PDF.

🧰 Funcionalidades
Entrada de valor inicial e intervalo de datas.

Escolha da frequência da série histórica: diária, mensal ou anual.

Consulta automática da série histórica do CDI (código 4389 - BCB).

Cálculo da evolução do investimento ao longo do tempo.

Geração de relatório PDF contendo:

Gráfico da evolução do valor investido.

Gráfico dos retornos percentuais por período.

Informações analíticas do investimento.

🖥️ Tecnologias Utilizadas
Python 3.8+

Tkinter (GUI)

Matplotlib (visualização e PDF)

Pandas (manipulação de dados)

Requests (requisição de dados da API do BCB)

API de séries temporais do Banco Central do Brasil

Clone o repositório:
git clone https://github.com/seu-usuario/calculadora-investimento-cdi.git
cd calculadora-investimento-cdi

Crie e ative um ambiente virtual (opcional):
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Instale as dependências:
pip install -r requirements.txt

▶️ Como Executar
python cdi_calculator.py

Ao executar, a interface gráfica será exibida. Preencha os campos com o valor inicial, data inicial e final, e selecione a frequência desejada. Clique em "Gerar Relatório" para obter o PDF com os resultados.

📁 Estrutura do Projeto
calculadora-investimento-cdi/
│
├── calculadora_CDI.py       # Código principal com interface e lógica de cálculo
├── README.md               # Documentação do projeto
├── requirements.txt        # Lista de dependências (veja abaixo)
└── Relatorio_CDI_*.pdf     # Arquivos gerados com os relatórios


