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
git clone https://github.com/Alan-DSA/calculadora-de-investimento-cdi.git

cd calculadora-de-investimento-cdi

Crie e ative um ambiente virtual (opcional):
python -m venv venv
source venv/bin/activate 

No Windows:
venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

▶️ Como Executar
python calculadra_CDI.py

Ao executar, a interface gráfica será exibida. Preencha os campos com o valor inicial, data inicial e final, e selecione a frequência desejada. Clique em "Gerar Relatório" para obter o PDF com os resultados.

Visualização do formulário:

![image](https://github.com/user-attachments/assets/5a36a1d9-9ad4-48d3-9e25-dc95877a472f)

Mensagem de saida do formulário:

![image](https://github.com/user-attachments/assets/1f62dda8-da81-456a-978f-9b4b71a368e5)

gráficos apresentados no pdf:

![image](https://github.com/user-attachments/assets/40ce6313-3a27-4565-8d0d-1de15e685340)

relatório gerado no pdf:

![image](https://github.com/user-attachments/assets/8638ef3d-3e4b-44ba-8f08-e6d5ae096729)




