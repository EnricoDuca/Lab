import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, constants
from scipy.fft import ifft, rfft
    
def func(a,b,valore):
    dic={}
    for elem1,elem2 in zip(a,b):
        dic[elem1]=elem2
    return dic[valore]

data, samplerate = sf.read('./pulita_difficile.wav')

#print(samplerate)
#print(data)
#print(len(data))

#print(type(samplerate))
#print(type(data))

#sf.write('./pulita_difficile_recreated.wav', data, samplerate)

time = np.linspace(0, len(data)/samplerate, len(data))

plt.plot(time,data[:,0])
plt.show()

datafft = fft.fft(data[:,0])

fftfreq =abs(fft.fftfreq(len(data[:,0]),1/samplerate))

#print(datafft)
#print(len(datafft))
#print(fftfreq)
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

r=fft.rfft(data[:,0])
i=fft.ifft(data[:,0])


plt.plot(fftfreq[:len(r)], r)
plt.show()

plt.plot(fftfreq[:len(i)], i)
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

valori = valori_piu_grandi(abs(datafft[:len(datafft)])**2,12)

print("I valori più grandi sono :", valori)
for i in valori:
    print('Le frequenza corrispondente è: ', func(abs(datafft[:len(datafft)])**2, fftfreq[:len(datafft)], i))
    

#larghezza a mezza altezza
max2=1464080.33276644
max2_mezzo=max2/2
print(max2_mezzo)
