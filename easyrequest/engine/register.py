from easyrequest.middlewares import MixFuncGeneratorMiddleWare
from .event_manage import EventManager
from .spider_runner import SpiderRunner


class Event:
    EVENT_REQUEST = "EVENT_REQUEST"
    EVENT_PARSE = "EVENT_PARSE"

    def __init__(self, type_=None):
        self.type_ = type_
        self.event = None


class Listener(SpiderRunner):
    def __init__(self, pool, spider_cls, data_cls, mid_cls_list, task_sender):
        super(Listener, self).__init__(pool, spider_cls, data_cls, mid_cls_list, task_sender)

    def put_request_to_pool(self, request_instance):

        # 任务实际上在另一个线程进行的,此处会造成任务丢失
        tmp = self.pool.spawn(self._request, request_instance)
        self.pool.start(tmp)

    def deal_request_event(self, event):
        request_instance = event.event
        print('收到request事件,并放入池中', request_instance.url)
        self.put_request_to_pool(request_instance)

    def deal_parse_event(self, event):
        resp = event.event
        if resp.callback is None or resp.callback.__name__ == 'parse_response':
            print('收到parser事件,即将解析')
            self._parse_resp_and_save_by_generator(resp)

        else:
            print('即将执行callback', resp.callback.__name__)
            callback_iter = MixFuncGeneratorMiddleWare(resp.callback)(resp)
            for request_instance in callback_iter:
                print('callback事件放入池中', request_instance.url)
                self.put_request_to_pool(request_instance)


class SendTasks:
    def __init__(self, event_manager):
        """ Init a event manager ."""
        self.__eventManager = event_manager

    def send_request(self, request_instance):
        """
        Send a instance of Request .
        """
        event = Event(type_=Event.EVENT_REQUEST)
        event.event = request_instance

        self.__eventManager.send_event(event)
        print('发送request', event.event.url)

    def send_parse(self, resp):
        event = Event(type_=Event.EVENT_PARSE)
        event.event = resp
        print('发送parse', event.event)
        self.__eventManager.send_event(event)


class Register:
    """
    API for manager , Sender ...
    """

    @staticmethod
    def register_manager():
        # register event manager
        event_manager = EventManager()
        return event_manager

    @staticmethod
    def bind_handler(manager, type_, handler):
        manager.add_event_handler(type_, handler)

    @staticmethod
    def task_sender(manager):
        sender = SendTasks(manager)
        return sender
