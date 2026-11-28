# Teste de Exaustão de Portas TCP/UDP

Este projeto é um experimento controlado para estudar o comportamento do sistema operacional durante a exaustão de portas locais TCP e UDP.

## Aviso importante

**Use apenas em laboratório ou em uma máquina descartável sob seu controle.** O programa tenta reservar portas locais em grandes quantidades e pode interromper navegadores, jogos, serviços de rede, atualizações e outras aplicações.

Ao ser executado, o script também tenta criar ou atualizar um atalho na pasta Inicializar do usuário. Depois disso, ele poderá iniciar novamente no próximo login do Windows e começar a rotina de reserva de portas.

- Não execute em computadores de terceiros.
- Não execute em servidores de produção.
- Não utilize em redes corporativas ou públicas sem autorização explícita.
- As portas serão liberadas ao encerrar o processo.

## O que o programa faz

O script:

1. Aguarda até detectar um endereço IPv4 local diferente de `127.0.0.1`.
2. Percorre as portas de `1` a `65535`.
3. Tenta criar um socket TCP e vinculá-lo a cada porta.
4. Tenta criar um socket UDP e vinculá-lo à mesma porta.
5. Mantém os sockets bem-sucedidos em uma lista para impedir que sejam descartados.
6. Reinicia a varredura das portas após atingir a faixa final.

A varredura só começa depois que o endereço IP é detectado. Se o script for iniciado com o Windows antes de a rede estar pronta, ele continua tentando detectar o IP, com intervalos de um segundo. Essa verificação identifica o endereço local escolhido pelo sistema; não confirma que o acesso à Internet já está funcionando.

Como resultado, o sistema pode ficar sem sockets livres ou sem portas locais disponíveis para novas conexões.

## Comportamento esperado

Dependendo do sistema operacional e das portas já reservadas pelo Windows ou por outros programas:

- O navegador pode continuar aberto, mas novas conexões HTTPS/HTTP podem falhar.
- Aplicações podem apresentar erros como `Address already in use` ou `No buffer space available`.
- Novos serviços locais podem não conseguir iniciar.
- A criação de novas portas dinâmicas pelo sistema pode ser limitada.
- Conexões já estabelecidas podem continuar temporariamente disponíveis.
- O consumo de memória e recursos pode aumentar à medida que os sockets são criados.

A aplicação não envia pacotes para toda a faixa de portas e não bloqueia diretamente a Internet do roteador.

## Requisitos

- Windows
- Python 3
- Permissões suficientes para vincular sockets às portas locais

No PowerShell, verifique o Python com:

```powershell
python --version
```

## Ambiente recomendado

Use uma máquina virtual ou uma instalação descartável com:

- Sem serviços críticos em execução.
- Sem antivírus ou políticas corporativas que possam interferir no teste.
- Sem execução remota obrigatória ao operador.
- Sistema e dados importantes protegidos por snapshot ou backup.

Recomenda-se criar um checkpoint da VM antes do teste.

## Execução

No diretório do projeto, execute:

```powershell
python .\PortExhaustion.py
```

Ao iniciar, o programa exibirá o endereço IP local detectado. Ao atingir o fim da varredura, mostrará aproximadamente quantos sockets conseguiu manter abertos.

## Encerramento

Pressione `CTRL+C` no terminal.

Os sockets são associados ao processo do Python. Depois que o processo termina, o sistema operacional normalmente libera todas as portas que ele reservou.

Se o terminal ficar travado, o processo pode ser encerrado pelo Gerenciador de Tarefas.

## Observações técnicas

- `bind()` reserva o endereço local e a porta. TCP também exige `listen()` para iniciar o modo de espera.
- UDP não possui conexão ou estado de listening como TCP.
- Portas ocupadas por outros processos não poderão ser vinculadas pelo script.
- Algumas portas são reservadas ou protegidas pelo Windows.
- O loop se reinicia depois que `porta` ultrapassa `65535`, então o programa continuará até receber `CTRL+C`.
- `subprocess.run("cls", shell=True)` apenas limpa o console em Windows.

## Melhorias sugeridas para testes controlados

- Limitar o intervalo de portas testadas.
- Permitir uma quantidade máxima de sockets.
- Executar em uma interface/IP específico.
- Definir duração automática do teste.
- Fechar todos os sockets em um bloco `finally` ou ao receber `SIGINT`.
- Registrar quantos sockets TCP e UDP foram efetivamente criados.
- Fazer o teste dentro de uma VM e verificar a recuperação após encerrar o processo.

## Uso seguro

Um experimento seguro pode usar somente uma faixa pequena em uma máquina isolada, por exemplo `20000–20010`, e duração limitada. Não precisa testar todas as `65535` portas para observar a falha de vinculação e a exaustão de recursos.

## Executável em segundo plano

O executável (`.exe`) do laboratório pode ser fornecido separadamente e não precisa ser compilado a partir deste repositório. Ele deve representar a mesma rotina de exaustão limitada a portas locais, ser identificado claramente e manter uma forma conhecida de encerramento.

- A execução em segundo plano não substitui a necessidade de supervisão manual.
- O `.exe` não deve ser executado sem consentimento explícito. Como o script cria um atalho de inicialização, informe ao operador que ele poderá iniciar novamente no próximo login e explique como remover o atalho.
- Não use mecanismos de evasão, persistência, nomes falsos ou dissimulação.
- Antes da entrega, confirme que os participantes sabem qual processo está ativo e como encerrá-lo.
- Registre o nome e o PID do processo para facilitar a interrupção pelo Gerenciador de Tarefas.

Uma pessoa não deve fechar ou perder o controle do programa sem querer. Use somente proteção operacional responsável: janela identificada, alerta antes do início, duração limitada e instruções claras de encerramento. Não utilize janela invisível, minimização deliberada ou ocultação em processos do sistema.

Antes da execução do `.exe`, confirme que os integrantes do laboratório sabem:

- Qual aplicação está executando.
- Que o processo pode afetar navegadores e serviços locais.
- Onde o processo aparece no Gerenciador de Tarefas.
- Como encerrá-lo imediatamente.
- Quanto tempo o teste poderá permanecer ativo.

## Inicialização com o Windows

O script chama `iniciar_com_windows()` ao iniciar. A função usa `win32com.client.Dispatch` para acessar `WScript.Shell`, obtém a pasta `Startup` do usuário e salva nela o atalho `PortExhaustion.lnk`.

O destino depende de como o programa está sendo executado:

- Como script Python, o destino é o caminho absoluto de `PortExhaustion.py`.
- Como executável congelado, o destino é `sys.executable`, ou seja, o próprio `.exe`.

O diretório de trabalho do atalho é a pasta do destino. Cada execução salva o atalho no mesmo caminho, atualizando-o; o código não verifica previamente se ele já existe. Se ocorrer um erro ao criar o atalho, a exceção é ignorada.

No próximo login do usuário, o Windows inicia o destino do atalho. Isso inicia também a rotina de detecção de IP e reserva de portas, que pode afetar a rede local e outros aplicativos até o processo ser encerrado. O script não oculta o terminal nem oferece duração automática.

Para desativar a inicialização, remova `PortExhaustion.lnk` da pasta Inicializar do usuário. Uma execução posterior do script tentará criar o atalho novamente.

### Execução em segundo plano

Atualmente, o script não é um aplicativo em segundo plano por padrão. Ele é executado em primeiro plano no terminal e mostra informações no console.

Isso significa que:

- uma janela do terminal permanece aberta;
- o usuário pode acompanhar as mensagens exibidas;
- `CTRL+C` pode encerrar o programa;
- fechar a janela do terminal pode interromper o processo;
- o Windows não cria um serviço do sistema automaticamente;
- o programa não usa `pythonw.exe`, ocultação de janela ou um mecanismo de persistência.

Somente tornar o executável invisível ou ocultar o terminal não é recomendado em um laboratório responsável. Um aplicativo em segundo plano precisa continuar visível no Gerenciador de Tarefas e ter uma forma conhecida de encerramento.

Os sockets criados pelo processo pertencem ao processo do Python. Ao fechar o programa, o Windows normalmente libera esses recursos. A aplicação ainda deve implementar um bloqueio `finally` ou tratamento explícito de `KeyboardInterrupt` para fechar os sockets antes de encerrar, principalmente enquanto o processo estiver em desenvolvimento.

## Instalação das dependências

As dependências externas estão listadas em `requirements.txt`:

- `pywin32`: fornece `win32com.client.Dispatch`.
- `pyinstaller`: opcional, usado somente para gerar um executável `.exe`.

Os módulos `socket`, `subprocess`, `sys`, `os`, `time` e `shutil` fazem parte da biblioteca padrão do Python e não precisam ser instalados separadamente.

No diretório do projeto, instale todas as dependências com:

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

Se quiser executar o script diretamente e não gerar um `.exe`, instale apenas a dependência de execução:

```powershell
python -m pip install pywin32
```
