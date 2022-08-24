CC = gcc
CFLAGS  = -g -Wall
TARGET = test
all: $(TARGET)
$(TARGET): $(TARGET).cxx
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).cxx -Ixgboost/include -Ixgboost/rabit/include -Lxgboost/lib -lxgboost -lstdc++
clean:
	$(RM) $(TARGET)
