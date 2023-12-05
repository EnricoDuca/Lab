import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, constants
from scipy.fft import ifft, rfft
    
data, samplerate = sf.read('./distorta.wav')

#print(samplerate)
#print(data)
#print(len(data))

#print(type(samplerate))
#print(type(data))

#sf.write('./distorta_recreated.wav', data, samplerate)

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

def func(a,b):
    dic={}
    for elem1,elem2 in zip(a,b):
        dic[elem1]=elem2
    return dic[222884.8301838864]

print(func((abs(datafft[:len(datafft)])**2),fftfreq[:len(datafft)]))

'''
Il primo picco è (110.24999999999999,9954056.90923407) --> nota: La2
Il secondo picco è (880.2499999999999, 1464080.3327664384) --> nota: La5
Il terzo picco è (1980.4166666666665,222884.8301838864) --> nota: Si6
'''
