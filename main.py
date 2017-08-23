# 导入sciter支持,必须安装pysciter
import sciter
import ctypes
import json

from multiprocessing import Process,Queue
from threading import Thread
from EventManager import EventManager
from FunManager import ServiceEvent, GuiCallBack

# 设置dpi, 防止程序在高分屏下发虚
ctypes.windll.user32.SetProcessDPIAware(2)

def startServiceP(_GuiQueue, _ServiceQueue):
    '''开启一个服务进程'''
    funMap = ServiceEvent( _GuiQueue )
    EventManager( _ServiceQueue, funMap ).Start()

def queueLoop( _GuiQueue, funCall ):
    guiCallBack = GuiCallBack( funCall )
    EventManager( _GuiQueue, guiCallBack ).Start()

class Frame(sciter.Window):
    def __init__(self):
        '''
            ismain=False, ispopup=False, ischild=False, resizeable=True,
            parent=None, uni_theme=False, debug=True,
            pos=None,  pos=(x, y)
            size=None
        '''
        super().__init__(ismain=True, debug=True)
        self.set_dispatch_options(enable=True, require_attribute=False)

    def _document_ready(self, target):
        '''在文档加载后执行，如果设置启动画面，可以在这里结束'''

        # 创建用于接收服务进程传递的回馈任务的队列，此队列线程安全
        self.GuiQueue = Queue()
        # 创建用于接收界面进程发送的任务的队列，此队列线程安全
        self.ServiceQueue = Queue()
        p = Process(target = startServiceP, args = ( self.GuiQueue, self.ServiceQueue ))
        p.daemon = True #设置为守护进程,保证主进程退出时子进程也会退出
        p.start()
        t = Thread(target = queueLoop, args=( self.GuiQueue, self.call_function ))
        t.daemon = True
        t.start()

    def clickMe(self):
        # 点击页面上的按钮后，只将任务添加到服务队列，耗时很短，因此不会发生界面卡顿现象
        self.__putService('clickCallBack','你已经点到我了!')

    def __putService(self, f, m = None):
        '''接收界面事件并转发'''
        self.ServiceQueue.put({
            'fun' : f,
            'msg' : m
        })

if __name__ == '__main__':
    frame = Frame()
    frame.load_file("Gui/main.html")
    frame.run_app()
