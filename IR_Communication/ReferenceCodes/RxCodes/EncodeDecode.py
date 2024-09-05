# Data encryption key.
ENCRYPTION_KEY = [ 0xC5, 0x07, 0x8C, 0xA9, 0xBD, 0x8B, 0x48, 0xEF, 0x88, 0xE1, 0x94, 0xDB, 0x63, 0x77, 0x95, 0x59 ]
# Data packet identifier.
PACKET_SIGNATURE = [ 0x63, 0xF9, 0x5C, 0x1B ]

# Data packet to transmit.
DataPacket = {
   "SIGNATURE": PACKET_SIGNATURE,
   "DATA_LENGTH": 0,
   "DATA": [],
   "CHECKSUM": 0,
}

class EncodeDecodePacket():
    
    ''' 
    Encrypt Tx-ed data and decrypt Rx-ed data
        @ Protocol: "exclusive-or" operation. '''  
    def cryptData(self, data):
        key_id = 0
        for i in range(len(data)):

            # print("BEFORE CRYPT: ", hex(data[i]))
            data[i] ^= ENCRYPTION_KEY[key_id]
            key_id += 1
            if(key_id) >= len(ENCRYPTION_KEY):
                key_id = 0
            # print("AFTER CRYPT: ", hex(data[i]))
        return data

    ''' 
    Convert data packet into a string of bit-stream
        @ input: data packet struct
        @ output: a string of bit-stream '''
    def getEncodedDataPacketStream(self, data):
            
        DataPacket["SIGNATURE"] = PACKET_SIGNATURE
        DataPacket["DATA_LENGTH"] = len(data)
        DataPacket["DATA"] = data
        DataPacket["CHECKSUM"] = 0
            
        signature_stream = ''
        for i in range(len(DataPacket["SIGNATURE"])):
            bin_num = "{0:08b}".format(DataPacket["SIGNATURE"][i], 8)
            signature_stream = signature_stream + str(bin_num)
        # print(signature_stream)    

        data_length_stream = str("{0:08b}".format(DataPacket["DATA_LENGTH"], 8))
        # print(data_length_stream)

        data_stream = ''
        DataPacket["DATA"] = EncodeDecodePacket.cryptData(DataPacket["DATA"])
        for i in range(len(DataPacket["DATA"])):
            bin_num = "{0:08b}".format(DataPacket["DATA"][i], 8)
            data_stream = data_stream + str(bin_num)
            
            # Checksum encoding protocol: "exclusive-or"
            DataPacket["CHECKSUM"] ^= DataPacket["DATA"][i]
        # print(data_stream)    

        checksum_stream = str("{0:08b}".format(DataPacket["CHECKSUM"], 8))
        # print(checksum_stream)

        return signature_stream + data_length_stream + data_stream + checksum_stream
    
    
    ''' 
    Convert received data into a data packet form
        @ input: a string of bit-stream
        @ output: data packet struct '''
    def getDncodedData(self, data):

        RxDataPacket = {
            "SIGNATURE": [],
            "DATA_LENGTH": 8,
            "DATA": [],
            "CHECKSUM": 0,
        }

        for i  in range(4):
            if data[i] != PACKET_SIGNATURE[i]:
                print('PACKET SIGNATURE ERROR')
                return False
        
        if data[4] != 8:
            print('RECIEVED DATA SIZE ERROR')
            return False
        
        data_received = data[5:13]
        rxed_check_sum = data[13]
        
        for i in range(len(data_received)):
            # checksum ^= data_received[i]

            RxDataPacket["CHECKSUM"] ^= data_received[i]

        if RxDataPacket["CHECKSUM"]  != rxed_check_sum:
            print('RECEIVED DATA DOES NOt MATCH WITH CHECKSUM')
            return False
        
        decrypted_data = self.cryptData(data_received)
        # print("Decrypted: ", decrypted_data)
        return decrypted_data

#   Test codes in this module
if __name__ == '__main__':

    pass

    # print(EncodeDecodePacket.getDataPacketStream([0xff, 0xee, 0xac, 0x1a, 0x11, 0x73, 0x24, 0x35]))
    
    # data = [0xff, 0xee, 0xac, 0x1a]
    # for i in range(len(data)):
    #     print(hex(data[i]), end=" ")
    # print('')
    
    # data = EncodeDecodePacket.cryptData([0xff, 0xee, 0xac, 0x1a])
    # for i in range(len(data)):
    #     print(hex(data[i]), end=" ")
    # print('')

    # data = EncodeDecodePacket.cryptData([0x3a, 0xe9, 0x20, 0xb3])
    # for i in range(len(data)):
    #     print(hex(data[i]), end=" ")
    # print('')

