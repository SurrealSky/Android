import frida
import sys
rdev = frida.get_remote_device()
session = rdev.attach("com.tencent.mm")
print session
jscode = """
Java.perform(function () {
    var jni = Java.use("com.tencent.mm.plugin.collect.ui.CollectMainUI$10");
    jni.cl.implementation =function () {
        send("cache:"+arguments[0]);
        send("cache:"+arguments[1]);
        result=this.cl.apply(this,arguments)
        return result
    };
});

Java.perform(function () {
    var jni = Java.use("com.tencent.mm.plugin.collect.ui.CollectMainUI");

            var threadef = Java.use('java.lang.Thread');
            var threadinstance = threadef.$new();
            function Where(stack)
            {
                for(var i = 0; i < stack.length; ++i)
                {
                    send(stack[i].toString());
                }
            }
    jni.yF.implementation =function () {
        send("yF:"+arguments[0]);
        result=this.yF.apply(this,arguments)
        var stack = threadinstance.currentThread().getStackTrace();
        send("Full call stack:" + Where(stack));
        return result
    };
});
"""
script = session.create_script(jscode)
def on_message(message ,data):
    if message['type'] == 'send':
        print(message['payload'])
    elif message['type'] == 'error':
        print(message['stack'])
script.on("message" , on_message)
script.load()
sys.stdin.read()
