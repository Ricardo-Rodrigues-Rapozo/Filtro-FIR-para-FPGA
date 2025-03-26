import numpy as np

# Testes Estacionarios

def signal_frequency(f1, N, f0, Fs, Frep, hmax, hmag, SNR):
    """ Gera sinais para o teste Signal Frequency segundo a norma IEC/IEEE 60255-118
    Parameters:
    -----------
        f1 (float): Frequência do sinal
        N (integer): Número de pontos do sinal gerado
        f0 (float): Frequência nominal
        Fs (float): Frequência de Amostragem
        Frep (float): Frequência de Reporte
        hmax (integer): Ordem harmônica máxima presente no sinal gerado
        hmag (float): Magnitude (em relação à fundamental) dos harmônicos gerados 
        SNR (float): Relação Sinal Ruído em dB

    Returns:
    --------
        x (array ): Amplitude do sinal
        X (complex array): Frequência do sinal
        f (array): Número de pontos do sinal gerado
        ROCOF (array): Frequência nominal
    """

    status = True
    if Frep < 10:
        if abs(f1-f0) > 2:
            raise TypeError('Frequencia do sinal fora do intervalo estipulado pela norma')
    elif Frep < 25:
        if abs(f1-f0) > Frep/5:
            raise TypeError('Frequencia do sinal fora do intervalo estipulado pela norma')
    else:
        if Frep >= 25:
            if abs(f1-f0) > 5:
                raise TypeError('Frequencia do sinal fora do intervalo estipulado pela norma') 
    
    if(status == False):
        return 0
    else:
        t = np.arange(N)/Fs
        var_ruido = (1/2)*(10**(-SNR/10))
        ruido = np.sqrt(var_ruido)*np.random.randn(len(t))


        phi = 0#np.random.uniform(-np.pi,np.pi)

        x = np.cos(2*np.pi*f1*t + phi)

        X = np.zeros((hmax,len(t))) + 1j*np.zeros((hmax,len(t)))
        X[0,:] = (1/np.sqrt(2))*np.exp(1j*(2*np.pi*(f1-f0)*t + phi))

        for hh in range(2,hmax+1):
            phi = 0#np.random.uniform(-np.pi,np.pi)
            x = x + hmag*np.cos(2*np.pi*hh*f1*t + phi)
            
            X[hh-1,:] = (hmag/np.sqrt(2))*np.exp(1j*(2*np.pi*hh*(f1-f0)*t + phi))
        
        x = x + ruido

        f = f1*np.ones(len(x))
        ROCOF = np.zeros(len(x))

        return (x, X, f, ROCOF)
    
def frequency_ramp(Rf, N, f0, fa, Fs, Frep, hmax, hmag, SNR):
    """ Gera sinais para o teste Signal Frequency segundo a norma IEC/IEEE 60255-118
    Parameters:
    -----------
        f1 (float): Frequência do sinal
        N (integer): Número de pontos do sinal gerado
        f0 (float): Frequência nominal
        Fs (float): Frequência de Amostragem
        Frep (float): Frequência de Reporte
        hmax (integer): Ordem harmônica máxima presente no sinal gerado
        hmag (float): Magnitude (em relação à fundamental) dos harmônicos gerados 
        SNR (float): Relação Sinal Ruído em dB

    Returns:
    --------
        x (array ): Amplitude do sinal
        X (complex array): Frequência do sinal
        f (array): Número de pontos do sinal gerado
        ROCOF (array): Frequência nominal
    """

    t = np.arange(N)/Fs
    var_ruido = (1/2)*(10**(-SNR/10))
    ruido = np.sqrt(var_ruido)*np.random.randn(len(t))


    phi = 0#np.random.uniform(-np.pi,np.pi)
    x = np.cos(2*np.pi*fa*t + np.pi*Rf*t**2 + phi)

    X = np.zeros((hmax,len(t))) + 1j*np.zeros((hmax,len(t)))
    X[0,:] = (1/np.sqrt(2))*np.exp(1j*(np.pi*Rf*t**2 + 2*np.pi*(fa-f0)*t + phi))

    for hh in range(2,hmax+1):
        phi = 0#np.random.uniform(-np.pi,np.pi)
        x = x + hmag*np.cos(hh*(2*np.pi*fa*t + np.pi*Rf*t**2) + phi)
        
        X[hh-1,:] = (hmag/np.sqrt(2))*np.exp(1j*(hh*(np.pi*Rf*t**2 + 2*np.pi*(fa-f0)*t) + phi))
    
    #x = x + ruido

    f = fa + Rf*t

    ROCOF = Rf*np.ones(len(f))
    
    return (x, X, f, ROCOF)


def sinusoidal_frequency(freqF, AmpF, N, f0, Fs, Frep, hmax, hmag, SNR):
    """ Gera sinais para o teste Signal Frequency segundo a norma IEC/IEEE 60255-118
    Parameters:
    -----------
        freqF (float): Frequência da Variação Senoidal
        AmpF (float): Amplitude da Variação
        N (integer): Número de pontos do sinal gerado
        f0 (float): Frequência nominal
        Fs (float): Frequência de Amostragem
        Frep (float): Frequência de Reporte
        hmax (integer): Ordem harmônica máxima presente no sinal gerado
        hmag (float): Magnitude (em relação à fundamental) dos harmônicos gerados 
        SNR (float): Relação Sinal Ruído em dB

    Returns:
    --------
        x (array ): Amplitude do sinal
        X (complex array): Frequência do sinal
        f (array): Número de pontos do sinal gerado
        ROCOF (array): Frequência nominal
    """

    t = np.arange(N)/Fs
    var_ruido = (1/2)*(10**(-SNR/10))
    ruido = np.sqrt(var_ruido)*np.random.randn(len(t))


    phi = 0#np.random.uniform(-np.pi,np.pi)

    x = np.cos(2*np.pi*f0*t + (-AmpF/freqF)*(np.cos(2*np.pi*freqF*t) - 1) + phi)

    X = np.zeros((hmax,len(t))) + 1j*np.zeros((hmax,len(t)))
    X[0,:] = (1/np.sqrt(2))*np.exp(1j*((-AmpF/freqF)*(np.cos(2*np.pi*freqF*t) - 1) + phi))

    for hh in range(2,hmax+1):
        phi = 0#np.random.uniform(-np.pi,np.pi)
        x = x + hmag*np.cos(2*np.pi*f0*t + (-AmpF/freqF)*(np.cos(2*np.pi*freqF*t) - 1) + phi)
        
        X[hh-1,:] = (hmag/np.sqrt(2))*np.exp(1j*(hh*(-AmpF/freqF)*(np.cos(2*np.pi*freqF*t) - 1) + phi))
    
    x = x + ruido

    f = f0 + AmpF*np.sin(2*np.pi*freqF*t)
    ROCOF = np.zeros(len(x))

    return (x, X, f, ROCOF)

def modulation(fm, kx, ka, N, f0, Fs, Frep, hmax, hmag, SNR):
    """ Gera sinais para o teste Signal Frequency segundo a norma IEC/IEEE 60255-118
    Parameters:
    -----------
        f1 (float): Frequência do sinal
        N (integer): Número de pontos do sinal gerado
        f0 (float): Frequência nominal
        Fs (float): Frequência de Amostragem
        Frep (float): Frequência de Reporte
        hmax (integer): Ordem harmônica máxima presente no sinal gerado
        hmag (float): Magnitude (em relação à fundamental) dos harmônicos gerados 
        SNR (float): Relação Sinal Ruído em dB

    Returns:
    --------
        x (array ): Amplitude do sinal
        X (complex array): Frequência do sinal
        f (array): Número de pontos do sinal gerado
        ROCOF (array): Frequência nominal
    """

    t = np.arange(N)/Fs
    var_ruido = (1/2)*(10**(-SNR/10))
    ruido = np.sqrt(var_ruido)*np.random.randn(len(t))


    phi = 0#np.random.uniform(-np.pi,np.pi)
    x = (1 + kx*np.cos(2*np.pi*fm*t))*np.cos(2*np.pi*f0*t + ka*np.cos(2*np.pi*fm*t - np.pi) + phi)

    X = np.zeros((hmax,len(t))) + 1j*np.zeros((hmax,len(t)))
    X[0,:] = (1/np.sqrt(2))*(1 + kx*np.cos(2*np.pi*fm*t))*np.exp(1j*(ka*np.cos(2*np.pi*fm*t - np.pi) + phi))

    for hh in range(2,hmax+1):
        phi = 0#np.random.uniform(-np.pi,np.pi)
        x = x + hmag*(1 + kx*np.cos(2*np.pi*fm*t))*np.cos(2*np.pi*hh*f0*t + ka*np.cos(2*np.pi*fm*t - np.pi) + phi)
        
        X[hh-1,:] = (hmag/np.sqrt(2))*(1 + kx*np.cos(2*np.pi*fm*t))*np.exp(1j*(ka*np.cos(2*np.pi*fm*t - np.pi) + phi))
    
    #x = x + ruido

    f = f0 - ka*fm*np.sin(2*np.pi*t - np.pi)

    ROCOF = - ka*2*np.pi*(fm**2)*np.cos(2*np.pi*t - np.pi)
    
    return (x, X, f, ROCOF)
