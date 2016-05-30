import sys
import os
import struct
import re



def add_to_ouput():
    full_name = methods_name[stack[0][0]]
    for i in range(1, len(stack)):
        full_name += ";" + methods_name[stack[i][0]]
    if (full_name in output.keys()):
        output[full_name] += stack[-1][2]
    else:
        output[full_name] = stack[-1][2]
################################################################################
if len(sys.argv) < 2:
    print("Usage : python parse.py filename")
    sys.exit()
if not (os.path.exists(sys.argv[1])):
    print("filename not found")
    
    sys.exit()

main_thread = 1
finename = sys.argv[1]
current_section = 0
methods_name = {}
len_record = 14
all_records = []
stack = []
output = {}

file = open(sys.argv[1] , encoding = "ISO-8859-1")
for line in file:
    line = line.strip()
    if (line.startswith("*version")):
        current_section = 1
    elif (line.startswith("*threads")):
        current_section = 2
        continue
    elif (line.startswith("*methods")):
        current_section = 3
        continue
    elif (line.startswith("*end")):
        break
    if (current_section == 3):
        fields = line.split("\t")
        method_id = int(fields[0],16)
        methods_name[method_id] = fields[1] + "." + fields[2]
file.close()

file = open(sys.argv[1], "rb")
alldata = file.read()
file.close()
pos = alldata.find(b"SLOW")
offset, = struct.unpack("H", alldata[pos+6:pos+8])
pos += offset
numofrecords = int((len(alldata) - pos) / len_record)


for i in range(numofrecords):
    record = alldata[pos + i * 14 : pos + i * 14 + 14]
    thread_id,=struct.unpack("H",record[0:2])
    if (thread_id == main_thread):
        tmp,=struct.unpack("I",record[2:6])
        method_id= int(tmp / 4) * 4;
        method_action= tmp % 4;
        time_offset,=struct.unpack("I",record[10:14])
        all_records.append([thread_id, method_id, method_action, time_offset])
        print("name =", methods_name[method_id], "; action =", method_action, "; time =", time_offset)

# method_id, starttime, excl_time, last_time

blank = 0
last_time = 0
for record in all_records:
    thread_id = record[0];
    method_id = record[1];
    action = record[2];
    time = record[3];
    if (action == 0):
        if (len(stack) == 0) :
            blank += time - last_time
            print("blank", blank)
        stack.append([method_id, time, 0, time])
    else:
        if (len(stack) != 0):
            top = stack[-1]
            print(methods_name[method_id], time, top[3])
            top[2] += time - top[3]
            top[3] = time
            add_to_ouput()
            if (len(stack) != 1):
                below_top = stack[-2];
                below_top[2] += top[1] - below_top[3]
                below_top[3] = time
            stack.pop()
        else:
            print("len(stack) == 0", methods_name[method_id], time)
            temp_output = output
            output = {}
            for i in temp_output.keys():
                output[methods_name[method_id]+";"+i] = temp_output[i]
            output[methods_name[method_id]] = time - last_time
            blank = 0
    last_time = time

time = last_time
while (len(stack) != 0) :
    print("poping", methods_name[method_id], time)
    top = stack[-1]
    top[2] += time - top[3]
    top[3] = time
    add_to_ouput()
    if (len(stack) != 1):
        below_top = stack[-2];
        below_top[2] += top[1] - below_top[3]
        below_top[3] = time
    stack.pop()

temp_output = output
output = {}
for i in temp_output.keys():
    output["ALL;"+i] = temp_output[i]
output["ALL"] = blank

file = open("./result.txt", 'w+')
output_list = sorted(output.items(), key=lambda d:d[0])
for i in output_list:
    print(i[0], '\t', i[1], file=file)
file.close()

