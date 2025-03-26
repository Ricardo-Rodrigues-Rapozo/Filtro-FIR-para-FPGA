import numpy as np

#def gerar_testbench(ordem=15, Nbs=16, Nbf=16, guard_bits=0, arquivo='fir_tb.v'):
def gerar_testbench(ordem=15, Nbs=16, Nbf=16, guard_bits=0, arquivo=r"C:\Users\Ricardo\Documents\FPGA\Filtro_Manso\Filtro\fir_tb.v"):

    """
    Gera um testbench Verilog atualizado automaticamente com:
    - Configuração dos bits da entrada, coeficientes e saída.
    - Cálculo automático do número de bits da saída.
    - Leitura e escrita de arquivos de entrada e saída.
    
    Parâmetros:
        ordem (int): Ordem do filtro FIR (quantidade de coeficientes - 1).
        Nbs (int): Número de bits para representar a entrada.
        Nbf (int): Número de bits para representar os coeficientes do filtro FIR.
        guard_bits (int): Número de bits extras para evitar overflow.
        arquivo (str): Nome do arquivo Verilog de saída.
    """
    Nbout = (Nbf + Nbs) - 1 + int(np.ceil(np.log2(ordem))) + guard_bits
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(f"""
`timescale 1us / 1ns // O segundo é o passo que ModelSim faz os cálculos

module fir_tb();

// ============================
// Parâmetros configuráveis
// ============================
parameter Nbs = {Nbs};  // Número de bits da entrada
parameter Nbf = {Nbf};  // Número de bits dos coeficientes
parameter Nbout = {Nbout}; // Bits da saída considerando overflow

// ============================
// Variáveis necessárias
// ============================
reg clk, rst;
reg signed [Nbs-1:0] x; // Entrada
wire signed [Nbout - 1:0] y; // Saída corrigida para 32 bits
integer input_data, output_data, output_data16;
integer scan_result; // Variável para armazenar o retorno do $fscanf

// ============================
// Gerando o clock
// ============================
always #62.5 clk = ~clk; // Clock de 8 kHz

// ============================
// Inicialização
// ============================
initial begin
    clk = 0;
    rst = 1;
    x = 0;
    
    #5 rst = 0; // Desativa o reset após 5 us

    // Abrindo arquivos
    input_data = $fopen("input_signal.txt", "r");
    output_data = $fopen("output_data.txt", "w");
    output_data16 = $fopen("output_data16.txt","w");


    if (input_data == 0) begin
        $display("Erro ao abrir input_signal.txt");
        $finish;
    end

    if (output_data == 0) begin
        $display("Erro ao abrir output_data.txt");
        $finish;
    end
    	 
    if (output_data16 == 0) begin
        $display("Erro ao abrir output_data16.txt");
        $finish;
    end
end

// ============================
// Leitura e Escrita
// ============================
always @ (posedge clk)
begin
    scan_result = $fscanf(input_data, "%d", x); // Lendo do arquivo de entrada
    $fwrite(output_data, "%d\\n", y); // Escrevendo no arquivo de saída
    $fwrite(output_data16, "%d\\n", y[15:0]); // Escrevendo no arquivo de saída
end

// ============================
// Instanciação do módulo FIR
// ============================
FIR DUT (
    .clk(clk),
    .rst(rst),
    .io_out(x),
    .delayed_out(y)
);

endmodule
""")
    print(f"Arquivo {arquivo} gerado com sucesso!")

# Exemplo de uso
# ordem = 15  # Ordem do filtro FIR
# Nbs = 16  # Número de bits para a entrada
# Nbf = 16  # Número de bits para coeficientes
# guard_bits = 4  # Bits extras para evitar overflow

# gerar_testbench(ordem=ordem, Nbs=Nbs, Nbf=Nbf, guard_bits=guard_bits)
