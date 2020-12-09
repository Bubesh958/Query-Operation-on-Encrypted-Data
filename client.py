import csv
import time
import socket
import sys
import ope
import rsa
import ashe

port = 9036
ip = '127.0.0.1'

def encrypt_data(data,field_type):
	encrypted_data = {}
	keys = {}
	for key,value in data.items():
		if field_type[key] == 'ope':
			encrypted_data[key],keys[key]= ope.ope(value)
		elif field_type[key] == 'ashe':
			encrypted_data[key],keys[key] = ashe.ashe(value)
		else:
			encrypted_data[key],keys[key] = rsa.rsa(value)
	return encrypted_data,keys

def decrypt_data(data,field_type,keys):
	decrypted_data = {}
	for key,value in data.items():
		if field_type[key] == 'ope':
			decrypted_data[key]= ope.decrypt_lt(keys[key][0],value)
		elif field_type[key] == 'ashe':
			decrypted_data[key] = ashe.decrypt_lt(keys[key][0],value)
		else:
			decrypted_data[key]= rsa.decrypt_lt(keys[key][0],value)
	return decrypted_data

def write_to_csv(data,file_name):
	rows = zip(*data.values())
	with open(file_name,'w') as f:
		writer = csv.writer(f)
		writer.writerow(data.keys())
		for row in rows:
			writer.writerow(row)

def send_file(file_name):
	file = open(file_name)
	count = len(file.readlines())
	csFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	csFT.connect((ip, port))
	csFT.send(str(count).encode('utf-8'))
	print str(count) + "\n1. Encrypting the file \n2. Sending the Encrypted file to server"
	time.sleep(1)
	text_file = file_name
	with open(text_file, 'rb') as fs:
	    while count !=0:
	        data = fs.read(1024*1024)
	        csFT.send(data)
	        count = count-1
	    time.sleep(1)
	    csFT.send('ENDED'.encode('utf-8'))
	csFT.close()


def query(keys):
    csFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csFT.connect((ip, port+1))
    while True:
        string = ''
        temp = raw_input()
        if temp =='1':
            csFT.send(temp.encode('utf-8'))
            break
        while temp != ';':
            if(temp[0] == '['):
                temp = temp[1:-1]
                temp = temp.split(':')
                temp = temp[0] + '_ope >= ' + str(ope.encrypt(keys[temp[0]+'_ope'][1],int(temp[1]))) + ' and ' + temp[0] +'_ope <= ' + str(ope.encrypt(keys[temp[0]+'_ope'][1],int(temp[2])))
                string = string +' ' + temp
            elif '==' in temp:
                k = temp.split('==')[0].strip()
                v = temp.split('==')[1].strip()
                if unicode(v,'utf-8').isnumeric():
                    temp = k + '_ope == ' + str(ope.encrypt(keys[k+'_ope'][1],int(v)))
                    string = string + ' ' + temp
                else:
                    temp = k + ' == "' + rsa.encrypt_word(keys[k][1],v) + '"'
                    string = string + ' ' + temp
            elif '>=' in temp:
                k = temp.split('>=')[0].strip()
                v = temp.split('>=')[1].strip()
                if unicode(v,'utf-8').isnumeric():
                    temp = k + '_ope >= ' + str(ope.encrypt(keys[k+'_ope'][1],int(v)))
                    string = string + ' ' + temp
                else:
                    temp = k + ' >= "' + rsa.encrypt_word(keys[k][1],v) + '"'
                    string = string + ' ' + temp
            elif '<=' in temp:
                k = temp.split('<=')[0].strip()
                v = temp.split('<=')[1].strip()
                if unicode(v,'utf-8').isnumeric():
                    temp = k + '_ope <= ' + str(ope.encrypt(keys[k+'_ope'][1],int(v)))
                    string = string + ' ' + temp
                else:
                    temp = k + ' <= "' + rsa.encrypt_word(keys[k][1],v) + '"'
                    string = string + ' ' + temp
            else:
                string = string +' ' + temp
            temp = raw_input()
        print "\n5. Sending Query to Server : " + string + "\n"
        if string =='1':
            csFT.send(string.encode('utf-8'))
            break
        csFT.send(string.encode('utf-8'))
        encrypted_file = 'client/encrypted_ans_data_in_client.csv'
        count = csFT.recv(1024*1024)
        count = int(count.decode('utf-8'))
        # print count
        c = 0
        with open(encrypted_file, 'wb') as fw:
            print "\n\n\n\n8. Receiving the result in encrypted form"
            while c <= count:
                data = csFT.recv(1024*1024)
                if data.find('ENDED') != -1:
                    print 'Breaking from file write'
                    break
                else:
                    fw.write(data)
                c = c + 1
            print "9. Received the result \n"

        ans = {}
        with open(encrypted_file) as fd:
            read = csv.DictReader(fd,delimiter=',')
            for row in read:
                for key in row.keys():
                    if key == 'ID' or 'ashe' in key:
                        continue
                    ans[key] = []
                break
        with open(encrypted_file) as fd:
            read = csv.DictReader(fd,delimiter=',')
            for row in read:
                for key, value in row.items():
                    if key == 'ID' or 'ashe' in key:
                        continue
                    if 'ope' in field_type[key]:
                        ans[key].append(int(value))
                    else:
                        ans[key].append(value)
            # print ans
            print "10. Check decrypted_ans_data_in_client.csv for the decrypted result\n"
        decrypted_data = decrypt_data(ans,field_type,keys)
        write_to_csv(decrypted_data,'client/decrypted_ans_data_in_client.csv')

    csFT.close()


if __name__ == '__main__':
    file_name = "data.csv"
    data = {}
    field_type = {}
    with open(file_name) as fd:
        read = csv.DictReader(fd, delimiter=',')
        for row in read:
            for field in row.keys():
                string = unicode(row[field],'utf-8') 
                if string.isnumeric():
                    field_type[field] = 'integer'
                    field_type[field + '_ope'] = 'ope'
                    field_type[field + '_ashe'] = 'ashe'
                    data[field + '_ope'] = []
                    data[field + '_ashe'] = []
                else:
                    field_type[field] = 'string'
                    data[field] = []
            break
    with open(file_name) as fd:
        read = csv.DictReader(fd, delimiter=',')
        for row in read:
            for key,value in row.items():
                if field_type[key] == 'integer':
                    data[key + '_ope'].append(int(value))
                    data[key + '_ashe'].append(int(value))
                else:
                    data[key].append(value)




	encrypted_data,keys = encrypt_data(data,field_type)
	write_to_csv(encrypted_data,'client/encrypted_data_in_client.csv')
	send_file("client/encrypted_data_in_client.csv")
	time.sleep(1)
	query(keys)