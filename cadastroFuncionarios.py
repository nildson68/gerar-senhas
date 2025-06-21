import tkinter as tk
from tkinter import font, messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "employees.json"

class DateEntry(tk.Entry):
    """Custom Entry widget with a date mask for dd/mm/yyyy format."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.insert(0, "dd/mm/aaaa")
        self.config(fg="#9ca3af")  # Light gray placeholder color
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<KeyRelease>", self._on_key_release)

    def _on_focus_in(self, event):
        if self.get() == "dd/mm/aaaa":
            self.delete(0, tk.END)
            self.config(fg="#111827")

    def _on_focus_out(self, event):
        text = self.get()
        if not text:
            self.insert(0, "dd/mm/aaaa")
            self.config(fg="#9ca3af")
        else:
            if not self._validate_date_format(text):
                messagebox.showerror("Entrada Inválida", "Data deve ter o formato dd/mm/aaaa")
                self.focus_set()

    def _on_key_release(self, event):
        text = self.get()
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Tab"):
            return
        # Auto-insert slashes as user types
        clean_text = text.replace("/", "")
        new_text = ""
        for i, c in enumerate(clean_text):
            new_text += c
            if i == 1 or i == 3:
                new_text += "/"
        # Avoid recursive modification
        if new_text != text:
            self.delete(0, tk.END)
            self.insert(0, new_text)

    def _validate_date_format(self, text):
        try:
            datetime.strptime(text, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def get_date(self):
        text = self.get()
        if text == "dd/mm/aaaa":
            return ""
        return text

class DependentDialog(simpledialog.Dialog):
    """Dialog window for adding or editing a dependent."""

    def __init__(self, parent, title, dependent=None):
        self.dependent = dependent
        super().__init__(parent, title)

    def body(self, master):
        self.resizable(False, False)
        font_style = ("Inter", 12)
        tk.Label(master, text="Nome:", font=font_style).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_name = tk.Entry(master, font=font_style, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Data de Nascimento (dd/mm/aaaa):", font=font_style).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_dob = DateEntry(master, font=font_style, width=30)
        self.entry_dob.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Grau de Parentesco:", font=font_style).grid(row=2, column=0, sticky="e", pady=5)
        self.entry_degree = tk.Entry(master, font=font_style, width=30)
        self.entry_degree.grid(row=2, column=1, padx=10, pady=5)

        if self.dependent:
            self.entry_name.insert(0, self.dependent.get("name", ""))
            self.entry_dob.delete(0, tk.END)
            self.entry_dob.insert(0, self.dependent.get("dob", "dd/mm/aaaa"))
            self.entry_degree.insert(0, self.dependent.get("degree", ""))

        return self.entry_name

    def validate(self):
        name = self.entry_name.get().strip()
        dob = self.entry_dob.get_date()
        degree = self.entry_degree.get().strip()

        if not name or not dob or not degree:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos do dependente.")
            return False

        try:
            datetime.strptime(dob, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data de nascimento inválida. Use dd/mm/aaaa.")
            return False

        self.result = {
            "name": name,
            "dob": dob,
            "degree": degree,
        }
        return True

class EmployeeManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Funcionários e Dependentes")
        self.geometry("900x620")
        self.configure(bg="#ffffff")
        self.resizable(False, False)

        self.font_header = font.Font(family="Inter", size=26, weight="bold")
        self.font_label = font.Font(family="Inter", size=14)
        self.font_entry = font.Font(family="Inter", size=14)
        self.font_button = font.Font(family="Inter", size=13, weight="bold")

        self.employees = []
        self.current_employee = None

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        container = tk.Frame(self, bg="#f9fafb", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        header = tk.Label(container, text="Gerenciamento de Funcionários", bg="#f9fafb", fg="#111827", font=self.font_header)
        header.pack(pady=(0, 15))

        form_frame = tk.Frame(container, bg="#f9fafb")
        form_frame.pack(fill="x", pady=(0,15))

        # Fields and labels
        labels = [
            ("Código:", 0, 0),
            ("Nome:", 0, 2),
            ("Cargo:", 1, 0),
            ("Setor:", 1, 2),
            ("Data de Nascimento:", 2, 0),
            ("Data de Admissão:", 2, 2),
            ("Salário (R$):", 3, 0),
        ]

        self.entries = {}

        for text, r, c in labels:
            lbl = tk.Label(form_frame, text=text, font=self.font_label, bg="#f9fafb", fg="#6b7280", anchor="w")
            lbl.grid(row=r, column=c, sticky="w", padx=5, pady=8)
            if "Data de" in text:
                entry = DateEntry(form_frame, font=self.font_entry, width=20)
            else:
                entry = tk.Entry(form_frame, font=self.font_entry, width=30)
            entry.grid(row=r, column=c+1, sticky="ew", padx=5, pady=8)
            self.entries[text] = entry

        # Make columns expandable
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Buttons frame for employee operations
        btn_frame = tk.Frame(container, bg="#f9fafb")
        btn_frame.pack(fill="x", pady=(0, 20))

        btn_params = dict(font=self.font_button, fg="white", relief="flat", cursor="hand2", padx=14, pady=10)

        self.btn_cadastrar = tk.Button(btn_frame, text="Cadastrar", bg="#111827", command=self.cadastrar, **btn_params)
        self.btn_cadastrar.pack(side="left", expand=True, fill="x", padx=8)

        self.btn_deletar = tk.Button(btn_frame, text="Deletar", bg="#ef4444", command=self.deletar, **btn_params)
        self.btn_deletar.pack(side="left", expand=True, fill="x", padx=8)

        self.btn_consultar = tk.Button(btn_frame, text="Consultar", bg="#2563eb", command=self.consultar, **btn_params)
        self.btn_consultar.pack(side="left", expand=True, fill="x", padx=8)

        self.btn_alterar = tk.Button(btn_frame, text="Alterar", bg="#10b981", command=self.alterar, **btn_params)
        self.btn_alterar.pack(side="left", expand=True, fill="x", padx=8)

        # Dependents Section Label
        dep_label = tk.Label(container, text="Dependentes", font=self.font_label, bg="#f9fafb", fg="#111827", anchor="w")
        dep_label.pack(fill="x", padx=5, pady=(0,5))

        # Dependents listbox with scrollbar
        dep_list_frame = tk.Frame(container, bg="#f9fafb")
        dep_list_frame.pack(fill="both", expand=True, pady=(0,10))

        self.dependents_listbox = tk.Listbox(dep_list_frame, font=self.font_entry, selectmode=tk.SINGLE, activestyle="none", relief="solid", borderwidth=1)
        self.dependents_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(dep_list_frame, orient="vertical", command=self.dependents_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.dependents_listbox.config(yscrollcommand=scrollbar.set)
        self.dependents_listbox.bind("<<ListboxSelect>>", self.on_dependent_select)

        # Dependents buttons
        dep_btn_frame = tk.Frame(container, bg="#f9fafb")
        dep_btn_frame.pack(fill="x")

        self.btn_dep_adicionar = tk.Button(dep_btn_frame, text="Cadastrar Dependente", bg="#2563eb", command=self.adicionar_dependente, **btn_params)
        self.btn_dep_adicionar.pack(side="left", expand=True, fill="x", padx=6, pady=4)

        self.btn_dep_deletar = tk.Button(dep_btn_frame, text="Deletar Dependente", bg="#ef4444", command=self.deletar_dependente, **btn_params)
        self.btn_dep_deletar.pack(side="left", expand=True, fill="x", padx=6, pady=4)

    def alert(self, title, message):
        messagebox.showinfo(title, message)

    def error(self, title, message):
        messagebox.showerror(title, message)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%d/%m/%Y")
            return True
        except Exception:
            return False

    def clear_employee_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        # Reset date placeholders for date fields
        for key in self.entries:
            if "Data de" in key:
                self.entries[key].insert(0, "dd/mm/aaaa")
                self.entries[key].config(fg="#9ca3af")
        self.dependents_listbox.delete(0, tk.END)
        self.current_employee = None

    def get_employee_data(self):
        data = {}
        for k, entry in self.entries.items():
            val = entry.get().strip()
            if val == "dd/mm/aaaa":
                val = ""
            data[k] = val
        return data

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.employees = json.load(f)
            except Exception:
                self.employees = []
        else:
            self.employees = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.employees, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.error("Erro", f"Erro ao salvar dados: {e}")

    def find_employee_index(self, codigo):
        for idx, emp in enumerate(self.employees):
            if emp.get("codigo") == codigo:
                return idx
        return None

    def fill_employee_form(self, emp):
        self.entries["Código:"].delete(0, tk.END)
        self.entries["Código:"].insert(0, emp.get("codigo",""))
        self.entries["Nome:"].delete(0, tk.END)
        self.entries["Nome:"].insert(0, emp.get("nome",""))
        self.entries["Cargo:"].delete(0, tk.END)
        self.entries["Cargo:"].insert(0, emp.get("cargo",""))
        self.entries["Setor:"].delete(0, tk.END)
        self.entries["Setor:"].insert(0, emp.get("setor",""))
        self.entries["Data de Nascimento (dd/mm/aaaa):"].delete(0, tk.END)
        self.entries["Data de Nascimento (dd/mm/aaaa):"].insert(0, emp.get("data_nascimento","dd/mm/aaaa"))
        self.entries["Data de Nascimento (dd/mm/aaaa):"].config(fg="#111827" if emp.get("data_nascimento") else "#9ca3af")
        self.entries["Data de Admissão (dd/mm/aaaa):"].delete(0, tk.END)
        self.entries["Data de Admissão (dd/mm/aaaa):"].insert(0, emp.get("data_admissao","dd/mm/aaaa"))
        self.entries["Data de Admissão (dd/mm/aaaa):"].config(fg="#111827" if emp.get("data_admissao") else "#9ca3af")
        self.entries["Salário (R$):"].delete(0, tk.END)
        self.entries["Salário (R$):"].insert(0, str(emp.get("salario","")))
        self.current_employee = emp
        # Load dependents
        self.load_dependents(emp.get("dependentes", []))

    def load_dependents(self, dependents):
        self.dependents_listbox.delete(0, tk.END)
        self.current_employee["dependentes"] = dependents
        for dep in dependents:
            text = f"{dep.get('name','')} - {dep.get('dob','')} - {dep.get('degree','')}"
            self.dependents_listbox.insert(tk.END, text)

    def cadastrar(self):
        data = self.get_employee_data()
        codigo = data["Código:"]
        if not codigo:
            self.error("Erro", "Informe o código do funcionário.")
            return
        # Validate required fields
        required_fields = ["Nome:", "Cargo:", "Setor:", "Data de Nascimento (dd/mm/aaaa):", "Data de Admissão (dd/mm/aaaa):", "Salário (R$):"]
        for field in required_fields:
            if not data[field]:
                self.error("Erro", f"Preencha o campo: {field}")
                return
        # Validate dates
        for field in ["Data de Nascimento (dd/mm/aaaa):", "Data de Admissão (dd/mm/aaaa):"]:
            if not self.validate_date(data[field]):
                self.error("Erro", f"Data inválida no campo {field}. Use dd/mm/aaaa")
                return
        # Validate salary
        try:
            salario = float(data["Salário (R$):"].replace(",", "."))
            if salario < 0:
                self.error("Erro", "Salário não pode ser negativo.")
                return
        except Exception:
            self.error("Erro", "Salário inválido.")
            return
        if self.find_employee_index(codigo) is not None:
            self.error("Erro", "Código já cadastrado.")
            return

        novo_func = {
            "codigo": codigo,
            "nome": data["Nome:"],
            "cargo": data["Cargo:"],
            "setor": data["Setor:"],
            "data_nascimento": data["Data de Nascimento (dd/mm/aaaa):"],
            "data_admissao": data["Data de Admissão (dd/mm/aaaa):"],
            "salario": salario,
            "dependentes": []
        }
        self.employees.append(novo_func)
        self.save_data()
        self.alert("Sucesso", "Funcionário cadastrado.")
        self.clear_employee_fields()

    def deletar(self):
        data = self.get_employee_data()
        codigo = data["Código:"]
        if not codigo:
            self.error("Erro", "Informe o código do funcionário para deletar.")
            return
        idx = self.find_employee_index(codigo)
        if idx is None:
            self.error("Erro", "Funcionário não encontrado.")
            return
        confirm = messagebox.askyesno("Confirmação", f"Deletar o funcionário de código {codigo}?")
        if confirm:
            del self.employees[idx]
            self.save_data()
            self.alert("Sucesso", "Funcionário deletado.")
            self.clear_employee_fields()

    def consultar(self):
        data = self.get_employee_data()
        codigo = data["Código:"]
        if not codigo:
            self.error("Erro", "Informe o código para consulta.")
            return
        idx = self.find_employee_index(codigo)
        if idx is None:
            self.error("Erro", "Funcionário não encontrado.")
            return
        emp = self.employees[idx]
        self.fill_employee_form(emp)

    def alterar(self):
        data = self.get_employee_data()
        codigo = data["Código:"]
        if not codigo:
            self.error("Erro", "Informe o código para alterar.")
            return
        idx = self.find_employee_index(codigo)
        if idx is None:
            self.error("Erro", "Funcionário não encontrado.")
            return
        # Validate required fields
        required_fields = ["Nome:", "Cargo:", "Setor:", "Data de Nascimento (dd/mm/aaaa):", "Data de Admissão (dd/mm/aaaa):", "Salário (R$):"]
        for field in required_fields:
            if not data[field]:
                self.error("Erro", f"Preencha o campo: {field}")
                return
        # Validate dates
        for field in ["Data de Nascimento (dd/mm/aaaa):", "Data de Admissão (dd/mm/aaaa):"]:
            if not self.validate_date(data[field]):
                self.error("Erro", f"Data inválida no campo {field}. Use dd/mm/aaaa")
                return
        # Validate salary
        try:
            salario = float(data["Salário (R$):"].replace(",", "."))
            if salario < 0:
                self.error("Erro", "Salário não pode ser negativo.")
                return
        except Exception:
            self.error("Erro", "Salário inválido.")
            return
        emp = self.employees[idx]
        emp["nome"] = data["Nome:"]
        emp["cargo"] = data["Cargo:"]
        emp["setor"] = data["Setor:"]
        emp["data_nascimento"] = data["Data de Nascimento (dd/mm/aaaa):"]
        emp["data_admissao"] = data["Data de Admissão (dd/mm/aaaa):"]
        emp["salario"] = salario
        self.save_data()
        self.alert("Sucesso", "Funcionário alterado.")
        self.clear_employee_fields()

    def on_dependent_select(self, event):
        index = self.dependents_listbox.curselection()
        if not index:
            return
        index = index[0]
        emp = self.current_employee
        if emp and 0 <= index < len(emp["dependentes"]):
            dep = emp["dependentes"][index]
            dlg = DependentDialog(self, "Editar Dependente", dep)
            if dlg.result:
                emp["dependentes"][index] = dlg.result
                self.load_dependents(emp["dependentes"])
                self.save_data()

    def adicionar_dependente(self):
        if not self.current_employee:
            self.error("Erro", "Localize ou cadastre um funcionário antes de adicionar dependentes.")
            return
        dlg = DependentDialog(self, "Cadastrar Dependente")
        if dlg.result:
            self.current_employee.setdefault("dependentes", []).append(dlg.result)
            self.load_dependents(self.current_employee["dependentes"])
            self.save_data()

    def deletar_dependente(self):
        sel = self.dependents_listbox.curselection()
        if not sel:
            self.error("Erro", "Selecione um dependente para deletar.")
            return
        idx = sel[0]
        emp = self.current_employee
        if emp and 0 <= idx < len(emp.get("dependentes", [])):
            confirm = messagebox.askyesno("Confirmação", f"Quer realmente deletar o dependente '{emp['dependentes'][idx]['name']}'?")
            if confirm:
                emp["dependentes"].pop(idx)
                self.load_dependents(emp["dependentes"])
                self.save_data()

if __name__ == "__main__":
    app = EmployeeManagerApp()
    app.mainloop()









