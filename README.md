# Filtro-FIR-para-FPGA
Projeto para explorar implementações otimizadas de filtros FIR de alta ordem em FPGA. Utiliza Python para geração automática de código Verilog, quantização, criação de testbenches e análise de desempenho, visando aplicações em tempo real e uso eficiente de recursos.

Geração, Simulação e Validação de Filtro FIR em Verilog com Suporte Python
Este projeto automatiza o fluxo completo de geração, simulação e verificação de um filtro FIR digital usando Python para gerar arquivos Verilog (módulo e testbench), simular no ModelSim (ou outro ambiente FPGA) e comparar os resultados com uma referência implementada no próprio Python.

⚙️ 1. Geração do Código Verilog – gerar_verilog()
Esta função em Python gera automaticamente um módulo Verilog (FIR.v) que implementa um filtro FIR com os seguintes elementos:

Linha de atraso para armazenar entradas anteriores (delay_line[])

Vetor de coeficientes (coeffs[]), com os valores vindos do código Python.

Estrutura de acumulador que realiza a convolução FIR.

Saída assinada com largura de bits suficiente para evitar overflow.

A largura da saída é calculada por:
### Fórmula:
###     Nbout = Nbs + Nbf - 1 + ceil(log2(ordem))
###
### Onde:
###     Nbs   = número de bits da entrada (ex: 16 bits do ADC)
###     Nbf   = número de bits dos coeficientes do filtro
###     ordem = número de coeficientes - 1 (ordem do filtro FIR)

🧪 2. Geração do Testbench – gerar_testbench()
Esta função gera um arquivo Verilog (fir_tb.v) que implementa o testbench automatizado. Ele realiza as seguintes tarefas:

Gera um clock de 8 kHz.

Lê amostras de entrada do arquivo input_signal.txt.

Aplica essas amostras ao módulo FIR.

Escreve as saídas simuladas em dois arquivos:

output_data.txt (todos os bits da saída)

output_data16.txt (apenas os 16 LSBs da saída)

⚠️ Atenção: É necessário editar os caminhos dos arquivos no código para que apontem para as pastas corretas no seu computador (entrada e saída devem estar no mesmo diretório do ModelSim ou da ferramenta de simulação Verilog).

🧾 3. Fluxo de Execução Completo
Gerar o sinal de entrada em Python usando o script principal (base):

Um sinal de teste é criado com harmônicos e ruído.

Este sinal é quantizado e salvo em input_signal.txt.

Executar as funções gerar_verilog() e gerar_testbench():

Estas funções criam automaticamente os arquivos Verilog do filtro e do testbench, já prontos para simulação.

Rodar a simulação no ModelSim (ou similar):

Carregue fir_tb.v, compile e simule o testbench.

Isso irá gerar automaticamente os arquivos output_data.txt e output_data16.txt.

Executar novamente o script Python base para comparação:

O script irá ler os arquivos de saída da simulação Verilog.

Comparar as respostas do FPGA com a resposta esperada em Python.

Plotar os sinais sobrepostos.

Calcular o erro quadrático médio (MSE) entre as respostas.

📊 4. Saídas do Verilog
output_data.txt: saída do filtro FIR completa com largura total de bits.

output_data16.txt: saída truncada para 16 bits (útil para visualização ou uso em blocos com limitação de largura de barramento).


