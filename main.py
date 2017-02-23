import sys

def run(filename):
    with open(filename) as _file:
        video_len, endpoint_len, request_len, cache_len, cache_size = next(_file).split()
        video_sizes = [int(size) for size in next(_file).split()]
        cache_servers = [int(cache_size) for _ in range(0, int(cache_len))]
        endpoints = []
        for endpoint_id in range(0, int(endpoint_len)):
            latency, cache_server_len = next(_file).split()
            endpoints.append({"id": endpoint_id,
                              "dc_latency": int(latency),
                              "videos": [],
                              "servers_cache": []})
            for _ in range(0, int(cache_server_len)):
                cache_server_id, cache_server_latency = next(_file).split()
                endpoints[endpoint_id]["servers_cache"].append({"id": int(cache_server_id),
                                                                "latency": int(cache_server_latency)})
            endpoints[endpoint_id]["servers_cache"].sort(key=lambda k: k.get("id"))

        for line in _file:
            video_nbr, endpoint_id, requests_len = line.split()
            endpoints[int(endpoint_id)]["videos"].append({"id": int(video_nbr),
                                                          "requests" : int(requests_len)})


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("No given file !")
