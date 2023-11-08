# Linker.py

from hf import *

opcodeDict = {
    'add': '000000',
    'sub': '000000',
    'slt': '000000',
    'or': '000000',
    'and': '000000',
    'lw': '100011', 
    'sw' : '101011',
    'addi': '001000',
    'beq' : '000100',
    'j' : '000010'

}

operandDict = {'$0': '000', '$1': '001', '$2': '010', '$3': '011', '$4': '100', '$5': '101', '$6': '111', '1': '000001', '0': '000000', '2': '000010', '3': '000011', '4': '000100', '5': '000101', '6': '000110', '7': '000111', '8': '001000', '9': '001001', '10': '001010', '11': '001011', '12': '001100', '13': '001101', '14': '001110', '15': '001111', '16': '010000', '17': '010001', '18': '010010', '19': '010011', '20': '010100', '21': '010101', '22': '010110', '23': '010111', '24': '011000', '25': '011001', '26': '011010', '27': '011011', '28': '011100', '29': '011101', '30': '011110', '31': '011111', '32': '100000', '33': '100001', '34': '100010', '35': '100011', '36': '100100', '37': '100101', '38': '100110', '39': '100111', '40': '101000', '41': '101001', '42': '101010', '43': '101011', '44': '101100', '45': '101101', '46': '101110', '47': '101111', '48': '110000', '49': '110001', '50': '110010', '51': '110011', '52': '110100', '53': '110101', '54': '110110', '55': '110111', '56': '111000', '57': '111001', '58': '111010', '59': '111011', '60': '111100', '61': '111101', '62': '111110', '63': '111111'}


functFieldDict = {
    'add': '100000',
    'sub': '100010',
    'slt': '101010',
    'or': '100101',
    'and': '100100',
}  
# add all the necessary functFields

def ConvertAssemblyToMachineCode(inline):
    '''given a string corresponding to a line of assembly,
    strip out all the comments, parse it, and convert it into
    a string of binary values'''

    outstring = ''

    if inline.find('#') != -1:
        inline = inline[0:inline.find('#')]  # get rid of anything after a comment
    if inline != '':
        words = inline.split()  # assuming syntax words are separated by space, not comma
        operation = words[0]
        operands = words[1:]
        if operation in opcodeDict:
            opcode = opcodeDict[operation]
            if opcode == '000000':  # R-type instruction
                functField = functFieldDict[operation]
                rd = operandDict[operands[0]]
                rt = operandDict[operands[1]]
                rs = operandDict[operands[2]]  # Swap the order of rs and rt
                outstring = opcode + rt + rs + rd + functField
                outstring = bs2hex(outstring)   #  convert binary string to hexadecimal

            elif opcode == '100011' or opcode == '101011':  # LW or SW instruction
                rt = operandDict[operands[0]]
                mem_offset = operands[1]
                rs, imm = mem_offset.split('($')
                imm = imm[:-1]  # remove the closing bracket
                rs = operandDict[rs]
                imm = int(imm)
                imm_binary = int2bs(imm, 16, signed=True)[-6:]
                outstring = opcode + rs + rt + imm_binary
                outstring = bs2hex(outstring)  # convert binary string to hexadecimal

            elif operation == 'addi':  # ADDI instruction
                rs = operandDict[operands[1]]
                rt = operandDict[operands[0]]
                imm = int(operands[2])
                imm_binary = int2bs(imm, 16, signed=True)[-6:]
                outstring = '001000' + rs + rt + '010' + imm_binary
                outstring = bs2hex(outstring)  # convert binary string to hexadecimal
            
            elif operation == "beq":
                rs = operandDict[operands[1]]
                rt = operandDict[operands[0]]
                imm = int(operands[2])
                imm_binary = int2bs(imm, 16, signed=True)[-6:]
                outstring = '000100' + rt + rs + '000' + imm_binary
                outstring = bs2hex(outstring)  # convert binary string to hexadecimal

            elif operation == "j":
                imm = int(operands[0])
                imm_binary = int2bs(imm, 16, signed=True)[-6:]
                outstring = '000010' + '000' + '000' + '000' + imm_binary
                outstring = bs2hex(outstring)  # convert binary string to hexadecimal

            else:
                # not R-type or LW/SW instruction, handle as usual
                outstring = opcode
                for oprand in operands:
                    if ',' in oprand:
                        oprand = oprand.replace(',', '')  # remove the comma
                    if oprand:
                        outstring += operandDict[oprand]
                    else:
                        outstring += '000'
                outstring = bs2hex(outstring)  # convert binary string to hexadecimal
    return outstring
               
               
def LinkAssemblies(inputfiles, outputfile):
    '''given a list of ascii assembly files, read them in line by line,
    convert each line of assembly to machine code, and concatenate them
    to generate one big output file'''

    outlines = []
    for infilename in inputfiles:
        with open(infilename) as f:
            lines = [line.rstrip() for line in f.readlines()]
            for curline in lines:
                outstring = ConvertAssemblyToMachineCode(curline)
                if outstring != '':
                    outlines.append(outstring)
        f.close()

    with open(outputfile, 'w') as of:
        for outline in outlines:
            of.write(outline)
            of.write("\n")
    of.close()