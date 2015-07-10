import asyncio
import aiohttp
import json
 
headers = {'X-API-Key' : 'd733b6d164864cc1b5aa3ff0e306e9a8'}  
modList = []; 
 
class Mod:
    
    def __init__(self, name, role, url, active, memberid):
        self.name = name
        self.role = role
        self.url = 'http://www.bungie.net' + url
        self.active = active
        self.memberid = memberid
                
class ModList:

    def __init__(self, list):
        self.list = list
 
def encode_mod(obj):
    if isinstance(obj, Mod):
        return obj.__dict__
    else:
        raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))
 
@asyncio.coroutine 
def fetch_page(url, likes, posts, role, memberid):
    global modList
    global headers
    
    connector = aiohttp.TCPConnector(verify_ssl=False)
    
    response = yield from aiohttp.request('GET', url, headers=headers, connector=connector)
    likesTime = yield from aiohttp.request('GET', likes, headers=headers, connector=connector)
    postsTime = yield from aiohttp.request('GET', posts, headers=headers, connector=connector)
    data = yield from response.json()
    timeData1 = yield from likesTime.json()
    timeData2 = yield from postsTime.json()
    
    if response.status == 200:

        timeArr1 = timeData1['Response']['posts']
        timeArr2 = timeData2['Response']['posts']
        
        time1 = timeArr1[len(timeArr1)-1]['lastModified']
        time2 = timeArr2[len(timeArr2)-1]['lastModified']
        
        lastActive = time1 if (time1 > time2) else time2
        
        #print (data['Response']['displayName'])
        #print (time1)
        #print (time2)
        #print (lastActive)
        #print ('')
        
        mod = Mod (data['Response']['displayName'], role, data['Response']['profilePicturePath'], lastActive, memberid)
        modList.append(mod)
        
    response.close()
    likesTime.close()
    postsTime.close()
    connector.close()
    
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
        coros.append(asyncio.Task(fetch_page(profile, likes, posts, "Mentor", x)))
    
    for x in ninjaIds:
        profile = profileUrl + str(x)
        likes = likesUrl1 + str(x) + likesUrl2
        posts = postsUrl1 + str(x) + postsUrl2
        coros.append(asyncio.Task(fetch_page(profile, likes, posts, "Ninja", x)))
    
    yield from asyncio.gather(*coros)
    
    print("Content-Type: application/json")
    print ('')

    modList.sort(key=lambda r: r.active, reverse=True)
    jsonModList = ModList(modList)
    print(json.dumps(jsonModList.__dict__, default=encode_mod))
        
if __name__ == '__main__':  
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
 

