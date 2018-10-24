import xmltodict
def parse(d):
    d=xmltodict.parse(d)
    def pppf(x):
        q={}
        for a in x:
            q[a["@id"]]=a["@value"]
        return q
    def plne(x):
        return {"from":{"block":x["@fromBlock"],"pin":x["@fromPin"]},"to":{"block":x["@toBlock"],"pin":x["@toPin"]}}
    def pprm(b,x):
        if b=="UIBlockText":
            return {"text":x["0"]}
        elif b=="UIBlockWait":
            return {"timeSec":x["0"]}
        elif b=="UIBlockBranchButton" or b=="UIBlockBranchLightBarrier":
            return {"input":"I"+str(int(x["0"])+1)}
        elif b=="UIBlockAwaitButton":
            return {"input":"I"+str(int(x["0"])+1),"waitFor":("press" if x["1"]=="0" else "stopPress")}
        elif b=="UIBlockAwaitLightBarrier":
            return {"input":"I"+str(int(x["0"])+1),"waitFor":("normal" if x["1"]=="0" else "special")}
        elif b=="UIBlockOutLamp":
            return {"output":"M"+str(int(x["0"])+1)}
        elif b=="UIBlockOutMotor":
            return {"output":"M"+str(int(x["0"])+1),"speed":x["1"]}
        else:
            return x
    def pblk(b,l):
        p=None
        p2=None
        for x in l:
            if x["@fromBlock"]==b["@id"] and x["@fromPin"]=="0" and b["@class"]=="UIBlockStart":
                p={"block":x["@toBlock"],"pin":x["@toPin"]}
            elif x["@fromBlock"]==b["@id"] and x["@fromPin"]=="1":
                p={"block":x["@toBlock"],"pin":x["@toPin"]}
            elif x["@fromBlock"]==b["@id"] and x["@fromPin"]=="2":
                p2={"block":x["@toBlock"],"pin":x["@toPin"]}
        return {"type":b["@class"],"id":b["@id"],"param":((pprm(b["@class"],pppf((b["parameter"] if str(type(b["parameter"]))=="<class 'list'>" else [b["parameter"]])))) if "parameter" in b else {}),"pin_ok":p,"pin_no":p2}
    o={"blocks":[pblk(b,d["root"]["edges"]["edge"]) for b in d["root"]["blocks"]["block"]]}
    return o
def run(a,o):
    def runblk(a,b,t,o):
        pin=(b["pin_ok"] if a.on(b["type"],t,b["param"])==0 else b["pin_no"])
        if pin:
            for b in o["blocks"]:
                if b["id"]==pin["block"]:
                    runblk(a,b,pin["pin"],o)
        elif b["type"]!="UIBlockStop":
            a.error("PIN_UNSET")
    for b in o["blocks"]:
        if b["type"] == "UIBlockStart":
            runblk(a,b,-1,o)
