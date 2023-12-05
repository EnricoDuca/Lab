import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, constants
from scipy.fft import ifft, rfft

def valori_piu_grandi(array,n_massimi):
    indici_ordinati = np.argsort(array)[::-1]
    valori_max = array[indici_ordinati[:n_massimi]]
    return valori_max

def func(a,b,valore):
    dic={}
    for elem1,elem2 in zip(a,b):
        dic[elem1]=elem2
    return dic[valore]

def trova_picchi_potenza(frequenze, potenze, intervallo_frequenza):
    picchi = []
    frequenza_picchi=[]
    potenza_picchi=[]


    for i in range(len(potenze)):
        frequenza = frequenze[i]
        potenza = potenze[i]
        
        # intervallo di frequenza intorno al punto 
        indice_inizio = max(0, i - intervallo_frequenza)
        indice_fine = min(len(potenze), i + intervallo_frequenza + 1)
        
        # Trova il massimo locale all'interno dell'intervallo 
        if potenza == max(potenze[indice_inizio:indice_fine]):
            picchi.append((frequenza, potenza))
            frequenza_picchi.append(frequenza)
            potenza_picchi.append(potenza)

            
    
    return picchi,frequenza_picchi,potenza_picchi

data, samplerate = sf.read('./pulita_pezzo.wav')

#sf.write('./pulita_pezzo_recreated.wav', data, samplerate)

time = np.linspace(0, len(data)/samplerate, len(data))

plt.plot(time,data[:,0])
plt.show()

datafft = fft.rfft(data[:,0])

fftfreq =fft.rfftfreq(len(data[:,0]),1/samplerate)

#plot potenza vs freq

plt.figure(20)
fig = plt.gcf()
fig.set_size_inches(6, 6)
plt.title("FFT")
plt.xlabel('Frequenza (hz)')
plt.ylabel('Potenza(u.a.)')
plt.plot(fftfreq[:len(datafft)],   (abs(datafft[:len(datafft)]))**2)
plt.show()

#plot coefficienti fft

r=datafft.real
coeff_imm=datafft.imag

#print('Coefficienti reali: ',r)
#print('Coefficienti immaginari: ',i)

plt.plot(fftfreq[:len(r)], r)
plt.show()

plt.plot(fftfreq[:len(coeff_imm)], coeff_imm)
plt.show()

potenze = abs(datafft[:len(datafft)])**2

#identificazione picchi e note
valori,freq_picchi,pot_picchi= trova_picchi_potenza(fftfreq[:len(datafft)], potenze, 50)

# for picco in valori:
#     frequenza_picco, potenza_picco = picco
#     print("Frequenza: {}, Potenza: {}".format(frequenza_picco, potenza_picco))

def primi_n_valori(lista, n):
    return lista[:n]

primi_valori = primi_n_valori(valori, 250)

for picco2 in primi_valori:
    frequenza_picco2, potenza_picco2 = picco2
    print("Frequenza: {}, Potenza: {}".format(frequenza_picco2, potenza_picco2))

freq_filtrati=primi_n_valori(freq_picchi,250)
pot_filtrate=primi_n_valori(pot_picchi,250)

plt.figure(20)
fig = plt.gcf()
fig.set_size_inches(6, 6)
plt.title("FFT")
plt.xlabel('Frequenza (hz)')
plt.ylabel('Potenza(u.a.)')
plt.plot(fftfreq[:len(datafft)],   (abs(datafft[:len(datafft)]))**2)
plt.scatter(freq_filtrati,   pot_filtrate)
plt.show()
