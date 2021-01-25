#!/usr/bin/env python3
'''
所有 Audio 的基类
'''

import time
import json
import wave

class Audio:
    def __init__(self):
        pass

    def __len__(self):
        """帧的数量"""
        return 0

    def getNorminalLength(self):
        """名义上的长度"""
        return len(self)

    def getActualOffset(self, offset):
        """实际长度"""
        return int(offset * len(self) / self.getNorminalLength())

    def getNominalOffset(self, offset):
        return int(offset * self.getNorminalLength() / len(self))

    def getChannelNum(self):
        """声道数量"""
        return 1

    def getSampleWidth(self):
        """1:8bit，2:16bit"""
        return 1

    def getFrameWidth(self):
        """一帧占的字节数"""
        return self.getChannelNum() * self.getSampleWidth()

    def getFrameRate(self):
        """采样率，一秒多少帧"""
        return 1

    def getBytes(self):
        """所有字节"""
        return self.getFrameBytes(0, len(self))

    def getFrameBytes(self, start, n=1):
        return bytes()

    def toJson(self):
        return {
            "tag": self.tag()
        }

    def fromJson(self):
        '''
        需要保证除了基本参数初始化之外
        一些优化性质的成员也要与 __init__ 一致
        '''        

    def getDuration(self):
        """返回音频时长"""
        return len(self) / self.getFrameRate()

    def getNorminalDuration(self):
        """返回名义上的时长"""
        return self.getNorminalLength() / self.getFrameRate()

    def tag(self):
        return self.__class__.__name__

    def __add__(self, other):
        from ContentGeneration.Audio.ConcatenateAudio import ConcatenateAudio
        return ConcatenateAudio([self, other])

    def __getitem__(self, item):
        if isinstance(item, slice):
            from ContentGeneration.Audio.SliceAudio import SliceAudio
            assert item.step is None or item.step == 1
            if item.start == 0 and item.stop == len(self):
                return self
            return SliceAudio(self, item.start, item.stop)
        else:
            raise Exception(f"{self} getitem failed:{item}")

    def print(self):
        print('len:', len(self))
        print('nominal len:', self.getNorminalLength())
        print('frame rate:', self.getFrameRate())
        print('channel num:', self.getChannelNum())
        print('sample width:', self.getSampleWidth())
        print('frame width:', self.getFrameWidth())
        print('bytes len:', len(self.getBytes()))
        print('audio self:', self)
        print('audio json: ')
        print('json:')
        print(json.dumps(self.toJson(), indent=2, ensure_ascii=False)) 
    
    def save(self, dst):
        wave_write = wave.open(dst, "wb")
        wave_write.setnchannels(self.getChannleNum())
        wave_write.setsampwidth(self.getSampleWidth())
        wave_write.setframerate(self.getFrameRate())
        wave_write.setnframes(len(self))
        wave_write.writeframes(self.getBytes())
        wave_write.close()

def test():
    a = Audio()
    a.print()

if __name__ == "__main__":
    import fire
    fire.Fire()    