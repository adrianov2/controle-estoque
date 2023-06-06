import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from PIL import Image, ImageTk


class Estoque:
    def __init__(self):
        self.produtos = {
            'agua': {
                'quantidade': 0,
                'vendidos': 0
            },
            'gas': {
                'quantidade': 0,
                'vendidos': 0
            }
        }
        self.caixa_agua = {
            'dinheiro': 0,
            'cartao': 0,
            'vale_gas': 0
        }
        self.caixa_gas = {
            'dinheiro': 0,
            'cartao': 0,
            'vale_gas': 0
        }

    def entrada_produto(self, produto, quantidade):
        self.produtos[produto]['quantidade'] += quantidade

    def saida_produto(self, produto, quantidade, forma_pagamento):
        if self.produtos[produto]['quantidade'] >= quantidade:
            self.produtos[produto]['quantidade'] -= quantidade
            self.produtos[produto]['vendidos'] += quantidade
            if produto == 'agua':
                if forma_pagamento == '1':
                    self.caixa_agua['dinheiro'] += quantidade
                elif forma_pagamento == '2':
                    self.caixa_agua['cartao'] += quantidade
            elif produto == 'gas':
                if forma_pagamento == '1':
                    self.caixa_gas['dinheiro'] += quantidade
                elif forma_pagamento == '2':
                    self.caixa_gas['cartao'] += quantidade
                elif forma_pagamento == '3':
                    self.caixa_gas['vale_gas'] += quantidade
            return True
        else:
            return False

    def obter_quantidade(self, produto):
        return self.produtos[produto]['quantidade']

    def obter_quantidade_vendida(self, produto):
        return self.produtos[produto]['vendidos']

    def obter_total_caixa(self, produto, forma_pagamento):
        if produto == 'agua':
            return self.caixa_agua[forma_pagamento]
        elif produto == 'gas':
            return self.caixa_gas[forma_pagamento]


class EstoqueGUI:
    def __init__(self, estoque):
        self.estoque = estoque
        self.window = tk.Tk()
        self.window.title("Controle de Estoque")
        self.window.geometry("700x400")
        self.window.resizable(False, False)

        # Carregar as imagens
        imagem_agua = Image.open("agua.jpg")
        imagem_gas = Image.open("gas.jpg")

        # Redimensionar as imagens para um tamanho adequado
        imagem_agua = imagem_agua.resize((100, 100))
        imagem_gas = imagem_gas.resize((100, 100))

        # Converter as imagens para o formato suportado pelo tkinter
        self.imagem_agua_tk = ImageTk.PhotoImage(imagem_agua)
        self.imagem_gas_tk = ImageTk.PhotoImage(imagem_gas)

        # Estilo para os widgets
        style = ttk.Style()
        style.configure("TFrame", background="#E1E1E1")
        style.configure("TLabel", background="#E1E1E1", foreground="#333333", font=("Arial", 12))
        style.configure("TButton", background="#4CAF50", foreground="white", font=("Arial", 12))

        self.frame_agua = ttk.Frame(self.window, style="TFrame")
        self.frame_agua.pack(pady=10)
        self.lbl_agua_imagem = ttk.Label(self.frame_agua, image=self.imagem_agua_tk)
        self.lbl_agua_imagem.grid(row=0, column=0, padx=10)
        self.lbl_agua_quantidade = ttk.Label(self.frame_agua, text="Quantidade: {}".format(self.estoque.obter_quantidade('agua')), style="TLabel")
        self.lbl_agua_quantidade.grid(row=0, column=1, padx=10)
        self.lbl_agua_vendidos = ttk.Label(self.frame_agua, text="Vendidos: {}".format(self.estoque.obter_quantidade_vendida('agua')), style="TLabel")
        self.lbl_agua_vendidos.grid(row=0, column=2, padx=10)
        self.btn_agua_entrada = ttk.Button(self.frame_agua, text="Entrada", command=self.entrada_agua, style="TButton")
        self.btn_agua_entrada.grid(row=0, column=5, padx=10)
        self.btn_agua_saida = ttk.Button(self.frame_agua, text="Saída", command=self.saida_agua, style="TButton")
        self.btn_agua_saida.grid(row=0, column=6, padx=10)

        self.frame_gas = ttk.Frame(self.window, style="TFrame")
        self.frame_gas.pack(pady=10)
        self.lbl_gas_imagem = ttk.Label(self.frame_gas, image=self.imagem_gas_tk)
        self.lbl_gas_imagem.grid(row=0, column=0, padx=10)
        self.lbl_gas_quantidade = ttk.Label(self.frame_gas, text="Quantidade: {}".format(self.estoque.obter_quantidade('gas')), style="TLabel")
        self.lbl_gas_quantidade.grid(row=0, column=1, padx=10)
        self.lbl_gas_vendidos = ttk.Label(self.frame_gas, text="Vendidos: {}".format(self.estoque.obter_quantidade_vendida('gas')), style="TLabel")
        self.lbl_gas_vendidos.grid(row=0, column=2, padx=10)
        self.btn_gas_entrada = ttk.Button(self.frame_gas, text="Entrada", command=self.entrada_gas, style="TButton")
        self.btn_gas_entrada.grid(row=0, column=5, padx=10)
        self.btn_gas_saida = ttk.Button(self.frame_gas, text="Saída", command=self.saida_gas, style="TButton")
        self.btn_gas_saida.grid(row=0, column=6, padx=10)

        self.frame_botoes = ttk.Frame(self.window, style="TFrame")
        self.frame_botoes.pack(pady=10)
        self.btn_imprimir_relatorio = ttk.Button(self.frame_botoes, text="Imprimir Relatório", command=self.imprimir_relatorio, style="TButton")
        self.btn_imprimir_relatorio.grid(row=0, column=0, padx=10)

    def entrada_agua(self):
        quantidade = simpledialog.askinteger("Entrada de Água", "Digite a quantidade de água:")
        if quantidade:
            self.estoque.entrada_produto('agua', quantidade)
            self.lbl_agua_quantidade.config(text="Quantidade: {}".format(self.estoque.obter_quantidade('agua')))
            messagebox.showinfo("Entrada de Água", "Entrada de água registrada com sucesso.")

    def saida_agua(self):
        quantidade = simpledialog.askinteger("Saída de Água", "Digite a quantidade de água:")
        if quantidade:
            forma_pagamento = simpledialog.askinteger("Saída de Água", "Selecione a forma de pagamento:\n1 - Dinheiro\n2 - Cartão")
            if forma_pagamento:
                if self.estoque.saida_produto('agua', quantidade, str(forma_pagamento)):
                    self.lbl_agua_quantidade.config(text="Quantidade: {}".format(self.estoque.obter_quantidade('agua')))
                    self.lbl_agua_vendidos.config(text="Vendidos: {}".format(self.estoque.obter_quantidade_vendida('agua')))
                    messagebox.showinfo("Saída de Água", "Saída de água registrada com sucesso.")
                else:
                    messagebox.showerror("Saída de Água", "Quantidade insuficiente de água em estoque.")

    def entrada_gas(self):
        quantidade = simpledialog.askinteger("Entrada de Gás", "Digite a quantidade de gás:")
        if quantidade:
            self.estoque.entrada_produto('gas', quantidade)
            self.lbl_gas_quantidade.config(text="Quantidade: {}".format(self.estoque.obter_quantidade('gas')))
            messagebox.showinfo("Entrada de Gás", "Entrada de gás registrada com sucesso.")

    def saida_gas(self):
        quantidade = simpledialog.askinteger("Saída de Gás", "Digite a quantidade de gás:")
        if quantidade:
            forma_pagamento = simpledialog.askinteger("Saída de Gás", "Selecione a forma de pagamento:\n1 - Dinheiro\n2 - Cartão\n3 - Vale Gas")
            if forma_pagamento:
                if self.estoque.saida_produto('gas', quantidade, str(forma_pagamento)):
                    self.lbl_gas_quantidade.config(text="Quantidade: {}".format(self.estoque.obter_quantidade('gas')))
                    self.lbl_gas_vendidos.config(text="Vendidos: {}".format(self.estoque.obter_quantidade_vendida('gas')))
                    messagebox.showinfo("Saída de Gás", "Saída de gás registrada com sucesso.")
                else:
                    messagebox.showerror("Saída de Gás", "Quantidade insuficiente de gás em estoque.")

    def imprimir_relatorio(self):
        total_vendido_agua = self.estoque.obter_quantidade_vendida('agua')
        total_vendido_gas = self.estoque.obter_quantidade_vendida('gas')
        total_dinheiro_agua = self.estoque.obter_total_caixa('agua', 'dinheiro')
        total_cartao_agua = self.estoque.obter_total_caixa('agua', 'cartao')
        total_dinheiro_gas = self.estoque.obter_total_caixa('gas', 'dinheiro')
        total_cartao_gas = self.estoque.obter_total_caixa('gas', 'cartao')
        total_vale_gas_gas = self.estoque.obter_total_caixa('gas', 'vale_gas')
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        relatorio = f"Relatório de Vendas - {data_hora}\n\n"
        relatorio += f"Água:\n"
        relatorio += f"  Quantidade vendida: {total_vendido_agua}\n"
        relatorio += f"  Total recebido em dinheiro (Água): {total_dinheiro_agua}\n"
        relatorio += f"  Total recebido em cartão (Água): {total_cartao_agua}\n\n"
        relatorio += f"Gás:\n"
        relatorio += f"  Quantidade vendida: {total_vendido_gas}\n"
        relatorio += f"  Total recebido em dinheiro (Gás): {total_dinheiro_gas}\n"
        relatorio += f"  Total recebido em cartão (Gás): {total_cartao_gas}\n"
        relatorio += f"  Total recebido em vale-gás (Gás): {total_vale_gas_gas}\n"

        with open("relatorio.txt", "w") as file:
            file.write(relatorio)

        messagebox.showinfo("Impressão de Relatório", "Relatório de vendas impresso com sucesso.")

    def run(self):
        self.window.mainloop()


estoque = Estoque()
estoque_gui = EstoqueGUI(estoque)
estoque_gui.run()
