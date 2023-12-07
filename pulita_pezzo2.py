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

def trova_indici(n):
    for j in range(0,len(potenze)):
        if (potenze[j] == n):
            return j

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

indice_valore=trova_indici(483053.6245658862)

print('Indice è: ',indice_valore)

print('La potenza di indice 50314 è: ',potenze[indice_valore])

somma = 0
for i in potenze[:indice_valore]:
    somma = somma+i
print('La media delle potenze è: ', somma/len(potenze[:indice_valore]))

#identificazione picchi e note

valori,freq_picchi,pot_picchi = trova_picchi_potenza(fftfreq[:len(datafft)], potenze, 300)

# for picco in valori:
#     frequenza_picco, potenza_picco = picco
#     print("Frequenza: {}, Potenza: {}".format(frequenza_picco, potenza_picco))

def primi_n_valori(lista, n):
    return lista[:n]

primi_valori = primi_n_valori(valori, 9000)

for picco2 in primi_valori:
    frequenza_picco2, potenza_picco2 = picco2
    print("Frequenza: {}, Potenza: {}".format(frequenza_picco2, potenza_picco2))

prime_n_freq=primi_n_valori(freq_picchi,9000)
prime_n_pot=primi_n_valori(pot_picchi,9000)

pot_filtrate=[]
for i in prime_n_pot:
    if i > somma/len(potenze[:indice_valore]):
        pot_filtrate.append(i)

#print(pot_filtrate)
#print(len(pot_filtrate))

freq_filtrate=[]
for i in pot_filtrate:
    freq_filtrate.append(func(prime_n_pot,prime_n_freq,i))

# print('Le frequenze filtrate sono: ', freq_filtrate,len(freq_filtrate))
# print('Le potenze filtrate sono: ', pot_filtrate,len(pot_filtrate))

plt.figure(20)
fig = plt.gcf()
fig.set_size_inches(6, 6)
plt.xlabel('Frequenza (hz)')
plt.title('Potenze picchi principali')
plt.plot(fftfreq[:len(datafft)],   (abs(datafft[:len(datafft)]))**2)
plt.axhline(y=somma/len(potenze[:indice_valore]),linestyle='--')
plt.scatter(freq_filtrate,   pot_filtrate)
plt.show()

## il picco principale

mask1 = potenze == max(pot_filtrate)

freq_mask1 = fftfreq*mask1

data_mask1 = datafft*mask1

antitrasf=fft.irfft(data_mask1,n=len(time))

#print(antitrasf)

plt.title('Antitrasformata con picco principale')
plt.xlabel('Time')
plt.plot(time, antitrasf)
plt.show()

##  primi due picchi principali, ma solo il termine "centrale"

mask2 = np.logical_or(potenze == max(pot_filtrate), potenze == 4604783.2157635745)

#print('maschera frequenze: ',fftfreq[mask2], 'maschera potenze: ',datafft[mask2])

freq_mask2 = fftfreq*mask2

data_mask2 = datafft*mask2

antitrasf2=fft.irfft(data_mask2,n=len(time))

plt.title('Antitrasformata con primi due picchi principali')
plt.xlabel('Time')
plt.plot(time,antitrasf2)
plt.show()

##  primi picchi principali, ma solo il termine "centrale"

mask3 = np.any([potenze == picco for picco in pot_filtrate], axis = 0)

#print('maschera frequenze: ',fftfreq[mask3], 'maschera potenze: ',datafft[mask3])

freq_mask3 = fftfreq*mask3

data_mask3 = datafft*mask3

antitrasf3=fft.irfft(data_mask3,n=len(time))

plt.title('Antitrasformata con primi picchi principali ma solo il termine centrale')
plt.xlabel('Time')
plt.plot(time,antitrasf3)
plt.show()

## i picchi principali con anche 1 o 2 termini, per lato, oltre quello centrale

valori3,freq_picchi3,pot_picchi3= trova_picchi_potenza(fftfreq[:len(datafft)], potenze, 0)

primi_valori3 = primi_n_valori(valori3, 55000)
prime_n_freq3=primi_n_valori(freq_picchi3,55000)
prime_n_pot3=primi_n_valori(pot_picchi3,55000)

pot_filtrate_dx_sx = []
for i in prime_n_pot3:
    if i > somma/len(potenze[:indice_valore]):
        pot_filtrate_dx_sx.append(i)

freq_filtrate_dx_sx=[]
for i in pot_filtrate_dx_sx:
    freq_filtrate_dx_sx.append(func(prime_n_pot3,prime_n_freq3,i))

pot_finali=[]
for i in range(0,len(pot_filtrate_dx_sx)):
    for j in range(0,len(pot_filtrate)):
        if pot_filtrate_dx_sx[i] == pot_filtrate[j]:
            pot_finali.append(pot_filtrate_dx_sx[i-2])
            pot_finali.append(pot_filtrate_dx_sx[i-1])
            pot_finali.append(pot_filtrate_dx_sx[i])
            pot_finali.append(pot_filtrate_dx_sx[i+1])
            pot_finali.append(pot_filtrate_dx_sx[i+2])

freq_finali=[]
for i in pot_finali:
    freq_finali.append(func(prime_n_pot3,prime_n_freq3,i))

plt.figure(20)
fig = plt.gcf()
fig.set_size_inches(6, 6)
plt.xlabel('Frequenza (hz)')
plt.title('Potenze picchi principali e due dati a destra e sinistra')
plt.plot(fftfreq[:len(datafft)],   (abs(datafft[:len(datafft)]))**2)
plt.axhline(y=somma/len(potenze[:indice_valore]))
plt.scatter(freq_finali,   pot_finali)
plt.show()

mask4 = np.any([potenze == picco for picco in pot_finali], axis = 0)

freq_mask4 = fftfreq*mask4

data_mask4 = datafft*mask4

antitrasf4=fft.irfft(data_mask4,n=len(time))

plt.title('Antitrasformata con picchi principali e i valori più vicini per ogni lato di ognuno')
plt.xlabel('Time')
plt.plot(time,antitrasf4)
plt.show()

sf.write('./pulita_pezzo_recreated.wav', antitrasf4, samplerate)
