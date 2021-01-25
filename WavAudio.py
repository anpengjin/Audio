#!/usr/bin/env python3
import wave

import numpy as np
from Audio import Audio

'''
wav 音频文件
nframe 样本数量
framerate 采样频率
nchannel 声道数量
sampwidth 一次采样的字节数
文件长度 = 头部长度 + 数据长度
数据长度 = nframe * nchannel *sampwidth
时间长度 = nframe / framerate
'''


class WavAudio(Audio):
    def __init__(self, src=""):
        super().__init__()
        self.src = src
        self.wave_read = None

    def ensureLoaded(self):
        if self.wave_read is not None:
            return
        self.wave_read = wave.open(self.src, "rb")

    def toJson(self):
        obj = super().toJson()
        obj["src"] = self.src
        return obj

    def __repr__(self):
        return f"{self.tag()}, src={self.src}, len={len(self)}, channels={self.getChannelNum()}, samplewidth={self.getSampleWidth()}"
    
    def fromJson(self, obj):
        super().fromJson(obj)
        self.src = obj["src"]

    def __len__(self):
        self.ensureLoaded()
        return self.wave_read.getnframes()

    def getChannelNum(self):
        self.ensureLoaded()
        return self.wave_read.getnchannels()

    def getSampleWidth(self):
        self.ensureLoaded()
        return self.wave_read.getsampwidth()

    def getFrameRate(self):
        self.ensureLoaded()
        return self.wave_read.getframerate()

    def getFrameBytes(self, start, n=1):
        self.ensureLoaded()
        if start < 0:
            raise Exception(f"start less than 0:{start}")
        if start + n > len(self):
            raise Exception(f"start greater than len:{start} + {n} > {len(self)}")
        self.wave_read.setpos(start) # 设置文件指针到指定位置。
        return self.wave_read.readframes(n)

def test():
    src = '/source/d3/ContentGeneration/audio/test_lrlr.wav'
    dst = '/source/d3/ContentGeneration/audio/拜登VS川普-1.wav'
    audio = WavAudio(src)
    print(audio)
    bs = audio.getBytes()
    print("bs", len(bs))  # 总字节数len(bs) =  数据长度(len(self)) * 通道数(channel) * 每帧字节数(samplewidth) 即：131008 = 32752 * 2 * 2

if __name__=='__main__':
    import fire
    fire.Fire()