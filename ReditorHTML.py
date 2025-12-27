import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

class HTMLTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Reditor HTML")
        
        # DEFINIÇÃO DE TEMAS
        self.themes = {
            'light': {
                'bg': '#f0f0f0',    # Fundo geral e da janela
                'text_bg': 'white', # Fundo das caixas de texto
                'fg': 'black',      # Cor da letra
                'disabled_bg': '#eee', # Fundo da caixa de saída desabilitada
                'button_bg': '#e0e0e0', # Fundo dos botões
                'insert': 'black'   # Cor do cursor de texto
            },
            'dark': {
                'bg': '#2b2b2b',
                'text_bg': '#3c3f41',
                'fg': 'white',
                'disabled_bg': '#4e4e4e',
                'button_bg': '#3c3f41',
                'insert': 'white'
            }
        }
        self.current_theme = 'light'
        
        # BARRA DE MENUS
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        
        # 1. Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Salvar arquivo como...", command=self.save_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=master.quit)
        
        # 2. Menu Atalhos
        shortcuts_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Atalhos", menu=shortcuts_menu)
        shortcuts_menu.add_command(label="Mostrar Atalhos", command=self.show_shortcuts)
        
        # 3. Menu Info com Submenu de Tema
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
        
        # Widgets
        tk.Label(self.output_header_frame, text="Saída HTML").pack(side=tk.LEFT)
        self.copy_button = tk.Button(self.output_header_frame, text="📋 Copiar HTML", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.RIGHT, padx=5)

        tk.Label(self.input_frame, text="Texto (Atalhos para dicas)").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.input_frame, wrap=tk.WORD, height=20, width=50, undo=True, autoseparators=True)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        self.html_output = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, height=20, width=50, state='disabled')
        self.html_output.pack(fill=tk.BOTH, expand=True)

        # BINDINGS E INICIALIZAÇÃO 
        self.bind_shortcuts()
        self.input_text.bind("<<Modified>>", self.update_html_output)
        self.input_text.bind('<Return>', self.handle_return_key)
        
        # Aplica o tema inicial
        self.set_theme(self.current_theme)

    # FUNÇÕES DE TEMA
    def set_theme(self, theme_name):
        """Aplica o tema (claro ou escuro) a todos os widgets."""
        self.current_theme = theme_name
        colors = self.themes[theme_name]
        
        # 1. Aplicar cores à janela principal e frames
        self.master.config(bg=colors['bg'])
        self.input_frame.config(bg=colors['bg'])
        self.output_frame.config(bg=colors['bg'])
        self.output_header_frame.config(bg=colors['bg'])
        
        # 2. Aplicar cores aos Rótulos (Labels)
        for widget in [self.input_frame, self.output_header_frame]:
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=colors['bg'], fg=colors['fg'])
        
        # 3. Aplicar cores às Caixas de Texto (ScrolledText)
        self.input_text.config(
            bg=colors['text_bg'], 
            fg=colors['fg'], 
            insertbackground=colors['insert'] 
        )
        self.html_output.config(
            bg=colors['disabled_bg'], 
            fg=colors['fg']
        )
        
        # 4. Aplicar cores aos Botões
        self.copy_button.config(
            bg=colors['button_bg'], 
            fg=colors['fg']
        )
    
    # FUNÇÕES DE MENU
    def save_file_dialog(self):
        self.html_output.config(state='normal')
        html_content = self.html_output.get("1.0", tk.END).strip()
        self.html_output.config(state='disabled')
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("Arquivos HTML", "*.html"), ("Todos os Arquivos", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em: {filepath}")
            except Exception as e:
                messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo: {e}")

    def show_shortcuts(self):
        shortcuts_text = (
            "Atalhos do Reditor HTML:\n\n"
            "   Ctrl + I:  Itálico (<i>...</i>)\n"
            "   Ctrl + B:  Negrito (<b>...</b>)\n"
            "   Ctrl + S:  Destaque (<strong>...</strong>)\n"
            "   Ctrl + U:  Sublinhado (<u>...</u>)\n"
            "   Ctrl + L:  Quebra de Linha (<br>)\n"
            "   Ctrl + P:  Parágrafo (<p>...</p>)\n"
            "   Ctrl + H + n:  Parágrafo (<h1> a </h6>)\n"
            "   Enter:     Nova Linha visual no editor\n"
            "   Ctrl + Z:    Desfazer a ação\n"
            "   Ctrl + Y:    Refazer a ação"
        )
        messagebox.showinfo("Atalhos", shortcuts_text)

    def show_info(self):
        messagebox.showinfo(
            "Sobre o Aplicativo",
            "Reditor HTML\n\n"
            "Desenvolvido por: Otávio Wolff Buffon\n"
            "Versão: 1.2 (2025)"
        )

    # FUNÇÕES DE ATALHOS E TEXTO
    def handle_return_key(self, event):
        # Enter: insere apenas uma nova linha (\n) para visualização no editor
        self.input_text.edit_modified(False)
        self.input_text.insert(tk.INSERT, '\n')
        return 'break'

    def bind_shortcuts(self):
        self.input_text.bind('<Control-i>', lambda event: self.apply_html_tag(event, 'i'))
        self.input_text.bind('<Control-b>', lambda event: self.apply_html_tag(event, 'b'))
        self.input_text.bind('<Control-s>', lambda event: self.apply_html_tag(event, 'strong'))
        self.input_text.bind('<Control-u>', lambda event: self.apply_html_tag(event, 'u'))
        self.input_text.bind('<Control-l>', lambda event: self.apply_html_tag(event, 'br')) 
        self.input_text.bind('<Control-p>', lambda event: self.apply_html_tag(event, 'p'))
       
        # Início da Sequência para Títulos (Ctrl + H)
        # Ao apertar Ctrl+H, o programa espera você digitar um número de 1 a 6
        self.input_text.bind('<Control-h>', self.start_heading_sequence)

    def start_heading_sequence(self, event):
        # Recebe o nível do título (1-6) após Ctrl+H.
        # Muda o cursor para indicar que o app está esperando um comando
        self.input_text.config(cursor="question_arrow")

        # Previne a digitação normal enquanto espera o número
        self.input_text.bind('<Key>', lambda e: "break")
        
        # Binds temporários para os números de 1 a 6
        for i in range(1, 7):
            self.input_text.bind(str(i), lambda e, n=i: self.finish_heading_sequence(e, n))
            
        # ESC para cancelar a operação caso o usuário desista do título
        self.input_text.bind('<Escape>', lambda e: self.finish_heading_sequence(e, None))
        
        return 'break' 

    def finish_heading_sequence(self, event, level):
        """Aplica a tag Hn e restaura o comportamento normal do teclado"""
        if level:
            self.apply_html_tag(None, f'h{level}')
        
        # Restaura o cursor original
        self.input_text.config(cursor="")
        
        # Desvincula o bloqueio de teclas e os números
        self.input_text.unbind('<Key>')
        for i in range(1, 7):
            self.input_text.unbind(str(i))
        self.input_text.unbind('<Escape>')
        
        return 'break'

    def apply_html_tag(self, event, tag):
        self.input_text.edit_modified(False)

        try:
            # Seleção existe
            selection_start = self.input_text.tag_ranges(tk.SEL)[0]
            selection_end = self.input_text.tag_ranges(tk.SEL)[1]
            selected_text = self.input_text.get(selection_start, selection_end)

            open_tag = f'<{tag}>'
            close_tag = f'</{tag}>'

            if tag == 'br':
                self.input_text.delete(selection_start, selection_end)
                self.input_text.insert(selection_start, '<br>')
            else:
                new_text = f'{open_tag}{selected_text}{close_tag}'
                self.input_text.delete(selection_start, selection_end)
                self.input_text.insert(selection_start, new_text)

        except IndexError:
            # Sem seleção: insere tags no cursor
            cursor_pos = self.input_text.index(tk.INSERT)

            if tag == 'br':
                self.input_text.insert(cursor_pos, '<br>')
            else:
                open_tag = f'<{tag}>'
                close_tag = f'</{tag}>'
                self.input_text.insert(cursor_pos, f'{open_tag}{close_tag}')
                self.input_text.mark_set(tk.INSERT, f"{cursor_pos}+{len(open_tag)}c")

        return 'break'

    def update_html_output(self, event):
        if self.input_text.edit_modified():
            raw_text = self.input_text.get("1.0", tk.END).strip()
            
            html_content = ""
            lines = raw_text.split('\n')
            
            for line in lines:
                stripped_line = line.strip()
                
                if not stripped_line:
                    continue

                # Apenas adiciona a linha de entrada e força a quebra de linha na saída
                html_content += line + '\n'

            # Atualiza a caixa de saída
            self.html_output.config(state='normal')
            self.html_output.delete("1.0", tk.END)
            self.html_output.insert("1.0", html_content)
            self.html_output.config(state='disabled')

            self.input_text.edit_modified(False)

    def copy_to_clipboard(self):
        self.html_output.config(state='normal')
        html_to_copy = self.html_output.get("1.0", tk.END).strip()
        self.html_output.config(state='disabled')
        
        self.master.clipboard_clear()
        self.master.clipboard_append(html_to_copy)
        
        messagebox.showinfo("Sucesso", "O código HTML foi copiado para a área de transferência!")


if __name__ == '__main__':
    root = tk.Tk()
    app = HTMLTranslatorApp(root)
    root.mainloop()