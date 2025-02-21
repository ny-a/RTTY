# Pythonによるラジオテレタイプの復調プログラム
This is a Python program to demodulate the radio teletype known as FSK modulation.
This is the simplest example, and only the Terminal Unit part of the RTTY is implemented. The rest should be coded according to ITA2, for example.

## サンプル音声ファイル
This ogg file should be converted to wave format.
https://en.wikipedia.org/wiki/File:RTTY.ogg
it is from wikipedia

### ogg ファイルを wave に変換する

Install [ffmpeg](https://www.ffmpeg.org/) and run:

~~~
ffmpeg -i RTTY.ogg -ar 8k -c:a pcm_u8 -f wav rtty3s.wav
~~~
      
## パラメーター
Some parameters in the source code need to be modified according to the audio file to be input. 
~~~
fname='rtty3s.wav' # should be specify the filename.
smp= 8000          # Sampling Rate
FQm= smp/914.0     # Mark Frequency 914Hz
FQs= smp/1086.0    # Space Frequency 1086Hz
~~~
- fname   
should be specify the filename.
- smp   
Sampling Rate.
- FQm     
smp / Mark Frequency. 
- FQs   
smp / Space Frequency. 

## マークとスペースの周波数の設定方法
To find MARK & SPACE frequences, You can use any spectrum analyze tools on your PC. For example I use Sazanami Version 1.7.3 2020/10/22
. 

- MARK Frequency about 915Hz    
![](img/space.png)
- SPACE Frequency is about 1085Hz   
![](img/mark.png)


## 使い方
Please specify an appropriate audio file for the input.
This program assumes 8KHz sampling, mono, 8bit quantization, and no sign.
~~~
python -m src.main
~~~
Demodulation example
![](img/2021-02-01.png)
