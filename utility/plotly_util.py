import plotly.plotly as py
import matplotlib.pyplot as plt
import numpy as np

ID = 'znxkznxk'
API_KEY = 'sjNJs2P1jDDzlz52fumC'


def signIn(id, api_key):
    py.sign_in(id, api_key)


def showSignalFFT(signal: np.array, frq: np.array, fft_signal: np.array):
    signIn(ID, API_KEY)
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(signal)
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')

    ax[1].plot(frq, abs(fft_signal))
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('y')

    plot_url = py.plot_mpl(fig, filename='mpl-basic-fft-basic-fft')
