import sys

def dump_result(cache_servers):
    print(len(cache_servers))
    for i, server in enumerate(cache_servers):
        row = str(i) + ' ' + ' '.join(map(str, server))
        print(row)

def main(video_sizes, cache_servers, endpoints):
    print("VIDEO_SIZES")
    print(video_sizes)
    print("CACHE_SERVERS")
    print(cache_servers)
    print("ENDPOINT_LIST\n")
    for endpoint in endpoints:
        print("ENDPOINT #T{}".format(endpoint["id"]))
        for server in endpoint["servers_cache"]:
            print("  CACHE #{} -> {} (latency)".format(server["id"], server["latency"]))
        print("    - - -")
        for video in endpoint["videos"]:
            print("  VIDEO #{} -> {} (requests)".format(video["id"], video["requests"]))
        print()
 
def run(filename):
    with open(filename) as _file:
        video_len, endpoint_len, request_len, cache_len, cache_size = map(int, next(_file).split())
        video_sizes = map(int, next(_file).split())
        cache_servers = [cache_size for _ in range(0, cache_len)]
        endpoints = []
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
            endpoints[endpoint_id]["servers_cache"].sort(key=lambda k: k.get("id"))

        for line in _file:
            video_nbr, endpoint_id, requests_len = map(int, line.split())
            endpoints[endpoint_id]["videos"].append({"id": video_nbr,
                                                          "requests": requests_len})
        main(video_sizes, cache_servers, endpoints)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("No given file !")
