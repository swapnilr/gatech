CC = gcc            
CFLAGS = -Wall   

# pattern rule for object files
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

rvm_main: seqsrchst.o steque.o rvm.o rvm_main.o
	$(CC) -o rvm_main seqsrchst.o steque.o rvm.o rvm_main.o

clean:
	rm -f *.o rvm_main