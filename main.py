import sys

def dump_result(cache_servers):
    print(len([cs for cs in cache_servers if cs]))
    for i, server in enumerate(cache_servers):
        if not server:
            continue
        row = str(i) + ' ' + ' '.join(map(str, server))
        print(row)

def basic_heuristic(requests, cache_servers):
    # We simply try to cache the slowest videos...
    cache_servers_usage = [0 for _ in range(0, len(cache_servers))]
    used_cache_servers = [[] for _ in range(0, len(cache_servers))]
    for request in requests:
        for connected_cache_server in request["connected_cache_servers"]:
            csid = connected_cache_server["id"]
            if request["video_size"] + cache_servers_usage[csid] <= cache_servers[csid]:
                cache_servers_usage[csid] += request["video_size"]
                used_cache_servers[csid].append(request["video_id"])
                break
    return used_cache_servers

def main(video_sizes, cache_servers, endpoints, requests):
    # print("VIDEO_SIZES")
    # print(video_sizes)
    # print("CACHE_SERVERS")
    # print(cache_servers)
    # print("REQUESTS")
    # for request in requests:
    #     print(request)
    # print("ENDPOINT_LIST\n")
    # for endpoint in endpoints:
    #     print("ENDPOINT #{}".format(endpoint["id"]))
    #     for server in endpoint["servers_cache"]:
    #         print("  CACHE #{} -> {} (latency)".format(server["id"], server["latency"]))
    #     print("    - - -")
    #     for video in endpoint["videos"]:
    #         print("  VIDEO #{} -> {} (requests)".format(video["id"], video["requests"]))
    #     print()
    res = basic_heuristic(requests, cache_servers)
    dump_result(res)
 
def run(filename):
    with open(filename) as _file:
        video_len, endpoint_len, request_len, cache_len, cache_size = map(int, next(_file).split())
        video_sizes = map(int, next(_file).split())
        cache_servers = [cache_size for _ in range(0, cache_len)]
        endpoints = []
        requests = []
        for endpoint_id in range(0, endpoint_len):
            latency, cache_server_len = map(int, next(_file).split())
            endpoints.append({"id": endpoint_id,
                              "dc_latency": latency,
                              "videos": [],
                              "servers_cache": []})
            for _ in range(0, cache_server_len):
                cache_server_id, cache_server_latency = map(int, next(_file).split())
                endpoints[endpoint_id]["servers_cache"].append({"id": cache_server_id,
                                                                "latency": cache_server_latency})
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
        requests.sort(key=lambda k: k.get("total_latency"))
        main(video_sizes, cache_servers, endpoints, requests)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("No given file !")
