final_proxies = []
web_results = []
config_data = {}
config_server_data = {}


def printvaribles(op):
    if op == "fp":
        print("Final Proxies:", final_proxies)
    elif op == "wr":
        print("Web Results:", web_results)
    elif op == "cd":
        print("Config Data:", config_data)
    elif op == "csd":
        print("Config Server Data:", config_server_data)