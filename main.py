import sys

class Video:
    videos = {}

    def __init__(self, id, size):
        self.id = id
        self.size = size
        Video.videos[id] = self

class Endpoint:
    endpoints = {}

    def __init__(self, id, latency):
        self.id = id
        self.dcLatency = latency
        self.caches = {}
        Endpoint.endpoints[id] = self

    def addCache(self, id, latency):
        if id in Cache.caches:
            self.caches[id] = c = Cache.caches[id]
        else:
            self.caches[id] = c = Cache(id)
        c.endpoints[self.id] = self
        c.latencies[self.id] = latency
        # ajouter cache dans la liste puis ajouter le endpoint dans le cache ainsi que la latency

class Cache:
    caches = {}
    size = 0

    def __init__(self, id):
        self.id = id
        self.freeSpace = Cache.size
        self.endpoints = {}
        self.latencies = {}
        self.requests = {}
        self.videos = {}
        self.opti = {}
        Cache.caches[id] = self

    def addRequest(self, request):
        if request.video.id not in self.requests:
            self.requests[request.video.id] = [request]
        else:
            self.requests[request.video.id].append(request)

    def getRequestsByVideo(self, video):
        return(self.requests[video.id])

    def reCalculateLatency(self, video):
        l = self.getRequestsByVideo(video)
        for r in l:
            r.latency = self.latencies[r.endpoint.id] * r.nb

    def whatIsTheGain(self, video):
        if video.size > self.freeSpace or video.id in self.videos:
            return(0)
        l = self.getRequestsByVideo(video)
        possibleLatency = 0
        latency = 0
        if video.id not in self.opti:
            for r in l:
                possibleLatency += (self.latencies[r.endpoint.id] * r.nb)
                latency += r.latency
            self.opti[video.id] = possibleLatency
            return(latency - possibleLatency)
        else:
            for r in l:
                latency += r.latency
            return(latency - self.opti[video.id])

    def addVideo(self, video):
        self.videos[video.id] = video
        self.freeSpace -= video.size
        self.reCalculateLatency(video)


class Request:
    requests = []

    @staticmethod
    def sort():
        Request.requests.sort(key=lambda k: k.latency, reverse=True)

    def __init__(self, endpoint, video, nb):
        self.endpoint = Endpoint.endpoints[endpoint]
        self.video = Video.videos[video]
        self.nb = nb
        self.latency = self.endpoint.dcLatency * nb
        for c in self.endpoint.caches.values():
            c.addRequest(self)
        Request.requests.append(self)

def algo():
    Request.sort()
    i = 0
    j = 0
    requestLen = len(Request.requests)
    while Request.requests:
        r = Request.requests[0]
        possibilities = []
        for c in r.endpoint.caches.values():
            gain = c.whatIsTheGain(r.video)
            if gain > 0:
                possibilities.append({"gain": gain,
                                      "cache": c})
        if (possibilities):
            possibilities.sort(key=lambda k: k["gain"], reverse=True)
            possibilities[0]["cache"].addVideo(r.video)
            Request.sort()
        else:
            Request.requests.pop(0)
            i += 1
        j += 1
        print("tour de boucle: ", j, "   supression: ", i, " / ", requestLen, file=sys.stderr)

def out():
    print(len(Cache.caches))
    for c in Cache.caches.values():
        ret = str(c.id)
        for v in c.videos.values():
            ret += (" " + str(v.id))
        print(ret)

def run(filename):
    with open(filename) as _file:
        video_len, endpoint_len, request_len, cache_len, cache_size = map(int, next(_file).split())
        Cache.size = cache_size
        video_sizes = list(map(int, next(_file).split()))

        for i,v in enumerate(video_sizes):
            Video(i, v)

        for endpoint_id in range(0, endpoint_len):
            latency, cache_server_len = map(int, next(_file).split())
            e = Endpoint(endpoint_id, latency)

            for _ in range(0, cache_server_len):
                cache_server_id, cache_server_latency = map(int, next(_file).split())
                e.addCache(cache_server_id, cache_server_latency)
        for line in _file:
            video_id, endpoint_id, requests_nbr = map(int, line.split())
            Request(endpoint_id, video_id, requests_nbr)
        Request.sort()
        algo()
        out()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("No given file !")
