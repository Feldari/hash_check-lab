#!/usr/bin/python3

import hmac
import sys

def gen_tag(msg, key):
    hm = hmac.new(key.encode())
    hm.update(msg.encode())
    return hm.hexdigest()

def usage():
    print("Usage: {} <flag> <msg> <key name>".format(sys.argv[0]))
    print("Valid flags are -g for generate or -v to verify")
    print("If -g msg is string if -v msg should be text file with lines")
    print("formatted as:")
    print("<original text string> :<hash to verify>")

def generate():
    if not sys.argv[3:]:
        usage()
        sys.exit(0)

    msg = sys.argv[2]
    filename = sys.argv[3] + '.key'

    with open(filename) as f:
        key = f.read()

    t = gen_tag(msg, key)
    print(msg + ':' + t)

def verify():
    if not sys.argv[3:]:
        usage()
        sys.exit(0)

    filename = sys.argv[2] + '.txt'
    with open(filename, 'r') as f:
        text = f.read()

    keyfile = sys.argv[3] + '.key'
    with open(keyfile) as k:
        key = k.read()

    with open('verified.txt', 'a') as v:
        v.write('Data format: <match?> :<orig message> :<given hash> '
                ':<generated hash>\n')

    for line in text.split('\n'):
        (msg,givhash) = line.split(':')
        genhash = gen_tag(msg, key)
        if genhash == givhash:
            match = 'YES match'
        else:
            match = 'NO  match'
        output = match + " :" + msg + " :" + givhash + " :" + genhash + "\n"
        with open('verified.txt', 'a') as v:
            v.write(output)
        

if __name__ == '__main__':

    if sys.argv[1] == '-g':
        generate()
    elif sys.argv[1] == '-v':
        verify()
    else:
        usage()
        sys.exit(0)
