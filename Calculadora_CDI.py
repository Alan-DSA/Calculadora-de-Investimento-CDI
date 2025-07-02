import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import requests
import pandas as pd

class CDIInvestmentCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora de Investimento CDI")
        self.root.geometry("500x400")
        self.setup_ui()
        
    def setup_ui(self):
        # Quadro principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Calculadora de Investimento CDI", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos de entrada
        ttk.Label(main_frame, text="Valor Inicial (R$):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.initial_value = ttk.Entry(main_frame)
        self.initial_value.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(main_frame, text="Data Inicial (DD/MM/AAAA):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.start_date = ttk.Entry(main_frame)
        self.start_date.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(main_frame, text="Data Final (DD/MM/AAAA):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.end_date = ttk.Entry(main_frame)
        self.end_date.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(main_frame, text="Frequência da Série:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.frequency = ttk.Combobox(main_frame, values=["Diária", "Mensal", "Anual"])
        self.frequency.set("Mensal")
        self.frequency.grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        # Botão de cálculo
        calculate_button = ttk.Button(main_frame, text="Gerar Relatório", command=self.generate_report)
        calculate_button.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Configurar pesos das colunas
        main_frame.columnconfigure(1, weight=1)
        
    def get_cdi_data(self, start_date, end_date):
        """Buscar dados do CDI na API do Banco Central"""
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter dados do CDI: {str(e)}")
            return None
    
    def calculate_investment(self, cdi_data, initial_value, frequency):
        """Calcular evolução do investimento com base nas taxas do CDI"""
        df = cdi_data.copy()
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df['valor'] = pd.to_numeric(df['valor']) / 100  # Converter para decimal
        
        # Calcular fator de retorno diário (assumindo 252 dias úteis por ano)
        df['fator_diario'] = (1 + df['valor']) ** (1/252)
        
        # Calcular retorno acumulado
        df['valor_acumulado'] = initial_value * df['fator_diario'].cumprod()
        
        # Reamostrar de acordo com a frequência
        if frequency == "Diária":
            result = df[['data', 'valor_acumulado']].copy()
        elif frequency == "Mensal":
            result = df.set_index('data').resample('M').last().reset_index()
            result = result[['data', 'valor_acumulado']]
        else:  # Anual
            result = df.set_index('data').resample('Y').last().reset_index()
            result = result[['data', 'valor_acumulado']]
        
        # Adicionar coluna de retorno
        result['retorno'] = result['valor_acumulado'].pct_change().fillna(0)
        
        return result
    
    def generate_report(self):
        """Gerar relatório em PDF com a evolução do investimento"""
        try:
            # Obter valores informados pelo usuário
            initial_value = float(self.initial_value.get().replace(',', '.'))
            start_date = self.start_date.get()
            end_date = self.end_date.get()
            frequency = self.frequency.get()
            
            # Validar datas
            start_date_dt = datetime.strptime(start_date, '%d/%m/%Y')
            end_date_dt = datetime.strptime(end_date, '%d/%m/%Y')
            
            if end_date_dt <= start_date_dt:
                messagebox.showerror("Erro", "Data final deve ser posterior à data inicial")
                return
                
            # Formatar datas para a API
            api_start_date = start_date_dt.strftime('%d/%m/%Y')
            api_end_date = end_date_dt.strftime('%d/%m/%Y')
            
            # Obter dados do CDI
            cdi_data = self.get_cdi_data(api_start_date, api_end_date)
            if cdi_data is None:
                return
                
            # Calcular investimento
            result = self.calculate_investment(cdi_data, initial_value, frequency)
            
            if result.empty:
                messagebox.showerror("Erro", "Nenhum dado encontrado para o período especificado")
                return
                
            # Criar arquivo PDF
            filename = f"Relatorio_CDI_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with PdfPages(filename) as pdf:
                # Criar figura para o relatório
                plt.figure(figsize=(11, 8))
                
                # Gráfico 1: Evolução do investimento
                plt.subplot(2, 1, 1)
                plt.plot(result['data'], result['valor_acumulado'])
                plt.title(f"Evolução do Investimento CDI ({frequency})\n{start_date} - {end_date}")
                plt.xlabel("Data")
                plt.ylabel("Valor (R$)")
                plt.grid(True)
                
                # Gráfico 2: Retornos
                plt.subplot(2, 1, 2)
                plt.bar(result['data'], result['retorno'] * 100)
                plt.title(f"Retornos {frequency}s")
                plt.xlabel("Data")
                plt.ylabel("Retorno (%)")
                plt.grid(True)
                
                plt.tight_layout()
                pdf.savefig()
                plt.close()
                
                # Criar página de texto com análise
                plt.figure(figsize=(11, 8))
                plt.axis('off')
                
                max_ret = result['retorno'].max()
                max_date = result.loc[result['retorno'] == max_ret, 'data'].iloc[0]
                total_return = (result['valor_acumulado'].iloc[-1] - initial_value) / initial_value * 100
                
                text_content = [
                    f"Relatório de Investimento CDI",
                    f"Período: {start_date} a {end_date}",
                    f"",
                    f"Valor Inicial: R$ {initial_value:,.2f}",
                    f"Valor Final: R$ {result['valor_acumulado'].iloc[-1]:,.2f}",
                    f"Retorno Total: {total_return:.2f}%",
                    f"",
                    f"Período mais rentável:",
                    f"Data: {max_date.strftime('%d/%m/%Y')}",
                    f"Retorno: {max_ret*100:.2f}%",
                    f"",
                    f"Frequência da série: {frequency}",
                    f"Data do relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                ]
                
                plt.text(0.1, 0.95, "\n".join(text_content), fontsize=12, verticalalignment='top')
                pdf.savefig()
                plt.close()
                
            messagebox.showinfo("Relatório Gerado", f"Relatório PDF gerado com sucesso:\n{filename}")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Verifique os valores informados: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CDIInvestmentCalculator()
    app.run()
