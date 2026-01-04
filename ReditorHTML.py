import tkinter as tk
import mammoth
import html
import re
from tkinterweb import HtmlFrame
from tkinter import scrolledtext, messagebox, filedialog
import webbrowser
import sys, os

class HTMLTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("ReditorHTML")
        
        # --- CARREGAMENTO DO ÍCONE ---
        def resource_path(relative_path):
            """ Obtém o caminho absoluto para o recurso, funciona para dev e PyInstaller """
            try:
                # O PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        try:
            # Busca o ícone usando o caminho absoluto resolvido pela função
            icon_path = resource_path('icon.ico')
            master.iconbitmap(icon_path)
        except:
            # Se falhar (ex: arquivo não existe na pasta de dev), o app abre com o ícone padrão
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

        self.html_output = HtmlFrame(self.output_frame, messages_enabled=False)
        self.html_output.pack(fill=tk.BOTH, expand=True)

        self.cover_frame = tk.Frame(self.output_frame)

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

        try:
            target_bg = "#2b2b2b" if theme_name == 'dark' else "white"
            self.html_output.config(bg=target_bg)
        except:
            pass 

        self.force_refresh_preview()

    def force_refresh_preview(self):
        """Força a re-renderização do HTML com base no tema atual."""
        self.input_text.edit_modified(True)
        self.update_html_output(None)

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
        # Cria uma janela personalizada em vez do messagebox padrão
        about_window = tk.Toplevel(self.master)
        about_window.title("Sobre")
        about_window.geometry("300x200")
        about_window.config(bg=self.themes[self.current_theme]['bg'])
        about_window.resizable(False, False)

        # Texto de Informação
        fg_color = self.themes[self.current_theme]['fg']
        bg_color = self.themes[self.current_theme]['bg']

        tk.Label(about_window, text="ReditorHTML", font=("Arial", 14, "bold"), 
                 bg=bg_color, fg=fg_color).pack(pady=10)
        
        tk.Label(about_window, text="Desenvolvido por: Otávio Buffon\nVersão: 1.3.1 (2026)", 
                 bg=bg_color, fg=fg_color).pack(pady=5)

        # Link do LinkedIn
        link_label = tk.Label(about_window, text="Meu LinkedIn", fg="#5fb3b3", 
                              bg=bg_color, cursor="hand2", font=("Arial", 10, "underline"))
        link_label.pack(pady=10)
        
        # Função para abrir o navegador
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("www.linkedin.com/in/ot%C3%A1vio-buffon/"))

        # Botão Fechar
        tk.Button(about_window, text="Fechar", command=about_window.destroy,
                  bg=self.themes[self.current_theme]['button_bg'], fg=fg_color).pack(pady=5)
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
            raw_text = self.input_text.get("1.0", tk.END)
            
            # Definimos as cores do tema
            is_dark = self.current_theme == 'dark'
            bg_color = "#2b2b2b" if is_dark else "white"
            text_color = "white" if is_dark else "black"
            heading_color = "#5fb3b3" if is_dark else "black"

            # 1. Colocamos o "escudo" por cima do preview imediatamente
            # O place com relwidth e relheight garante que ele cubra tudo sem mover nada
            self.cover_frame.config(bg=bg_color)
            self.cover_frame.place(in_=self.html_output, relwidth=1, relheight=1)

            style = f"""
            <style>
                html, body {{ 
                    background-color: {bg_color} !important; 
                    color: {text_color}; 
                    font-family: sans-serif; 
                    padding: 10px;
                }}
                h1, h2, h3, h4, h5, h6 {{ color: {heading_color}; }}
            </style>
            """
            full_html = style + raw_text
            
            # Carregar o conteúdo (o flash branco acontece atrás do cover_frame)
            self.html_output.load_html(full_html) 
            
            # Remover o escudo após um tempo mínimo, quando o motor já processou o CSS
            self.master.after(60, lambda: self.cover_frame.place_forget())
            
            self.input_text.edit_modified(False)

    def copy_to_clipboard(self):
        html_to_copy = self.input_text.get("1.0", tk.END).strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(html_to_copy)
        messagebox.showinfo("Sucesso", "HTML Copiado!")

if __name__ == '__main__':
    root = tk.Tk()
    app = HTMLTranslatorApp(root)
    root.mainloop()