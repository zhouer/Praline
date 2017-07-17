import json

import bitcoin
import leveldb
import serial

from praline import dialog

def importAddress(priv):
    addr = bitcoin.privkey_to_address(priv)
    obj = {'address': addr, 'privateKey': priv}

    db = leveldb.LevelDB('/var/lib/Praline')
    db.Put(addr, json.dumps(obj))
    db = None

def getNewAddress():
    priv = bitcoin.encode_privkey(bitcoin.random_key(), 'wif_compressed')
    addr = bitcoin.privkey_to_address(priv)
    obj = {'address': addr, 'privateKey': priv}

    db = leveldb.LevelDB('/var/lib/Praline')
    db.Put(addr, json.dumps(obj))
    db = None

    return addr

def loadDatabase():
    keys = {}
    db = leveldb.LevelDB('/var/lib/Praline')
    for k, v in db.RangeIter():
        keys[k.decode('utf-8')] = json.loads(v.decode('utf-8'))['privateKey']
    db = None
    return keys

def chooseUTXO(utxos, amount):
    total = 0
    choosen = []

    for utxo in utxos:
        if total >= amount:
            break
        total += utxo['value']
        choosen.append(utxo)

    # balance is not enough
    if total < amount:
        return []

    return choosen

def send(toAddress, amount, fee, utxos):
    choosen = chooseUTXO(utxos, amount + fee)
    ins = []
    outs = []
    total = 0

    # return empty tx when fail to choose UTXO
    if not choosen:
        return ''

    for utxo in choosen:
        ins.append({
            'output': utxo['txid'] + ':' + str(utxo['vout']),
            'value': utxo['value']
        })
        total += utxo['value']
        print('input', utxo['txid'], utxo['vout'], '(address)', utxo['address'])

    outs.append({
        'address': toAddress,
        'value': amount
    })
    print('output (to)', toAddress, amount)

    if total - amount - fee != 0:
        changeAddress = getNewAddress()
        outs.append({
            'address': changeAddress,
            'value': total - amount - fee
        })
        print('output (change)', changeAddress, total - amount - fee)

    print('total', total)
    print('fee', fee)

    tx = bitcoin.mktx(ins, outs)

    keys = loadDatabase()

    for i, utxo in enumerate(choosen):
        tx = bitcoin.sign(tx, i, keys[utxo['address']])

    return tx

def sendSerialPort(ser, result, rid):
    obj = {'id': rid, 'result': result}
    res = (json.dumps(obj) + '\n').encode('utf-8')
    ser.write(res)
    ser.flush()

def main():
    ser = serial.Serial('/dev/ttyGS0', 115200)

    showDialog = dialog.init()

    while True:
        try:
            cmd = json.loads(ser.readline().decode('utf-8'))

            if cmd['method'] == 'version':
                sendSerialPort(ser, 'Praline 0.0.2', cmd['id'])
            elif cmd['method'] == 'newaddress':
                sendSerialPort(ser, getNewAddress(),  cmd['id'])
            elif cmd['method'] == 'listaddress':
                sendSerialPort(ser, list(loadDatabase().keys()),  cmd['id'])
            elif cmd['method'] == 'importprivkey':
                importAddress(cmd['params'][0])
                sendSerialPort(ser, True, cmd['id'])
            elif cmd['method'] == 'send':
                addr = cmd['params'][0]
                amount = cmd['params'][1]
                fee = cmd['params'][2]
                utxos = cmd['params'][3]

                # create transaction without user confirmation if the OLED is not available
                if not showDialog or dialog.showSendDialog(addr, amount):
                    sendSerialPort(ser, send(addr, amount, fee, utxos), cmd['id'])
                else:
                    sendSerialPort(ser, '', cmd['id'])
        except serial.serialutil.SerialException:
            print('SerialException')
            import time
            time.sleep(1)
            ser = serial.Serial('/dev/ttyGS0', 115200)


if __name__ == '__main__':
    main()
