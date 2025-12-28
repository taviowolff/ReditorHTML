# Reditor HTML

O **Reditor HTML** é uma ferramenta de produtividade para desktop desenvolvida em Python (Tkinter). Seu objetivo é otimizar a conversão de textos convencionais para o formato HTML, garantindo a padronização técnica necessária para publicações no blog da Databasers.

A aplicação processa o texto em tempo real, permitindo a inserção de tags semânticas e estruturais através de comandos de teclado, resultando em um código limpo e pronto para implementação em sistemas de gerenciamento de conteúdo (CMS).

## Funcionalidades Principais

* **Processamento em Tempo Real:** Visualização imediata do código HTML gerado conforme a edição no painel de entrada.
* **Interface Multi-tema:** Suporte a modos de visualização Claro e Escuro para maior conforto visual.
* **Gestão de Documentos:** Exportação direta do conteúdo processado para arquivos com extensão `.html`.
* **Sistema de Histórico:** Suporte nativo para operações de desfazer e refazer (Undo/Redo).

## Comandos de Produtividade (Atalhos)

Abaixo estão listados os comandos configurados para a manipulação rápida de tags no painel de edição.

| Atalho | Ação Executada | Tag Resultante |
| --- | --- | --- |
| **Ctrl + P** | Envolve o texto em um parágrafo | `<p>...</p>` |
| **Ctrl + B** | Aplica negrito simples | `<b>...</b>` |
| **Ctrl + S** | Aplica destaque semântico (Strong) | `<strong>...</strong>` |
| **Ctrl + I** | Aplica itálico | `<i>...</i>` |
| **Ctrl + U** | Aplica sublinhado | `<u>...</u>` |
| **Ctrl + L** | Insere quebra de linha | `<br>` |
| **Ctrl + H + (1-6)** | Inicia sequência para níveis de título | `<h1>` a `<h6>` |
| **Ctrl + Z / Y** | Desfazer / Refazer alteração | N/A |
| **Escape** | Cancela sequência de comando ativa | N/A |

## Padrões de Formatação e Regras Estruturais

Para manter a consistência estética do blog, a equipe deve observar as seguintes diretrizes de uso da ferramenta:

### Estruturação de Parágrafos

* A tag `<p>` deve delimitar cada bloco principal de pensamento ou informação.
* Utilize o atalho **Ctrl + P** com o texto selecionado para garantir o fechamento correto da tag.

### Controle de Espaçamento Interno

* **Quebras Simples:** Utilize **Ctrl + L** (`<br>`) para quebras de linha dentro do mesmo bloco de texto.
* **Espaçamento entre Blocos:** Para manter o padrão visual de espaçamento duplo entre parágrafos, recomenda-se a inserção de duas tags `<br>` após o fechamento de cada parágrafo (`</p><br><br>`).

## Guia de Instalação e Execução

### Requisitos de Sistema

O aplicativo é distribuído como um executável independente (Standalone), não sendo necessária a instalação prévia de interpretadores Python ou bibliotecas adicionais no ambiente do usuário.

### Instalação e Execução
Para utilizar o ReditorHTML sem a necessidade de configurar um ambiente de desenvolvimento Python, você pode baixar o executável diretamente pelo link abaixo:

Download do Aplicativo (.exe): [ReditorHTML.exe](https://github.com/taviowolff/ReditorHTML/blob/main/dist/ReditorHTML.exe)

[!TIP] Após baixar o arquivo, basta executá-lo para iniciar o editor. Caso o Windows exiba um alerta de segurança (SmartScreen), clique em "Mais informações" e "Executar assim mesmo", pois o executável não possui assinatura digital de desenvolvedor.

### Instruções de Uso

1. Execute o arquivo `ReditorHTML.exe`.
2. Insira o texto original no painel esquerdo.
3. Utilize os atalhos para aplicar a formatação desejada.
4. Clique em **Copiar HTML** ou utilize o menu **Arquivo > Salvar** para obter o código final.

---

## Informações Técnicas

* **Desenvolvedor:** Otávio Wolff Buffon
* **Versão:** 1.2
* **Ambiente:** Python 3.14.0/ Tkinter