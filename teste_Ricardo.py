import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, lfilter, firls
import sinaisIEC60255_118
from teste import gerar_verilog
from teste_bench import gerar_testbench


#===================================================
# Parâmetros
#===================================================
"""
Definição dos parâmetros principais do sinal, incluindo frequência nominal, 
frequência de amostragem, frequência de reporte, número de pontos por ciclo, 
número de ciclos simulados, e vetores de tempo.
"""
f0 = 60      # Frequência nominal (Hz)
Fs = 8000    # Frequência de amostragem (Hz)
Fr = 50      # Frequência de reporte (Hz)

Nppc = Fs / f0  # Número de pontos por ciclo
Nc = 10         # Número de ciclos

t = np.arange(Nc * Nppc) / Fs  # Vetor de tempo

# Parâmetros do sinal gerado
f1 = 60       # Frequência do sinal
hmax = 30     # Ordem harmônica máxima
hmag = 0.1    # Magnitude dos harmônicos
SNR = 600000  # Relação Sinal-Ruído (dB)

fm = 5   # Frequência da modulação
kx = 0.1 # Índice de modulação em fase
ka = 0   # Índice de modulação em amplitude


#===================================================
# Geração do Sinal de Teste
#===================================================
"""
Gera um sinal de teste usando a função signal_frequency do módulo sinaisIEC60255_118.
"""
x, Xr, f1r, ROCOFr = sinaisIEC60255_118.signal_frequency(f1, Nc*Nppc, f0, Fs, Fr, hmax, hmag, SNR)

# Plot do sinal gerado
plt.figure(figsize=(10, 4))
plt.plot(t, x, label='Sinal de Teste')
plt.grid()
plt.xlabel('Tempo (s)')
plt.ylabel('Magnitude')
plt.title('Sinal de Teste Gerado')
plt.legend()
plt.show()


#===================================================
# Quantização do Sinal
#===================================================
Nbs = 16  # Número de bits para quantização do sinal

xQ = (x/4) * (2**(Nbs-1)) # sinal quantizado --> a maior amplitude do sinal é 4 e para esse caso precisa estar entre -1 e 1 
xQ = np.round(xQ) # Arredondando a ultima casa

# Salvando o sinal quantizado em arquivo
with open(r"C:\Users\Ricardo\Documents\FPGA\Filtro_Manso\Filtro\simulation\modelsim\input_signal.txt", "w") as arquivo:
    for amostra in xQ:
        arquivo.write(f"{int(amostra)}\n")

print("Arquivo salvo com sucesso!")

# Plot do sinal quantizado
plt.figure(figsize=(10, 4))
plt.plot(t, xQ, label='Sinal Quantizado', color='purple')
plt.grid()
plt.xlabel('Tempo (s)')
plt.ylabel('Magnitude')
plt.title('Sinal Quantizado')
plt.legend()
plt.show()


#===================================================
# Projeto do Filtro FIR
#===================================================
ordem = 15 ## ordem do filtro 
frequencias = [0, 65/(Fs/2), 1000/(Fs/2), 1]
ganhos = [1, 1, 0, 0]
b = firls(ordem, frequencias, ganhos)

omega, h = freqz(b, 1, 4096)

# Plot da resposta em frequência do filtro
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(omega * Fs / (2 * np.pi), abs(h), label='Resposta de Magnitude')
plt.grid()
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.title('Resposta em Frequência do Filtro FIR')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(omega * Fs / (2 * np.pi), (180/np.pi) * np.unwrap(np.angle(h)), label='Fase')
plt.grid()
plt.xlabel('Frequência (Hz)')
plt.ylabel('Fase (°)')
plt.legend()
plt.show()

# Plot dos coeficientes do filtro FIR
plt.figure(figsize=(10, 4))
plt.plot(b, label='Coeficientes do Filtro')
plt.grid()
plt.xlabel('Ordem do Filtro')
plt.ylabel('Coeficiente')
plt.title('Coeficientes do Filtro FIR')
plt.legend()
plt.show()


#===================================================
# Quantização do Filtro
#===================================================
Nbf = 4# Número de bits para quantização do filtro
bQ = np.round(b * (2**(Nbf-1)))
print("Coeficientes quantizados:", bQ)


#===================================================
# Aplicação do Filtro no Sinal Quantizado
#===================================================
yQ = np.round(lfilter(bQ, 1, xQ))

plt.figure(figsize=(10, 4))
plt.stem(t, yQ, label='Sinal Filtrado')
plt.grid()
plt.xlabel('Tempo (s)')
plt.ylabel('Magnitude')
plt.title('Sinal Filtrado pelo Filtro FIR Quantizado')
plt.legend()
plt.show()


#===================================================
# Leitura do Arquivo Gerado pelo FPGA
#===================================================
#fir_fpga = np.loadtxt("output_data.txt", dtype=int)
fir_fpga = np.loadtxt( r"C:\Users\Ricardo\Documents\FPGA\Filtro_Manso\Filtro\simulation\modelsim\output_data.txt", dtype=int)
fir_fpga = fir_fpga 
fir_fpga = fir_fpga[:len(yQ)]

tempo_fpga = t[:len(fir_fpga)]
yQ = yQ[:len(fir_fpga)]


#===================================================
# Leitura do Arquivo Gerado pelo FPGA 16bits de saída
#===================================================
#fir_fpga16 = np.loadtxt("output_data16.txt", dtype=int)
fir_fpga16 = np.loadtxt(r"C:\Users\Ricardo\Documents\FPGA\Filtro_Manso\Filtro\simulation\modelsim\output_data16.txt", dtype=int)

fir_fpga16 = fir_fpga16 
fir_fpga16 = fir_fpga[:len(yQ)]


#===================================================
# Comparação do Filtro FIR no FPGA e no Python
#===================================================
plt.figure(figsize=(10, 5))
plt.plot(fir_fpga, label="FPGA - Filtro FIR", linestyle='dashed', color='r')
plt.plot(yQ, label="Python - Filtro FIR", linestyle='solid', color='b')
plt.plot(fir_fpga16,label="FPGA - Filtro FIR 16 bits", linestyle='dashed', color='g')
plt.grid()
plt.xlabel("Tempo (s)")
plt.ylabel("Magnitude")
plt.title("Comparação: FPGA vs Python - Filtro FIR")
plt.legend()
plt.show()


gerar_verilog(bQ, ordem, Nbs=Nbs, Nbf=Nbf)
gerar_testbench(ordem, Nbs=Nbs, Nbf=Nbf, guard_bits = 0) ##


# ------------------------ MSE ---------------------------------------
MSE1 = np.mean((yQ - fir_fpga) ** 2) ## Sinal original e o sinal de 32 bits 
print(f"Erro Quadrático Médio (MSE) : {MSE1:.6f}")
MSE1 = np.mean((yQ - fir_fpga16) ** 2) ## Sinal original e o sinal de 32 bits 
print(f"Erro Quadrático Médio (MSE) para saída de 16bits: {MSE1:.6f}")