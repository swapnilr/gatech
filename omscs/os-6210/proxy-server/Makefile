CC     = gcc
CFLAGS = -Wall

RPCGEN   = rpcgen
RPCGEN_FLAGS = -C -K 0

CURL_LIBS = $(shell curl-config --libs)
CURL_CFLAGS = $(shell curl-config --cflags)

GENERICS = hshtbl.c indexrndq.c indexminpq.c steque.c

RPC_FILES = proxy_rpc_svc.c proxy_rpc.h proxy_rpc_clnt.c

#### RPC Client Part ####
$(RPC_FILES): proxy_rpc.x
	$(RPCGEN) $(RPCGEN_FLAGS) $<

client: client.c proxy_rpc_clnt.c proxy_rpc.h
	$(CC) -o $@ $(CFLAGS) client.c proxy_rpc_clnt.c $(LIBS)

client_test: client_test.c proxy_rpc_svc.c proxy_rpc.h
	$(CC) -o $@ $(CFLAGS) client_test.c proxy_rpc_svc.c $(LIBS)

#### RPC Server & Libcurl ####
proxy: proxy.c proxy_rpc_svc.c proxy_rpc.h
	$(CC) -o $@ $(CFLAGS) $(CURL_CFLAGS) proxy.c proxy_rpc_svc.c $(CURL_LIBS)

#### Cache Policy Experiments ####
perform: rnd_perform lfu_perform lru_perform lrumin_perform

rnd_perform: cache_perform.c rnd.c $(GENERICS) fake_www.c
	$(CC) -o $@ $(CFLAGS) $^ $(LIBS)

lfu_perform: cache_perform.c lfu.c $(GENERICS) fake_www.c
	$(CC) -o $@ $(CFLAGS) $^ $(LIBS)

lru_perform: cache_perform.c lru.c $(GENERICS) fake_www.c
	$(CC) -o $@ $(CFLAGS) $^ $(LIBS)

lrumin_perform: cache_perform.c lrumin.c $(GENERICS) fake_www.c
	$(CC) -o $@ $(CFLAGS) $^ $(LIBS)

#### Cleanup ####
clean:
	rm -f $(RPC_FILES) *.o client client_test proxy_tes

