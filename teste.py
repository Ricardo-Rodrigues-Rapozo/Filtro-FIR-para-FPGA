import numpy as np

#def gerar_verilog(coeffs, ordem, Nbs, Nbf, arquivo='fir_filter.v'):
def gerar_verilog(coeffs, ordem, Nbs, Nbf, arquivo=r"C:\Users\Ricardo\Documents\FPGA\Filtro_Manso\Filtro\FIR.v"):

    """
    Gera um código Verilog atualizado automaticamente com:
    - Os coeficientes do filtro FIR,
    - O número de bits da entrada e da saída,
    - A ordem do filtro FIR.
    
    Parâmetros:
        coeffs (list or np.array): Lista de coeficientes quantizados gerados no Python.
        ordem (int): Ordem do filtro FIR (quantidade de coeficientes - 1).
        Nbs (int): Número de bits para representar a entrada 
        Nbf (int): Número de bits para representar os coeficientes do filtro FIR (igual a Nbs por padrão).
        arquivo (str): Nome do arquivo Verilog de saída.
    """
    Nbout = (Nbs + Nbf) - 1 + int(np.ceil(np.log2(ordem)))  # Cálculo do número de bits da saída considerando o acúmulo das multiplicações

    with open(arquivo, 'w') as f:
        f.write("""
module FIR #(
    parameter NUBITS = {},
    parameter NBITS_OUT = {},
    parameter ORDER = {}
)(
    input clk, rst,
    input signed [NUBITS-1:0] io_out,
    output signed [NBITS_OUT-1:0] delayed_out 
);

    reg signed [NBITS_OUT-1:0] acc; // Acumulador para soma ponderada
    reg signed [NUBITS-1:0] delay_line [0:ORDER-1]; // Linha de atraso para armazenar amostras passadas
    reg signed [NUBITS-1:0] coeffs [0:ORDER-1]; // Coeficientes do filtro FIR
    reg signed [NBITS_OUT-1:0] y; // Saída filtrada

    initial begin
        """.format(Nbs, Nbout, ordem))
        
        # Escrever coeficientes com a mesma representação do Python
        for i, c in enumerate(coeffs):
            f.write(f"        coeffs[{i}] = {Nbf}'sd{int(c)};\n")
        
        f.write("""
    end

    integer i;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < ORDER; i = i + 1)
                delay_line[i] <= 0; // Resetar valores na linha de atraso
        end else begin
            for (i = ORDER-1; i > 0; i = i - 1)
                delay_line[i] <= delay_line[i-1]; // Deslocamento dos valores
            
            delay_line[0] <= io_out; // Atualizar a entrada mais recente
        end
    end

    always @* begin
        acc = 0;
        for (i = 0; i < ORDER; i = i + 1)
            acc = acc + coeffs[i] * delay_line[i]; // Convolução FIR
        y <= acc;
    end

    assign delayed_out = y; // Atribuição da saída

endmodule
""")
    print(f"Arquivo {arquivo} gerado com sucesso!")

# Exemplo de uso
# Nbs = 5  # Número de bits para a entrada e coeficientes
# Nbf = Nbs  # Número de bits para representar os coeficientes do filtro FIR (igual à entrada)
# dummy_coeffs = np.round(np.random.rand(5) * (2**(Nbf-1)))  # Gera coeficientes aleatórios para teste
# print(dummy_coeffs)
# gerar_verilog(dummy_coeffs, ordem=len(dummy_coeffs), Nbs=Nbs, Nbf=Nbf)
