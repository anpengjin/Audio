#!/usr/bin/env python3
import os
import sys
import wave
import librosa

from Audio import Audio

"""
纯数据，没有 wav 头
nframe 样本数量(帧的个数)
framerate 采样频率(如16000、44100)
nchannel 声道数量(如1、2)
sampwidth 一次采样的字节数:16bit=2个字节，即1帧占用2个字节
文件长度 = 头部长度 + 数据长度
数据长度 = nframe * nchannel *sampwidth
时间长度 = nframe / framerate
"""

class PCMAudio(Audio):
    def __init__(self, src="", framerate=16000, nchannel=2, sampwidth=1):
        super().__init__()
        self.src = src
        self.framerate = framerate
        self.nchannel = nchannel
        self.sampwidth = sampwidth
        self.fp = None

    def ensureLoaded(self):
        if self.fp is not None:
            return
        self.fp = open(self.src, "rb")


    def __len__(self):
        self.ensureLoaded()
        self.fp.seek(0, 2) # 2表示从文件末尾算起
        bytes_num = self.fp.tell()
        frame_width = self.nchannel * self.sampwidth
        return int(bytes_num/frame_width)

    def getChannelNum(self):
        return self.nchannel

    def getSampleWidth(self):
        return self.sampwidth
    
    def getFrameRate(self):
        return self.framerate

    def getFrameBytes(self, start, n=1):
        self.ensureLoaded()
        pos = start * self.getFrameWidth() # getFrameWidth:一帧占的字节数
        size = n * self.getFrameWidth()
        self.fp.seek(pos, 0)
        content = self.fp.read(size)
        return content

    def toJson(self):
        obj = super().toJson()
        obj["src"] = self.src
        obj["framerate"] = self.framerate
        obj["nchannel"] = self.nchannel
        obj["sampwidth"] = self.sampwidth
        return obj

    def fromJson(self, obj):
        super().fromJson(obj)
        self.src = obj["src"]
        self.framerate = obj["framerate"]
        self.nchannel = obj["nchannel"]
        self.sampwidth = obj["sampwidth"]

    def __repr__(self):
        return f"({self.tag()},src={self.src}, len={len(self)}, frame_rate={self.getFrameRate()})"


def test():
    src = '/source/d3/ContentGeneration/test/test_lrlr.pcm'
    audio = PCMAudio(src=src, nchannel=2, sampwidth=2, framerate=16000)
    audio.print()
    print(audio)
    exit(0)
    o = audio.toJson()
    audio2 = PCMAudio()
    audio2.fromJson(o)
    print(audio2)
    audio2.save('/source/d3/ContentGeneration/audio/test_lrlr.wav')
        

if __name__ == "__main__":
    import fire
    fire.Fire()