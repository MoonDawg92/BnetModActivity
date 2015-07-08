import asyncio
import aiohttp
 
headers = {'X-API-Key' : 'd733b6d164864cc1b5aa3ff0e306e9a8'}  
modList = []; 
 
class Mod:
    
    def __init__(self, name, role, url, active):
        self.name = name
        self.role = role
        self.url = 'http://www.bungie.net' + url
        self.active = active
        
    def getName(self):
        return self.name
        
    def getRole(self):
        return self.role
        
    def getUrl(self):
        return self.url
        
    def getActive(self):
        return self.active
 
 
@asyncio.coroutine 
def fetch_page(url, likes, posts, role):
    #url = 'https://www.bungie.net/platform/User/GetBungieNetUserById/108762/'
    global modList
    global headers
    
    response = yield from aiohttp.request('GET', url, headers=headers)
    likesTime = yield from aiohttp.request('GET', likes, headers=headers)
    postsTime = yield from aiohttp.request('GET', posts, headers=headers)
    data = yield from response.json()
    timeData1 = yield from likesTime.json()
    timeData2 = yield from postsTime.json()
    
    if response.status == 200:
        #print(data['Response']['displayName'])
        timeArr1 = timeData1['Response']['posts']
        timeArr2 = timeData2['Response']['posts']
        #for x in timeArr1:
        time1 = timeArr1[len(timeArr1)-1]['lastModified']
        time2 = timeArr2[len(timeArr2)-1]['lastModified']
        
        lastActive = time1 if (time1 > time2) else time2
        #print(time1)
        #print(time2)
        #print(time1 > time2)
        
        mod = Mod (data['Response']['displayName'], role, data['Response']['profilePicturePath'], lastActive)
        modList.append(mod)
        print(mod.getName())
        print(mod.getRole())
        print(mod.getActive())
        print()
        
    # else:
        # print("data fetch failed for: %d" % idx)
        # print(response.content, response.status)
        
    response.close()
    likesTime.close()
    postsTime.close()
    
    
    
def main():
    mentorIds = [ 108762, 4878, 224480 ];
    ninjaIds  = [ 2311, 218625, 7024 ];

    profileUrl = 'https://www.bungie.net/platform/User/GetBungieNetUserById/'
    likesUrl1 = 'https://www.bungie.net/platform/Activity/User/'
    likesUrl2 = '/Activities/LikesAndShares/?itemsperpage=1&currentpage=1'
    postsUrl1 = 'https://www.bungie.net/platform/Activity/User/'
    postsUrl2 = '/Activities/Forums/?itemsperpage=1&currentpage=1'
    
    coros = []
    for x in mentorIds:
        profile = profileUrl + str(x)
        likes = likesUrl1 + str(x) + likesUrl2
        posts = postsUrl1 + str(x) + postsUrl2
        coros.append(asyncio.Task(fetch_page(profile, likes, posts, "Mentor")))
    
    for x in ninjaIds:
        profile = profileUrl + str(x)
        likes = likesUrl1 + str(x) + likesUrl2
        posts = postsUrl1 + str(x) + postsUrl2
        coros.append(asyncio.Task(fetch_page(profile, likes, posts, "Ninja")))

    print("WAIT")
    
    yield from asyncio.gather(*coros)
    
    print("DONE")
    
    for x in modList:
        print(x.getName())
        
    return modList
    

        
if __name__ == '__main__':  
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
 
 
 
# def main(): 
    #dictionary to hold extra headers
    # HEADERS = {"X-API-Key":'d733b6d164864cc1b5aa3ff0e306e9a8'} 
     
    # mentorIds = [ 108762, 4878, 224480 ];
    # ninjaIds = [ 2311, 218625, 7024 ];
    # modList = [ ];
     
    # for x in mentorIds:
        #r = requests.get("https://www.bungie.net/platform/User/GetBungieNetUserById/" + str(x), headers=HEADERS);
        # r = async.get("https://www.bungie.net/platform/User/GetBungieNetUserById/" + str(x));
        # response = r.json();
        #print(response)
        # mod = Mod(response['Response']['displayName'], "Mentor", response['Response']['profilePicturePath'])
        # modList.append(mod)
        
    # for x in ninjaIds:
        #r = requests.get("https://www.bungie.net/platform/User/GetBungieNetUserById/" + str(x), headers=HEADERS);
        # r = async.get("https://www.bungie.net/platform/User/GetBungieNetUserById/" + str(x));
        # response = r.json();
        # mod = Mod(response['Response']['displayName'], "Ninja", response['Response']['profilePicturePath'])
        # modList.append(mod)

    # for y in modList:
        # print(y.getName())
     
    #make request for Gjallarhorn
    #r = requests.get("https://www.bungie.net/platform/Destiny/Manifest/InventoryItem/1274330687/", headers=HEADERS);
     
    #convert the json object we received into a Python dictionary object
    #and print the name of the item
    #inventoryItem = r.json()
    #print(inventoryItem['Response']['data']['inventoryItem']['itemName'])
     
    #Gjallarhorn

