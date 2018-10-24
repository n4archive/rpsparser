import rpsparser,json
o=None
with open("/sdcard/Documents/RoboProSmart/v.xml") as x:
    o=rpsparser.parse(x.read())
print(json.dumps(o))
class Test:
    def on(self,t,pin,p):
        print(t)
        print(pin)
        print(json.dumps(p))
        return 0 if t != "UIBlockBranchButton" and t != "UIBlockBranchLightBarrier" else (1 if input("True?")=="y" else 0) 
    def error(self,e):
        print(e)
rpsparser.run(Test(),o)
