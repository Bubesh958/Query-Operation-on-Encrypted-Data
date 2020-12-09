import socket
import csv
import time
import sqlite3

port = 9036
ip = '127.0.0.1'


def write_to_csv(data):
    rows = zip(*data.values())
    with open('server/encrypted_ans_data_in_server.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(data.keys())
        for row in rows:
            writer.writerow(row)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def send_file(file_name,conn):
    file = open(file_name)
    count = len(file.readlines())
    file.close()
    conn.send(str(count).encode('utf-8'))
    print count
    time.sleep(1)
    text_file = file_name
    with open(text_file, 'rb') as fs:
        while count !=0:
            data = fs.read(1024*1024)
            conn.send(data)
            count = count-1
        time.sleep(1)
        conn.send('ENDED'.encode('utf-8'))

if __name__ == '__main__':
    ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssFT.bind((ip, port))
    ssFT.listen(1)
    (conn, address) = ssFT.accept()
    encrypted_file = 'server/encrypted_data_in_server.csv'

    count = conn.recv(1024*1024)

    count = int(count.decode('utf-8'))
    print count
    c =0
    #Receive, output and save file
    with open(encrypted_file, "wb") as fw:
        print "3. Receiving.."
        while c <= count:
            data = conn.recv(1024*1024)
            if data.find('ENDED') != -1:
                print 'Breaking from file write'
                break
            else:
                fw.write(data)
            c = c+1

        print "4. Received.."
    ssFT.close()

    ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssFT.bind((ip, port + 1))
    ssFT.listen(1)
    (conn, address) = ssFT.accept()


    encrypted_data = {}
    ans = {}
    field_type = {}
    first_time = True
    with open(encrypted_file) as fd:
        read = csv.DictReader(fd,delimiter=',')
        for row in read:
            for key in row.keys():
                encrypted_data[key] = []
                ans[key] = []
            break
        for row in read:
            for key, value in row.items():
                if 'ope' in key or 'ashe' in key:
                    encrypted_data[key].append(value)
                    field_type[key] = 'INT'
                else:
                    field_type[key] = 'TEXT'
                    encrypted_data[key].append('"' + value + '"')

    con = sqlite3.connect('test.db')
    columns = encrypted_data.keys()
    file = open(encrypted_file)
    count = len(file.readlines())
    file.close()
    print count
    create = 'CREATE TABLE IF NOT EXISTS encrypted_data (ID INT PRIMARY KEY NOT NULL'
    insert = 'INSERT INTO encrypted_data (ID'
    for c in columns:
        create = create + ', ' + c + ' ' + field_type[c]
        insert = insert + ', ' + c 
    create = create + ')'
    insert = insert + ') VALUES ('

    # con.execute("DROP TABLE encrypted_data")
    # con.commit()
    # con.close()  

    con.execute(create)
    i = 1
    for a in zip(*encrypted_data.values()):
        q = insert + str(i) + ', ' + ', '.join(a) + ')'
        i = i + 1
        con.execute(q)

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    

    while True:
        query = conn.recv(1024*1024).decode('utf-8')
        print "\n\n\n6. Received Query : " + query + "\n"
        if query == '1':
            break
        cur.execute(query)
        result = [dict(row) for row in cur.fetchall()]
        # print result
        print "7. Sending only the result in encrypted form to Client\n\n"
        
        if len(result) != 0:
            v = {k: [dic[k] for dic in result] for k in result[0]}
            write_to_csv(v)
        else:
            write_to_csv({})
        send_file('server/encrypted_ans_data_in_server.csv',conn)
        
   


    con.execute("DROP TABLE encrypted_data")
    con.commit()
    con.close()  
    ssFT.close()







































































# def find_range(lt,en_name,en_lt,en_sal,en_job):
#     ans = []
#     c = 0
#     for i in en_lt:
#         # print i,lt,"\n"
#         if( i >= lt[0] and i <= lt[1]):
#             # print i,lt,c
#             ans.append(':'.join([en_name[c],str(en_lt[c]),str(en_sal[c]),en_job[c]]))
#             # print [en_name[c],str(en_lt[c]),str(en_sal[c]),en_job[c]]
#         c = c + 1
#     return ans

# def rsa_find(en_list,enc_value):
#     c = en_list.index(enc_value)
#     return (':'.join([en_name[c],str(en_age[c]),str(en_sal[c]),en_job[c]]))



# def sum_of_encrypted_numbers(en_lt):
#     return sum(en_lt)









# file = "data2.csv"
# en_age = []
# en_name = []
# en_sal = []
# en_job= []
# rd = {}
# with open(file) as fh:
#     rd = csv.DictReader(fh, delimiter=',')
#     for row in rd:
#         en_age.append(int(row["age"]))
#         en_name.append(row["name"])
#         en_sal.append(int(float(row["salary"])))
#         en_job.append(row["job"])

# lt = [10,22]
# lt[0] = conn.recv(1024*1024).decode('utf-8')
# lt[1] = conn.recv(1024*1024).decode('utf-8')
# lt = map(int,lt)
# print lt


# ans_age = find_range(lt,en_name,en_age,en_sal,en_job)



# ans_age = '-'.join(ans_age)
# conn.send(ans_age.encode('utf-8'))

# en_word = conn.recv(1024*1024).decode('utf-8')
# # print en_word
# index = rsa_find(en_name,en_word)
# # print index
# conn.send(str(index).encode('utf-8'))

# en_sum = sum_of_encrypted_numbers(en_sal)
# time.sleep(1)
# conn.send(str(en_sum).encode('utf-8'))


# ssFT.close()



