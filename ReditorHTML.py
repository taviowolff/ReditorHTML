import tkinter as tk
import mammoth
import html
import re
from tkinterweb import HtmlFrame
from tkinter import scrolledtext, messagebox, filedialog

class HTMLTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("ReditorHTML")
        
        # --- CARREGAMENTO DO ÍCONE ---
        try:
            # Ajustado para o nome real do seu arquivo: icon.ico
            master.iconbitmap('icon.ico')
        except:
            pass
        
        # DEFINIÇÃO DE TEMAS
        self.themes = {
            'light': {
                'bg': '#f0f0f0', 'text_bg': 'white', 'fg': 'black', 
                'disabled_bg': '#eee', 'button_bg': '#e0e0e0', 'insert': 'black'
            },
            'dark': {
                'bg': '#2b2b2b', 'text_bg': '#3c3f41', 'fg': 'white', 
                'disabled_bg': '#4e4e4e', 'button_bg': '#3c3f41', 'insert': 'white'
            }
        }
        self.current_theme = 'light'
        
        # BARRA DE MENUS
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Importar arquivo (.docx)", command=self.import_docx_dialog)
        file_menu.add_command(label="Salvar arquivo como...", command=self.save_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=master.quit)
        
        shortcuts_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Atalhos", menu=shortcuts_menu)
        shortcuts_menu.add_command(label="Mostrar Atalhos", command=self.show_shortcuts)
        
        info_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mais", menu=info_menu)
        info_menu.add_command(label="Sobre", command=self.show_info)
        
        theme_menu = tk.Menu(info_menu, tearoff=0)
        info_menu.add_cascade(label="Tema", menu=theme_menu)
        theme_menu.add_command(label="Claro", command=lambda: self.set_theme('light'))
        theme_menu.add_command(label="Escuro", command=lambda: self.set_theme('dark'))
        
        # FRAMES E LAYOUT
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_frame = tk.Frame(master)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.output_header_frame = tk.Frame(self.output_frame)
        self.output_header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.output_header_frame, text="Visualização Web").pack(side=tk.LEFT)
        self.copy_button = tk.Button(self.output_header_frame, text="📋 Copiar HTML", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.RIGHT, padx=5)

        tk.Label(self.input_frame, text="Editor de Código (Tags)").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.input_frame, wrap=tk.WORD, height=20, width=50, undo=True, autoseparators=True)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # O Visualizador Web (NÃO configurado no set_theme para evitar erro -bg)
        self.html_output = HtmlFrame(self.output_frame, messages_enabled=False)
        self.html_output.pack(fill=tk.BOTH, expand=True)

        self.bind_shortcuts()
        self.input_text.bind("<<Modified>>", self.update_html_output)
        self.input_text.bind('<Return>', self.handle_return_key)
        
        self.set_theme(self.current_theme)

    def set_theme(self, theme_name):
        self.current_theme = theme_name
        colors = self.themes[theme_name]
        
        self.master.config(bg=colors['bg'])
        self.input_frame.config(bg=colors['bg'])
        self.output_frame.config(bg=colors['bg'])
        self.output_header_frame.config(bg=colors['bg'])
        
        for widget in [self.input_frame, self.output_header_frame]:
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=colors['bg'], fg=colors['fg'])
        
        self.input_text.config(bg=colors['text_bg'], fg=colors['fg'], insertbackground=colors['insert'])
        self.copy_button.config(bg=colors['button_bg'], fg=colors['fg'])

    def import_docx_dialog(self):
        filepath = filedialog.askopenfilename(filetypes=[("Arquivos Word", "*.docx")])
        if filepath:
            try:
                with open(filepath, "rb") as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    html_gerado = html.unescape(result.value)
                    html_limpo = re.sub(r'<a id="[^"]+"></a>', '', html_gerado)
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", html_limpo)
                    self.input_text.edit_modified(True) 
                    messagebox.showinfo("Sucesso", "Documento importado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    def save_file_dialog(self):
        html_content = self.input_text.get("1.0", tk.END).strip()
        filepath = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Arquivos HTML", "*.html")])
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Sucesso", "Arquivo salvo!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def show_shortcuts(self):
        shortcuts_text = (
            "Atalhos do Reditor HTML:\n\n"
            "   Ctrl + I: Itálico (<i>)\n"
            "   Ctrl + B: Negrito (<b>)\n"
            "   Ctrl + S: Destaque (<strong>)\n"
            "   Ctrl + U: Sublinhado (<u>)\n"
            "   Ctrl + L: Quebra de Linha (<br>)\n"
            "   Ctrl + P: Parágrafo (<p>)\n"
            "   Ctrl + H + (1-6): Títulos (<h1> a <h6>)\n"
            "   Ctrl + Z / Y: Desfazer / Refazer\n"
            "   Esc: Cancelar comando de título"
        )
        messagebox.showinfo("Atalhos", shortcuts_text)

    def show_info(self):
        messagebox.showinfo("Sobre", "ReditorHTML\n\nDesenvolvido por: Otávio Buffon\nVersão: 1.3 (2026)")

    def handle_return_key(self, event):
        self.input_text.edit_modified(False)
        self.input_text.insert(tk.INSERT, '\n')
        return 'break'

    def bind_shortcuts(self):
        self.input_text.bind('<Control-i>', lambda e: self.apply_html_tag(e, 'i'))
        self.input_text.bind('<Control-b>', lambda e: self.apply_html_tag(e, 'b'))
        self.input_text.bind('<Control-s>', lambda e: self.apply_html_tag(e, 'strong'))
        self.input_text.bind('<Control-u>', lambda e: self.apply_html_tag(e, 'u'))
        self.input_text.bind('<Control-l>', lambda e: self.apply_html_tag(e, 'br')) 
        self.input_text.bind('<Control-p>', lambda e: self.apply_html_tag(e, 'p'))
        self.input_text.bind('<Control-h>', self.start_heading_sequence)

    def start_heading_sequence(self, event):
        self.input_text.config(cursor="question_arrow")
        self.input_text.bind('<Key>', lambda e: "break")
        for i in range(1, 7):
            self.input_text.bind(str(i), lambda e, n=i: self.finish_heading_sequence(e, n))
        self.input_text.bind('<Escape>', lambda e: self.finish_heading_sequence(e, None))
        return 'break' 

    def finish_heading_sequence(self, event, level):
        if level: self.apply_html_tag(None, f'h{level}')
        self.input_text.config(cursor="")
        self.input_text.unbind('<Key>')
        for i in range(1, 7): self.input_text.unbind(str(i))
        self.input_text.unbind('<Escape>')
        return 'break'

    def apply_html_tag(self, event, tag):
        self.input_text.edit_modified(False)
        try:
            sel_range = self.input_text.tag_ranges(tk.SEL)
            if not sel_range: raise IndexError
            start, end = sel_range[0], sel_range[1]
            text = self.input_text.get(start, end)
            self.input_text.delete(start, end)
            if tag == 'br': self.input_text.insert(start, '<br>')
            else: self.input_text.insert(start, f'<{tag}>{text}</{tag}>')
        except IndexError:
            pos = self.input_text.index(tk.INSERT)
            if tag == 'br': self.input_text.insert(pos, '<br>')
            else: self.input_text.insert(pos, f'<{tag}></{tag}>')
        return 'break'

    def update_html_output(self, event):
        if self.input_text.edit_modified():
            # Renderiza o código HTML no painel web
            raw_text = self.input_text.get("1.0", tk.END)
            self.html_output.load_html(raw_text) 
            self.input_text.edit_modified(False)

    def copy_to_clipboard(self):
        # Copia o código do editor da esquerda
        html_to_copy = self.input_text.get("1.0", tk.END).strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(html_to_copy)
        messagebox.showinfo("Sucesso", "HTML Copiado!")

if __name__ == '__main__':
    root = tk.Tk()
    app = HTMLTranslatorApp(root)
    root.mainloop()