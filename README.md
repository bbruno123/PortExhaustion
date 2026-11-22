# Teste de Exaustão de Portas TCP/UDP

Este projeto é um experimento controlado para estudar o comportamento do sistema operacional durante a exaustão de portas locais TCP e UDP.

## Aviso importante

**Use apenas em laboratório ou em uma máquina descartável sob seu controle.** O programa tenta reservar portas locais em grandes quantidades e pode interromper navegadores, jogos, serviços de rede, atualizações e outras aplicações.

- Não execute em computadores de terceiros.
- Não execute em servidores de produção.
- Não utilize em redes corporativas ou públicas sem autorização explícita.
- As portas serão liberadas ao encerrar o processo.

## O que o programa faz

O script:

1. Detecta o endereço IPv4 local usado para comunicação com a Internet.
2. Percorre as portas de `1` a `65535`.
3. Tenta criar um socket TCP e vinculá-lo a cada porta.
4. Tenta criar um socket UDP e vinculá-lo à mesma porta.
5. Mantém os sockets bem-sucedidos em uma lista para impedir que sejam descartados.
6. Reinicia a varredura das portas após atingir a faixa final.

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
- O `.exe` não deve ser instalado sem consentimento, iniciado automaticamente nem mantido após uma reinicialização.
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
