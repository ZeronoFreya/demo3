from time import sleep

class ServiceEvent(object):
    '''服务进程'''
    def __init__(self, _GuiQueue):
        self.GuiQueue = _GuiQueue

    def clickCallBack(self, msg):
        sleep(3)
        self.__putGui( 'clickCallBack', msg )

    def __putGui(self, f, m = None ):
        self.GuiQueue.put({
            'fun' : f,
            'msg' : m
        })

class GuiCallBack(object):
    def __init__(self, funCall):
        self.funCall = funCall

    def clickCallBack(self, msg):
        return self.funCall('clickCallBack', msg )