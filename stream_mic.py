NAO_IP = "192.168.0.109" # Romeo on table
#~ NAO_IP = "10.0.253.99" # Nao Alex Blue


from optparse import OptionParser
import naoqi
import numpy as np
import time
import sys
import pyaudio


class SoundReceiverModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp ):
        try:
            naoqi.ALModule.__init__(self, strModuleName );
            self.BIND_PYTHON( self.getName(),"callback" );
            self.strNaoIp = strNaoIp;
            self.outfile = None;
            self.aOutfile = [None]*(4-1); # ASSUME max nbr channels = 4
        except BaseException as err:
            print( "ERR: abcdk.naoqitools.SoundReceiverModule: loading error: %s" % str(err) );

    # __init__ - end
    def __del__( self ):
        print( "INF: abcdk.SoundReceiverModule.__del__: cleaning everything" );
        self.stop();

    def start(self):
        audio = naoqi.ALProxy("ALAudioDevice", self.strNaoIp, 9559)
        nNbrChannelFlag = 3  # ALL_Channels: 0,  AL::LEFTCHANNEL: 1, AL::RIGHTCHANNEL: 2; AL::FRONTCHANNEL: 3  or AL::REARCHANNEL: 4.
        nDeinterleave = 0
        nSampleRate = 16000
        audio.setClientPreferences(self.getName(), nSampleRate, nNbrChannelFlag,
                                   nDeinterleave)  # setting same as default generate a bug !?!
        audio.subscribe(self.getName())
        print("INF: SoundReceiver: started!")

    def processRemote(self, nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, buffer_audio):
        """
        This is THE method that receives all the sound buffers from the "ALAudioDevice" module
        https://stackoverflow.com/questions/24243757/nao-robot-remote-audio-problems
        """
        aSoundDataInterlaced = np.fromstring(str(buffer_audio), dtype=np.int16)

        aSoundData = np.reshape(aSoundDataInterlaced, (nbOfChannels, nbrOfSamplesByChannel), 'F')
        # print "input data:", aSoundDataInterlaced
        # print "Processed data:", aSoundData

        if (True):
            # compute peak
            aPeakValue = np.max(aSoundData)
            if (aPeakValue > 16000):
                print("Peak: %s" % aPeakValue)

            p = pyaudio.PyAudio()

            def callback(in_data, frame_count, time_info, status):
                return (buffer_audio, pyaudio.paContinue)
                # return (aSoundDataInterlaced, pyaudio.paContinue)
            print(nbOfChannels)
            print(nbrOfSamplesByChannel)
            print(aTimeStamp)

            stream = p.open(format=p.get_format_from_width(1),
                            channels=nbOfChannels,
                            rate=nbrOfSamplesByChannel,
                            output=True,
                            stream_callback=callback)
            # stream.write(aSoundData[0])
            stream.start_stream()

