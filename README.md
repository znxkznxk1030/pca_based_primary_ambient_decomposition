# pca_based_primary_ambient_decomposition
주 요소, 주변 요소 분리

reference - http://smcnetwork.org/system/files/SMC2016_submission_36.pdf

## main algorithm

![alt text](https://scontent-hkg3-1.xx.fbcdn.net/v/t1.0-9/19642333_1584742551555972_2460613194975633821_n.jpg?oh=afd9f8a9b684c690d4a66f1d930f246f&oe=59DA5B4B)

```python

 for i in range(frame):
        subSignal = source[i * N: (i + 1) * N, :]

        print("%d %s %d" % (i, '/', frame))

        XVL = fftpack.rfft(subSignal[:, 0])
        XVR = fftpack.rfft(subSignal[:, 1])

        for k in range(N):
            subIn = vstack((XVL[k], XVR[k]))
            currP = dot(subIn.transpose(), subIn)

            psd[:, :, k] = psd[:, :, k] * lamb + (1 + lamb) * currP
            Cpsd = psd[:, :, k]

            # compute eigenvalue & eigenvector

            eigVal, eigVec = np.linalg.eig(Cpsd)
            pan = eigVec[:, 1]

            Sest[k] = pan[0] * XVL[k] + pan[1] * XVR[k]

            Nlest[k] = XVL[k] - Sest[k] * pan[0]
            Nrest[k] = XVR[k] - Sest[k] * pan[1]

        xout = fftpack.irfft(Sest)
        xl = fftpack.irfft(Nlest)
        xr = fftpack.irfft(Nrest)
        OutVec = append(OutVec, xout)
        OutAmbL = append(OutAmbL, xl)
        OutAmbR = append(OutAmbR, xr)

    print('process end : copy start')
    ext_primary = OutVec
    ext_ambient = transpose(vstack((OutAmbL, OutAmbR)))

    ret_primary = wave.open(primary_path, 'w')
    ret_primary.setparams((1, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))
```



















## Practice fft and select frequency
- origin frequency

![alt text](https://scontent-hkg3-1.xx.fbcdn.net/v/t31.0-8/19693700_1584735708223323_4169270473697054645_o.jpg?oh=51bff0e83738e520bdc69683145fb6a6&oe=59D8F0FC)

- cut-off high frequency
![alt text](https://scontent-hkg3-1.xx.fbcdn.net/v/t31.0-8/19702810_1584735704889990_2629168977502692219_o.jpg?oh=a7b201367e3fc5d0fd14014af935e8a3&oe=59D1FEC8)

- cut-off low frequency
![alt text](https://scontent-hkg3-1.xx.fbcdn.net/v/t31.0-8/19577323_1584735711556656_7554138837472030077_o.jpg?oh=04e4dce15cd2f48b7d72196c3960d439&oe=5A0A3A85)


