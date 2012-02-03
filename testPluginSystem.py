#!/usr/bin/env python
import unittest
from pluginsystem import *

class PluginSystemTest(unittest.TestCase):

    def testBasePluginSystem(self):
        assert isinstance(basePluginSystem, PluginSystem)

    def testInstallPlugin(self):
        basePluginSystem.installPlugin(BasePlugin)

    def testGlobalHooks(self):
        function=lambda x:x+1
        plugin=basePluginSystem.installPlugin(BasePlugin)
        plugin.registerGlobalHook("globalhook", function)
        fnc=basePluginSystem.getGlobalHook("globalhook")
        self.assertEqual(function,fnc,"Plugin not installed")

    def testEvents(self):
        event=Event("name",arg=1,arg2=2)
        basePluginSystem.emit(event)
        self.assertEqual(len(basePluginSystem.eventqueue),1)
        basePluginSystem.emit_event("name",arg1=1)
        self.assertEqual(len(basePluginSystem.eventqueue),2)
        basePluginSystem.run()
        self.assertEqual(len(basePluginSystem.eventqueue),0)

    def testLogger(self):
        logger=basePluginSystem.getLogger("main")
        logger.warning("Test warning")

    def testListenersBasic(self):
        def testhandler():
            pass
        #Create listener
        listener=Listener(BasePlugin())
        #Creat temporary handler for test
        listener.handler_testevent=testhandler
        #Register event
        basePluginSystem.registerEvent("testevent", listener, PRIORITY_NORMAL)
        #Handle event (this will be called by PluginSystem after run() )
        listener._handleEvent(Event("testevent1"))

    def testEventsPriority(self):
        def testhandler():
            pass
        #Create listener
        listener=Listener(BasePlugin())
        #Creat temporary handler for test
        listener.handler_testevent=testhandler
        #Register event
        basePluginSystem.registerEvent("testevent", listener, PRIORITY_HIGH)
        event=Event("testevent")
        listener.applyPriority(event)
        self.assertEqual(event.priority, PRIORITY_HIGH)
        #Check after emit
        event=Event("testevent")
        basePluginSystem.emit(event)
        basePluginSystem.run()
        self.assertEqual(event.priority, PRIORITY_HIGH,"Priority not match after emit")

    def testListenerEvents(self):
        listener=Listener(BasePlugin())
        basePluginSystem.registerEvent("testevent", listener, PRIORITY_NORMAL)
        assert isinstance(listener.isEventSupported("testevent"), bool),"isEventSupported must return boolean value"
        assert isinstance(listener.getEventPriority("testevent"), int),"getEventPriority must return integer value"
        self.assertEqual(listener.getEventPriority("unknownevent"), None, "getEventPriority must return None value for not supported event")

if __name__=="__main__":
    unittest.main()
