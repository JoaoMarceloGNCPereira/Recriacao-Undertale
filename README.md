# Recriação de Undertale

Protótipo de um jogo inspirado em Undertale, feito com Python e Pygame.

## Rodar no Windows

1. Instale [Python](https://www.python.org/downloads/) **3.12, 3.13 ou 3.14**. Na instalação, marque `Add Python to PATH`.
2. Baixe ou clone este repositório.
3. Dê duplo clique em `run.bat`.

Na primeira execução, o script cria a pasta `.venv`, instala as bibliotecas e abre o jogo. Nas próximas, ele apenas confirma as dependências e inicia o jogo.

Também é possível executar pelo PowerShell:

```powershell
.\run.ps1
```

## Instalação manual

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe Main.py
```

## Chave da IA (opcional)

O protótipo principal abre sem IA. Para usar inimigos com conversa por Gemini, copie `.env.example` para `.env` e coloque sua chave:

```text
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env` é ignorado pelo Git e nunca deve ser enviado ao repositório.

## Compatibilidade

O projeto usa `pygame-ce`, uma versão mantida e compatível da API Pygame. Ele é testado automaticamente no GitHub Actions com Python 3.12, 3.13 e 3.14 em cada envio ao repositório.

## Teste rápido

Para conferir a inicialização sem abrir uma janela do jogo:

```powershell
.\.venv\Scripts\python.exe tests\smoke_test.py
```
