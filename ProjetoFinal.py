import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from fpdf import FPDF

class Funcionario:
    def __init__(self, nome, cpf, cargo):
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo

class CestaBasica:
    def __init__(self, nome, quantidade, funcionario):
        self.nome = nome
        self.quantidade = quantidade
        self.funcionario = funcionario

class ControleCestasBasicas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Controle de Cestas Básicas")

        self.funcionarios = []
        self.cestas = []
        self.valores_unitarios = {"Alimentação": 275, "Limpeza": 92}

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.lbl_nome = ttk.Label(self.frame, text="Nome:")
        self.entry_nome = ttk.Entry(self.frame)
        self.lbl_cargo = ttk.Label(self.frame, text="Cargo:")
        self.entry_cargo = ttk.Entry(self.frame)
        self.lbl_cpf = ttk.Label(self.frame, text="CPF:")
        self.entry_cpf = ttk.Entry(self.frame)
        self.lbl_nome_cesta = ttk.Label(self.frame, text="Nome da cesta básica:")
        self.combo_nome = ttk.Combobox(self.frame, values=["Alimentação", "Limpeza"])
        self.lbl_quantidade = ttk.Label(self.frame, text="Quantidade:")
        self.entry_quantidade = ttk.Entry(self.frame)
        self.btn_adicionar_funcionario = ttk.Button(self.frame, text="Adicionar Funcionário", command=self.adicionar_funcionario)
        self.btn_adicionar_cesta = ttk.Button(self.frame, text="Adicionar Cesta", command=self.adicionar_cesta)
        self.btn_salvar_pdf = ttk.Button(self.frame, text="Salvar em PDF", command=self.salvar_pdf)
        self.lbl_resultado = ttk.Label(self.frame, text="")

        self.lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        self.lbl_cargo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_cargo.grid(row=1, column=1, padx=5, pady=5)
        self.lbl_cpf.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_cpf.grid(row=2, column=1, padx=5, pady=5)
        self.btn_adicionar_funcionario.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_nome_cesta.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.combo_nome.grid(row=4, column=1, padx=5, pady=5)
        self.lbl_quantidade.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_quantidade.grid(row=5, column=1, padx=5, pady=5)
        self.btn_adicionar_cesta.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.btn_salvar_pdf.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_resultado.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def adicionar_funcionario(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        cargo = self.entry_cargo.get()

        funcionario = Funcionario(nome, cpf, cargo)
        self.funcionarios.append(funcionario)

        self.entry_nome.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)

    def adicionar_cesta(self):
        nome_cesta = self.combo_nome.get()
        quantidade = int(self.entry_quantidade.get())

        if not self.funcionarios:
            messagebox.showwarning("Aviso", "Adicione um funcionário primeiro.")
            return

        funcionario = self.funcionarios[-1]  # Pegar o último funcionário adicionado

        for cesta in self.cestas:
            if cesta.nome.lower() == nome_cesta.lower() and cesta.funcionario == funcionario:
                cesta.quantidade += quantidade
                break
        else:
            cesta = CestaBasica(nome_cesta, quantidade, funcionario)
            self.cestas.append(cesta)

        self.entry_quantidade.delete(0, tk.END)

    def salvar_pdf(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(0, 10, "Relatório de Cestas Básicas", ln=True, align='C')

        headers = ["Nome", "Cargo", "CPF", "Cesta Básica", "Quantidade", "Valor Total (R$)"]
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font("Arial", size=10, style='B')
        for header in headers:
            pdf.cell(40, 10, header, 1, 0, 'C', fill=True)
        pdf.ln()

        for cesta in self.cestas:
            pdf.set_fill_color(255, 255, 255)
            pdf.set_font("Arial", size=10)
            pdf.cell(40, 10, cesta.funcionario.nome, 1)
            pdf.cell(40, 10, cesta.funcionario.cargo, 1)
            pdf.cell(40, 10, cesta.funcionario.cpf, 1)
            pdf.cell(40, 10, cesta.nome, 1)
            pdf.cell(40, 10, str(cesta.quantidade), 1)
            valor_total = cesta.quantidade * self.valores_unitarios[cesta.nome]
            pdf.cell(40, 10, f"R${valor_total:.2f}", 1)
            pdf.ln()

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf.output(file_path)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ControleCestasBasicas()
    app.run()
