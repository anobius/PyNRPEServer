#flag tools
def isBitSet(currentValue, bit):
    return True if (currentValue & bit) else False

def setBit(currentValue, bit):
    return currentValue | bit;

def unsetBit(currentValue, bit):
    if isBitSet(currentValue,bit):
        return currentValue - (currentValue & bit);
    return currentValue;


def sigscan(bContent,length,signature,mask):
    '''
    Signature-scanning, derived from finding memory addresses of function routines on C/C++ Libraries.
    :param bContent: Search body
    :param length: length of the body
    :param signature: signature
    :param mask: mask
    :return: index number
    '''
    sig_len = len(signature);
    for i in range(0,length):
        v = 0;
        while v < sig_len:
            if (mask[v] != '?' and bContent[i+v] != signature[v]):
                break;
            v+=1;
        if v == sig_len:
            return i;
    return None

def sigscanvlen(bContent,length,signature,mask):
    '''
    Variable-length signature scanning.
    '#' is the symbol used in a mask to specify a variable length.
    The character in the signature to be ignored will be the index of this pound character in the mask.
    :param bContent: Search body
    :param length: length of the body
    :param signature: signature
    :param mask: mask
    :return: index number, result length
    '''
    sig_len = len(signature);
    for i in range(0,length):
        v = 0;
        tBackOffset = 0;
        while v < sig_len:
            cOffset = i+v - tBackOffset;
            sOffset = v - tBackOffset;
            #print sOffset,cOffset
            if (cOffset < length and mask[sOffset] != '?' and bContent[cOffset] != signature[sOffset]) and mask[sOffset] != "#":
                break;
            elif (mask[sOffset] == "#"):
                cOffset += 1;
                sOffset += 1;
                iOffset = sigscanvlen(bContent[cOffset:],length - cOffset, signature[sOffset:], mask[sOffset:])[0];
                if not iOffset:
                    #break;  #do we break or assume it would never be found ?
                    return None;
                tBackOffset += iOffset;
                sig_len += iOffset;
                v += iOffset + len(mask[sOffset:]);
            v+=1;
        if v == sig_len:
            return i,v;
    return None
