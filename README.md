# Reditor HTML

Este é um aplicativo de desktop simples e eficiente, desenvolvido em Python com a biblioteca Tkinter, projetado para ajudar na produção de conteúdo HTML formatado para blogs.

Ele permite que o usuário escreva texto simples e aplique formatação HTML (parágrafos, negrito, itálico e quebras de linha) usando atalhos de teclado, gerando o código HTML limpo e pronto para ser copiado e colado na plataforma de gerenciamento de conteúdo.

---

## 🛠️ Funcionalidades Principais

* **Edição Rápida:** Dois painéis, um para entrada de texto e outro para visualização e cópia do HTML final.
* **Atalhos de Produtividade:** Aplicação instantânea de tags HTML via atalhos.
* **Controle de Tema:** Opção de alternar entre os temas Claro e Escuro (`light`/`dark`).
* **Gerenciamento de Arquivos:** Opção para Salvar o código HTML gerado diretamente em um arquivo `.html`.

---

## ⌨️ Atalhos de Teclado (Produtividade)

Utilize os seguintes atalhos no painel de **Texto de Entrada** para formatar seu conteúdo:

| Comando | Descrição | Tag HTML Gerada |
| :--- | :--- | :--- |
| **Ctrl + P** | **Parágrafo:** Cria as tags de abertura e fechamento de parágrafo. Se o texto estiver selecionado, envolve a seleção. | `<p>Conteúdo</p>` |
| **Ctrl + B** | **Negrito:** Cria as tags de abertura e fechamento de negrito. | `<b>Conteúdo</b>` |
| **Ctrl + I** | **Itálico:** Cria as tags de abertura e fechamento de itálico. | `<i>Conteúdo</i>` |
| **Ctrl + L** | **Quebra de Linha:** Insere uma quebra de linha. | `<br>` |
| **Enter** | **Nova Linha Visual:** Apenas move o cursor para a próxima linha no editor, facilitando a visualização do código-fonte. | `\n` (Ignorado no HTML final) |

---

## 📚 Regras de Formatação e Padrões

Este editor foi configurado para respeitar um padrão de espaçamento e estrutura que deve ser seguido pela equipe para garantir a consistência no blog.

### 1. Estrutura de Parágrafos (`<p>`)

* **Quando usar `<p>`:** A tag `<p>` (Parágrafo) deve ser usada para envolver blocos inteiros de texto que representam um bloco coeso.
* **Como usar:** Use o atalho **Ctrl + P** para iniciar um novo parágrafo.
* **Regra:** **Cada bloco de texto principal (cada "insert") deve ser um `<p>` separado.**

### 2. Controle de Quebra de Linha (`<br>`)

O editor assume que você está no controle total das quebras de linha dentro do seu texto:

* **Pular Linha/Quebra Curta:** Para forçar uma quebra de linha visual dentro do mesmo parágrafo (sem iniciar um novo bloco `<p>`), utilize o atalho **Ctrl + L** para inserir a tag `<br>`.
* **Espaçamento Padrão (Recomendado):**
    * Para criar um espaçamento vertical confortável (como se fosse um Enter duplo), é **recomendável utilizar a tag `<br>` até 2 vezes** (ex: `<br><br>`) para manter um padrão de espaçamento visível no blog.
    * **Ao final de todo parágrafo (`</p>`), também é recomendável utilizar a tag `<br>` (ex: `</p><br><br>`).**

---

## 💾 Instalação e Uso

### 1. Requisitos

O aplicativo é um executável independente e **não requer a instalação do Python**.

### 2. Executando

1.  Baixe o arquivo executável (`ReditorHTML.exe`).
2.  Dê um duplo clique no arquivo para iniciar o aplicativo.

### 3. Opções do Menu

| Menu | Opção | Ação |
| :--- | :--- | :--- |
| **Arquivo** | Salvar HTML como... | Salva o conteúdo do painel "Saída HTML" em um arquivo `.html` no seu computador. |
| **Atalhos** | Mostrar Atalhos | Exibe a lista completa de atalhos e suas tags correspondentes. |
| **Mais** | Tema > Claro/Escuro | Alterna o esquema de cores da aplicação. |
| **Mais** | Sobre | Exibe informações sobre a autoria e a versão do software.
