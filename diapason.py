import soundfile as sf
import numpy as np
import array as arr
import matplotlib.pyplot as plt
from scipy import fft, constants
from scipy.fft import ifft, rfft


def func(a,b,valore):
    dic={}
    for elem1,elem2 in zip(a,b):
        dic[elem1]=elem2
    return dic[valore]

data, samplerate = sf.read('./diapason.wav')

#print(samplerate)
#print(data)
#print(len(data))

#print(type(samplerate))
#print(type(data))

sf.write('./diapason_recreated.wav', data, samplerate)

time = np.linspace(0, len(data)/samplerate, len(data))

plt.plot(time,data[:,0])
plt.show()

datafft = fft.rfft(data[:,0])

fftfreq =fft.rfftfreq(len(data[:,0]),1/samplerate)

#print('i coefficienti sono: ',datafft)
#print(len(datafft))
#print('Frequenze: ',fftfreq)
#print(len(fftfreq))

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

#identificazione picchi e note

def trova_massimo(a,b):
    dic={}
    ymax=max(a)
    for elem1,elem2 in zip(a,b):
        dic[elem1]=elem2
    return dic[ymax], ymax

#lista_filtrata_y=(abs(datafft[:len(datafft)])**2)
#lista_filtrata_y= [x for x in (abs(datafft[:len(datafft)])**2) if  (x < 1600000)]
lista_filtrata_y= [x for x in (abs(datafft[:len(datafft)])**2) if (x < 247602.88594849446)]

p1=trova_massimo(lista_filtrata_y, fftfreq[:len(datafft)])
print('Il picco è: ',p1)


#print(func((abs(datafft[:len(datafft)])**2),fftfreq[:len(datafft)]),p1)


#Il primo picco è (110.24999999999999,9954056.90923407) --> nota: La2
#Il secondo picco è (880.2499999999999, 1464080.3327664384) --> nota: La5
#Il terzo picco è (1980.4166666666665,222884.8301838864) --> nota: Si6

massimi = np.array([9954056.90923407,1464080.3327664384,222884.8301838864])
'''
def trova_piu_massimi(array):
    indici_massimi = np.argwhere(array == np.max(array)).flatten()
    valori_massimi = array[indici_massimi]
    return indici_massimi, valori_massimi


indici, valori = trova_piu_massimi(abs(datafft[:len(datafft)])**2)

print("Indici dei massimi:", indici)
print("Valori dei massimi:", valori)
'''


def valori_piu_grandi(array,n_massimi):
    indici_ordinati = np.argsort(array)[::-1]
    valori_max = array[indici_ordinati[:n_massimi]]
    return valori_max

valori = valori_piu_grandi(abs(datafft[:len(datafft)])**2,20)

for i in valori:
    print("I valori più grandi sono : ", i, 'La frequenza corrispondente è: ', func(abs(datafft[:len(datafft)])**2, fftfreq[:len(datafft)], i))

#larghezza a mezza altezza

max2=1464080.33276644
max2_mezzo=max2/2

def trova_punto_prima_dopo(arr2,valore):
    for i in range(0,len(datafft)):
        if arr2[i]==valore:
            return arr2[i-1], arr2[i+1]

'''
def trova_massimo(arr2,valore):
    arr1=arr.array(0)
    for i in range (0,len(arr2)):
        n=valore-arr2[i]
        arr1.append(n)
    plus=arr1>0
    minus=arr1<0
    sorted_plus=np.sort(plus)
    print('il punto precedente è: ',sorted_plus[0])
    sorted_minus=np.sort(minus)
    l=(len(sorted_minus))
    print('il punto successivo è:',sorted_minus[l])


trova_massimo(abs(datafft[:len(datafft)])**2,1464080.33276644)

p=trova_punto_prima_dopo(abs(datafft[:len(datafft)])**2,1464080.33276644)
print(p)
'''

# mascherare (i.e. mettere a zero) i coefficienti tranne alcuni "scelti"

potenze = abs(datafft[:len(datafft)])**2
picco_princ = max(valori)
picchi=np.array([picco_princ,valori[2],valori[9],valori[1],valori[3],valori[4],valori[5],valori[12],valori[16]])
freq_=np.array([110.24999999999999,880.2499999999999,1980.4166666666665,109.66666666666666,110.83333333333331,880.8333333333333,879.6666666666665, 1980.9999999999998,1979.833333333333])


## il picco principale

mask1 = potenze == picco_princ

freq_mask1 = fftfreq*mask1

data_mask1 = datafft*mask1

antitrasf=fft.irfft(data_mask1)

plt.title('Antitrasformata con picco principale')
plt.xlabel('Time')
plt.plot(time,antitrasf)
plt.show()

#codice per verificare il corretto funzionamento della maschera

# print(fftfreq[mask1], datafft[mask1])

# indici_freq_filtrati=np.argsort(fftfreq*mask1)[::-1]
# indici_coeff_filtrati=np.argsort(datafft*mask1)[::-1]

# print(datafft[indici_coeff_filtrati[0]],fftfreq[indici_freq_filtrati[0]])

# elementi_diversi_da_zero=[]

# for elem in fftfreq[mask1]:
#     if elem !=0 :
#         elementi_diversi_da_zero.append(elem)
#     print('le frequenze diverse da zero sono: ',elementi_diversi_da_zero)

# elementi_diversi_da_zero2=[]
# for elem in datafft[mask1]:
#     if elem !=0 :
#         elementi_diversi_da_zero2.append(elem)
#     print('le frequenze diverse da zero sono: ',elementi_diversi_da_zero2)


##  primi due picchi principali, ma solo il termine "centrale"


mask2 = np.logical_or(potenze == picco_princ, potenze == valori[2])

#print('maschera frequenze: ',fftfreq[mask2], 'maschera potenze: ',datafft[mask2])

freq_mask2 = fftfreq*mask2

data_mask2 = datafft*mask2

antitrasf2=fft.irfft(data_mask2)

plt.title('Antitrasformata con primi due picchi principali')
plt.xlabel('Time')
plt.plot(time,antitrasf2)
plt.show()


##  primi picchi principali, ma solo il termine "centrale"

mask3 = np.any([potenze == picco for picco in picchi[:3]], axis = 0)

#print('maschera frequenze: ',fftfreq[mask3], 'maschera potenze: ',datafft[mask3])

freq_mask3 = fftfreq*mask3

data_mask3 = datafft*mask3

antitrasf3=fft.irfft(data_mask3)

plt.title('Antitrasformata con primi picchi principali ma solo il termine centrale')
plt.xlabel('Time')
plt.plot(time,antitrasf3)
plt.show()


## i picchi principali con anche 1 o 2 termini, per lato, oltre quello centrale

mask4 = np.any([potenze == picco for picco in picchi], axis = 0)
#print('maschera frequenze: ',fftfreq[mask4], 'maschera potenze: ',datafft[mask4])

freq_mask4 = fftfreq*mask4

data_mask4 = datafft*mask4

antitrasf4=fft.irfft(data_mask4)

plt.title('Antitrasformata con picchi principali e il valore più vicino per ogni lato di ognuno')
plt.xlabel('Time')
plt.plot(time,antitrasf4)
plt.show()


# UTILLIZZARE SENI E COSENI

def trova_indici(n):
    for j in range(0,len(potenze)):
        if (potenze[j] == n):
            return j

def trova_antitrasformata(picchi,freq):
    somma=0
    indici=[]
    for i in range(0,len(freq_)):
        for j in range(0,len(potenze)):
            if (potenze[j] == picchi[i]):
                indici.append(j)
        somma=somma + ((r[indici[i]]*np.cos(2*np.pi*freq[i]*time))-(coeff_imm[indici[i]]*np.sin(2*np.pi*freq[i]*time)))
    return somma

# picco principale

antitrasformata_picco_princ=((r[189]*np.cos(2*np.pi*freq_[0]*time))-(coeff_imm[189]*np.sin(2*np.pi*freq_[0]*time)))*2/len(time)

plt.title('Antitrasformata con picco principale sin cos')
plt.xlabel('Time')
plt.plot(time,antitrasformata_picco_princ)
plt.show()

#primi due picchi

antitrasformata_picco2=((r[189]*np.cos(2*np.pi*freq_[0]*time))-(coeff_imm[189]*np.sin(2*np.pi*freq_[0]*time)))+((r[1509]*np.cos(2*np.pi*freq_[1]*time))-(coeff_imm[1509]*np.sin(2*np.pi*freq_[1]*time)))

plt.title('Antitrasformata con i primi due picchi principali sin cos')
plt.xlabel('Time')
plt.plot(time,antitrasformata_picco2*2/len(time))
plt.show()

#  primi picchi principali, ma solo il termine "centrale"

antitrasformata_picco3=((r[189]*np.cos(2*np.pi*freq_[0]*time))-(coeff_imm[189]*np.sin(2*np.pi*freq_[0]*time)))+((r[1509]*np.cos(2*np.pi*freq_[1]*time))-(coeff_imm[1509]*np.sin(2*np.pi*freq_[1]*time)))+((r[3395]*np.cos(2*np.pi*freq_[2]*time))-(coeff_imm[3395]*np.sin(2*np.pi*freq_[2]*time)))

plt.title('Antitrasformata con i primi picchi principali sin cos')
plt.xlabel('Time')
plt.plot(time,antitrasformata_picco3*2/len(time))
plt.show()

# i picchi principali con anche 1 o 2 termini, per lato, oltre quello centrale
antitrasformata_picco4=trova_antitrasformata(picchi,freq_)

plt.title('Antitrasformata con picchi principali e 1 dato per lato per ciascuno sin cos')
plt.xlabel('Time')
plt.plot(time,antitrasformata_picco4*2/len(time))
plt.show()

sf.write('./diapason_recreated2.wav', antitrasformata_picco4, samplerate)
sf.write('./diapason_recreated3.wav', antitrasf4, samplerate)


def trova_picchi_potenza(frequenze, potenze, intervallo_frequenza):
    picchi = []
    
    for i in range(len(potenze)):
        frequenza = frequenze[i]
        potenza = potenze[i]
        
        # intervallo di frequenza intorno al punto corrente
        indice_inizio = max(0, i - intervallo_frequenza)
        indice_fine = min(len(potenze), i + intervallo_frequenza + 1)
        
        # Trova il massimo locale all'interno dell'intervallo
        if potenza == max(potenze[indice_inizio:indice_fine]):
            picchi.append((frequenza, potenza))
    
    return picchi

picchi_con_intervallo = trova_picchi_potenza(fftfreq[:len(datafft)], potenze, 1000)
print("Picchi di potenza con intervallo {}: {}".format(fftfreq[:len(datafft)], picchi_con_intervallo))

