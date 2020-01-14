# -*- coding: utf-8 -*-

from queue import Queue, Empty
from threading import Thread


class EventManager:
    """
    This is an event manager .
    """

    def __init__(self):
        self.__eventQueue = Queue()
        self.__active = False
        self.__thread = Thread(target=self.__run)
        # eg .
        #  self.__handlers = {
        #      'type1':[methods1,methods2],
        #      'type2': [methods3, methods4],
        #  }
        self.__handlers = {}

    def __run(self):
        """
        Start engine .
        """

        while self.__active:
            try:
                event = self.__eventQueue.get(block=True, timeout=1)
                self.__event_process(event)
            except Empty:
                pass

    def __event_process(self, event):
        """
        Handling events .
        """
        # Check if there is a handler for this event
        if event.type_ in self.__handlers:
            # If present, the events are passed to the handler in order
            for handler in self.__handlers[event.type_]:
                handler(event)

    def start(self):
        """
        Start event manager .
        """
        self.__active = True
        self.__thread.daemon = False
        self.__thread.start()

    def stop(self):
        """
        Stop event manager .
        """
        self.__active = False
        self.__thread.join()

    def add_event_handler(self, type_, handler):
        """
        Binding events and listener handlers .

        :param type_: a name of handler
        :param handler: function
        """
        # Attempt to get a list of handler functions corresponding
        # to an event type, create it if none .
        try:
            handler_list = self.__handlers[type_]
        except KeyError:
            handler_list = []
            self.__handlers[type_] = handler_list

        # To register a handler that is not in the handler list for
        # the event, register the event .
        if handler not in handler_list:
            handler_list.append(handler)

    def remove_event_handler(self, type_, handler):
        """
        Remove handler .
        """
        try:
            handler_list = self.__handlers[type_]
            if handler in handler_list:
                handler_list.remove(handler)
            if not handler_list:
                del self.__handlers[type_]
        except KeyError:
            pass

    def send_event(self, event):
        """
        Send events and store events in the event queue .
        """
        self.__eventQueue.put(event)
