import a2s
import time

timeout = 100

iplist = "ips.txt"
addQue = "/var/www/html/addServer.txt"
servData = "/var/www/html/serverData.txt"

def getData():
    print("Updating database")
    data = ""

    with open(iplist, "r") as file:
        lines = file.readlines()
    
    goodServers = []
    for line in lines:
        line = line.strip()
        if ":" in line:  
            ip, port = line.split(":")  
            address = (ip, int(port)) 
            print(f"GettingInfo: {address}")
            try:
                info = a2s.info(address)
            except:
                info = ""
                print("ERROR when trying to get info from server.")
            if info != "":
                print("data retrived sucessfully!")
                info.ip = ip
                info.port = port
                goodServers.append(info)

    infoServList = sortServers(goodServers)
    for info in infoServList:
        data = data + "\"" + info.server_name + "\"" +  info.map_name + "\"" +  str(info.player_count) + "\"" +  str(info.max_players) + "\"" +  str(info.ping) + "\""+str(info.ip)+":"+str(info.port)+"\n"
    print(data)
    sdtxt = open(servData, "w")
    sdtxt.write(data)
    sdtxt.close()

def updateIps():
    print("Adding new IPs")
    with open(addQue, "r+") as cache:
        cacheIps = cache.readlines()
        if len(cacheIps) > 10:
            return 
    cache.close()

    verifiedIps = []

    for tip in cacheIps:
        tip = tip.strip()
        if ":" in tip:
            ip, port = tip.split(":")
            print("Adding: "+str(ip)+":"+str(port))
            taddress = (ip,int(port))
            try:
                tinfo = a2s.info(taddress)
            except:
                tinfo = ""
                print("Error: Bad/no respone from server, skipping!")
            if tinfo != "" and tinfo.game == "Counter-Strike: Global Offensive":
                with open(iplist, "r") as testFile:
                    testIps = testFile.readlines()
                isContained = False
                for address in testIps:
                    if str(address).strip() == (str(ip) + ":" + str(port)).strip():
                        isContained = True
                        break;
                if isContained == False:
                    verifiedIps.append(ip+":"+port)
                else:
                    print("IP already found in ip list, skipping!")

    if len(verifiedIps)>0:
        print("Adding IPs to the IP list")
        outputString = ""
        for verIP in verifiedIps:
            outputString = outputString + verIP + "\n"
        with open(iplist, "a") as outputFile:
            outputFile.write(outputString)
        outputFile.close()
    open(addQue, "w").close()

def sortServers(servers):
    sortedserv = sorted(servers, key=lambda s: s.player_count, reverse=True)
    return sortedserv

while(True):
    getData()
    updateIps()
    print(str(timeout)+"s untill the next update.")
    time.sleep(timeout)
    
