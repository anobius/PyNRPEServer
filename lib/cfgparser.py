import shlex

try:
    IS_C;
except NameError:
    from .shared.bits import sigscanvlen

def parseCFG(nrpe_file,):

    pFile = open(nrpe_file);
    rVal = { "command" : dict() };
    for i in pFile.readlines():
        line = i.strip();
        if line and line[0] not in ['#',';']:
            key,value = line.split('=',1);

            if key[:7].lower() == 'command' and '[' in key:
                res = sigscanvlen(key,len(key),"[#]","x#x");
                if not res:
                    continue;
                nrpe_command = key[res[0] + 1:res[0] + res[1] - 1];
                rVal['command'][nrpe_command] = value;#shlex.split(value);
            else:
                rVal[key] = value;
    return rVal;
