import sys

class Video:
    videos = {}

    def __init__(self, id, size):
        self.id = id
        self.size = size
        Video.videos[id] = self

class Cache:
    caches = {}
    size = 0

    # @staticmethod
    # def getCache(cache_id):


    def __init__(self, id):
        self.id = id
        self.endpoints = {}
        self.videos = {}
        self.freeSpace = Cache.size
        self.requests = []
        self.latencies = {}
        Cache.caches[id] = self

    def addVideo(self, video):
        self.videos[video.id] = video
        self.freeSpace -= video.size

    def increaseLatency(self, video):
        requests = [r for r in self.requests if r.video.id == video]
        ret = 0
        for r in requests:
            delta = r.endpoint.dcLatency - self.latencies[r.endpoint.id]
            if (delta != 0):
                ret += (r.nb * delta)
        return(ret)

    # def freeSpace(self):
    #   s = Cache.size
    #   for v in self.videos:
    #       s -= v.size
    #   return s

class Endpoint:
    endpoints = {}

    @staticmethod
    def get(endpoint):
        return Endpoint.endpoints[endpoint]

    @staticmethod
    def sort():
        for e in Endpoint.endpoints.values():
            e.latencies.sort(key=lambda k: k.get("latency"))

    def __init__(self, id, lat):
        self.id = id
        self.caches = {}
        self.latencies = []
        self.latenciesDict = {}
        self.dcLatency = lat
        # self.requests = []
        Endpoint.endpoints[id] = self

    def addCaches(self, cache, lat):
        if cache not in Cache.caches:
            c = Cache(cache)
        else:
            c = Cache.caches[cache]
        self.caches[cache] = c
        c.latencies[self.id] = lat
        if self.id not in c.endpoints:
            c.endpoints[self.id] = self
        self.latencies.append({"id": cache,
                               "cache": c,
                               "latency": lat})
        self.latenciesDict[cache] = lat

class Request:
    requests = []

    @staticmethod
    def sort():
        Request.requests.sort(key=lambda k: k.latency, reverse=True)

    def __init__(self, video, endpoint, nb):
        e = Endpoint.get(endpoint)
        self.video = Video.videos[video]
        self.endpoint = e
        self.nb = nb
        self.latency = e.dcLatency * nb
        Request.requests.append(self)
        for c in e.caches.values():
            c.requests.append(self)
        # e.requests.append(self)

    def latency(self):
        lat = Endpoint.get(self.endpoint).dcLatency
        for c in self.endpoint.caches:
            if self.video in c.videos and self.endpoint.latencies[c.id] < lat:
                lat = self.endpoint.latencies[c.id]
        self.latency = lat
        return lat
                

def algo():
    for r in Request.requests:
        possibilities = []
        for l in r.endpoint.latencies:
            c = l["cache"]
            id = l["id"]
            if r.video.size < c.freeSpace:
                gain = c.increaseLatency(r.video.id)
                if (gain != 0):
                    possibilities.append({"cache": c,
                                          "gain": gain})
        if (possibilities):
            possibilities.sort(key=lambda k: k["gain"], reverse=True)
            possibilities[0]["cache"].addVideo(r.video)


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

        cache_servers = [cache_size for _ in range(0, cache_len)]
        endpoints = []
        requests = []
        for endpoint_id in range(0, endpoint_len):
            latency, cache_server_len = map(int, next(_file).split())
            endpoints.append({"id": endpoint_id,
                              "dc_latency": latency,
                              "videos": [],
                              "servers_cache": []})

            e = Endpoint(endpoint_id, latency)

            for _ in range(0, cache_server_len):
                cache_server_id, cache_server_latency = map(int, next(_file).split())
                endpoints[endpoint_id]["servers_cache"].append({"id": cache_server_id,
                                                                "latency": cache_server_latency})

                e.addCaches(cache_server_id, cache_server_latency)

            endpoints[endpoint_id]["servers_cache"].sort(key=lambda k: k.get("latency"))

        for line in _file:
            video_id, endpoint_id, requests_nbr = map(int, line.split())
            endpoints[endpoint_id]["videos"].append({"id": video_id,
                                                     "requests": requests_nbr})
            requests.append({"endpoint_id" : endpoint_id,
                             "video_id": video_id,
                             "video_size": video_sizes[video_id],
                             "connected_cache_servers": endpoints[endpoint_id]["servers_cache"],
                             "total_latency": requests_nbr * endpoints[endpoint_id]["dc_latency"],
                             "dc_latency": endpoints[endpoint_id]["dc_latency"]})

            Request(video_id, endpoint_id, requests_nbr)

        Request.sort()
        Endpoint.sort()
        algo()
        out()

        # requests.sort(key=lambda k: k.get("total_latency"), reverse=True)
        # main(video_sizes, cache_servers, endpoints, requests)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("No given file !")
