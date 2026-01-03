# ReditorHTML (v1.3 - Live Preview Edition)

O **Reditor HTML** é uma ferramenta de produtividade para desktop desenvolvida em Python. Seu objetivo é otimizar a conversão de textos e documentos do Word para o formato HTML, garantindo a padronização técnica necessária para publicações em blogs e sistemas de gerenciamento de conteúdo (CMS).

A aplicação processa o conteúdo em tempo real, permitindo a inserção de tags semânticas e estruturais através de comandos de teclado, resultando em um código limpo e pronto para implementação.

## Funcionalidades Principais

* **Live Preview:** Painel de visualização que utiliza um motor de navegador integrado para exibir a renderização real do HTML.
* **Importação de Documentos:** Suporte para arquivos .docx com conversão automática para HTML semântico.
* **Sanitização de Código:** Limpeza automática de âncoras internas do Word e decodificação de entidades HTML (conversão de aspas e caracteres especiais).
* **Interface Multi-tema:** Suporte aos modos Claro e Escuro para adaptação ao ambiente de trabalho.
* **Sistema de Histórico:** Suporte completo para operações de desfazer e refazer (Undo/Redo).

## Comandos de Produtividade (Atalhos)

| Atalho | Ação Executada | Tag Resultante |
| --- | --- | --- |
| **Ctrl + P** | Envolve o texto em um parágrafo | `<p>...</p>` |
| **Ctrl + B** | Aplica negrito simples | `<b>...</b>` |
| **Ctrl + S** | Aplica destaque semântico (Strong) | `<strong>...</strong>` |
| **Ctrl + I** | Aplica itálico | `<i>...</i>` |
| **Ctrl + U** | Aplica sublinhado | `<u>...</u>` |
| **Ctrl + L** | Insere quebra de linha | `<br>` |
| **Ctrl + H + (1-6)** | Sequência para níveis de título | `<h1>` a `<h6>` |
| **Ctrl + Z / Y** | Desfazer / Refazer alteração | N/A |
| **Escape** | Cancela sequência de comando ativa | N/A |

## Padrões de Formatação e Regras Estruturais

### Estruturação de Conteúdo

* A tag `<p>` deve delimitar cada bloco principal de informação.
* Para manter a consistência visual do espaçamento entre parágrafos, recomenda-se a inserção de duas tags `<br>` após o fechamento de cada parágrafo (`</p><br><br>`).

### Limpeza de Importação

* O sistema remove automaticamente atributos de identificação desnecessários (`<a id="...">`) gerados por editores de texto externos.

## Guia de Instalação e Execução

### Requisitos de Sistema

O aplicativo é distribuído como um executável independente (Standalone), não sendo necessária a instalação de interpretadores Python ou bibliotecas adicionais.

### Instalação e Execução

1. Baixe o executável: [ReditorHTML.exe](https://github.com/taviowolff/ReditorHTML/blob/main/dist/ReditorHTML.exe)
2. Execute o arquivo `ReditorHTML.exe`.
3. Caso o Windows SmartScreen exiba um alerta, selecione "Mais informações" e "Executar assim mesmo".

### Instruções de Uso

1. Importe um arquivo .docx através do menu Arquivo ou insira o texto no painel esquerdo.
2. Utilize os atalhos para aplicar a formatação necessária.
3. Utilize o botão **Copiar HTML** para transferir o código processado para a área de transferência.

---

## Informações Técnicas

* **Desenvolvedor:** Otávio Wolff Buffon
* **Versão:** 1.3 (2026)
* **Ambiente:** Python 3.14.0 / Tkinter / Mammoth / TkinterWeb