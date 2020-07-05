from SLiCAPplots import *

def getValues(elmt, param, numeric, parDefs):
    """
    Returns the symbolic or numeric value of numerator and the denominator
    of a parameter of an element.
    """
    if numeric == True:
        value = sp.N(fullSubs(elmt.params[param], parDefs))
    else:
        value = elmt.params[param]
    try:
        if ini.Laplace in value.atoms(sp.Symbol):
            (numer, denom) = sp.fraction(value)
        else:
            numer = value
            denom = 1
    except:
        numer = value
        denom = 1
    return (numer, denom)

def getValue(elmt, param, numeric, parDefs):
    """
    Returns the symbolic or numeric value of a parameter of an element.
    """
    if param not in elmt.params.keys():
        return 0
    if numeric == True:        
        value = sp.N(fullSubs(elmt.params[param], parDefs))
    else:
        value = elmt.params[param]
    return value
        
def makeMatrices(cir, parDefs, numeric, gainType, lgRef):
    """
    Modifications in the circuit object, necessary for calculation different
    gain types need to be temporary. The circuit data before and after
    running 'makeMatrices' should be the same!
    
    1. If gainType == 'asymptotic':
        store the model of lgRef
        modify the model of lgRef to 'N'
        update depVars and varIndex
        create the matrices
        restore the model of lgRef
        update depVars and varIndex
        
    2. If gainType == 'direct', 'loopgain' or 'servo':
        store value of lgRef
        set value of lgRef element to zero
        create the matrices
        restore the value of lgRef
        
        loopgain and servo will be calculated with the output of lgRef 
        as source and the input of lgRef as detector.
        
    3. If gainType == 'vi' or 'gain':
        no alterations of the circuit need to be made
    """
    if gainType == 'vi' or gainType == 'gain':
        pass
    elif gainType == 'direct' or gainType == 'loopgain' or gainType == 'servo':
        lgValue = cir.elements[lgRef].params['value']
        cir.elements[lgRef].params['value'] = 0
    elif gainType == 'asymptotic':
        lgRefModel = cir.elements[lgRef].model
        cir.elements[lgRef].model = 'N'
        cir.updateMdata()
    varIndex = cir.varIndex
    dim = len(cir.varIndex.keys())
    Vv = [0 for i in range(dim)]
    M  = [[0 for i in range(dim)] for i in range(dim)]
    for i in range(len(cir.depVars)):
        Vv[i] = sp.Symbol(cir.depVars[i])
    for el in cir.elements.keys():
        elmt = cir.elements[el]
        if elmt.model == 'C':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos0] += value * ini.Laplace
            M[pos0][pos1] -= value * ini.Laplace
            M[pos1][pos0] -= value * ini.Laplace
            M[pos1][pos1] += value * ini.Laplace
        elif elmt.model == 'L':
            dVarPos = varIndex['I_'+ elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
            M[dVarPos][dVarPos] -= value * ini.Laplace
        elif elmt.model == 'R':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = 1/getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos0] += value
            M[pos0][pos1] -= value
            M[pos1][pos0] -= value
            M[pos1][pos1] += value
        elif elmt.model == 'r':
            dVarPos = varIndex['I_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
            M[dVarPos][dVarPos] -= value
        elif elmt.model == 'E':
            dVarPos = varIndex['I_o_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += denom
            M[dVarPos][pos1] -= denom
            M[dVarPos][pos2] -= numer
            M[dVarPos][pos3] += numer
        elif elmt.model == 'EZ':
            dVarPos = varIndex['I_o_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            (zoN, zoD) = getValues(elmt, 'zo', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += denom * zoD
            M[dVarPos][pos1] -= denom * zoD
            M[dVarPos][pos2] -= numer * zoD
            M[dVarPos][pos3] += numer * zoD
            M[dVarPos][dVarPos] -= zoN * denom
        elif elmt.model == 'F':
            dVarPos = varIndex['I_i_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += numer
            M[pos1][dVarPos] -= numer
            M[pos2][dVarPos] += denom
            M[pos3][dVarPos] -= denom
            M[dVarPos][pos2] += 1
            M[dVarPos][pos3] -= 1
        elif elmt.model == 'g':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos2] += value
            M[pos0][pos3] -= value
            M[pos1][pos2] -= value
            M[pos1][pos3] += value
        elif elmt.model == 'G':
            dVarPos = varIndex['I_o_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos2] += numer
            M[dVarPos][pos3] -= numer
            M[dVarPos][dVarPos] -= denom
        elif elmt.model == 'H':
            dVarPosO = varIndex['I_o_' + elmt.refDes]
            dVarPosI = varIndex['I_i_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPosO] += 1
            M[pos1][dVarPosO] -= 1
            M[pos2][dVarPosI] += 1
            M[pos3][dVarPosI] -= 1
            M[dVarPosI][pos2] += 1
            M[dVarPosI][pos3] -= 1
            M[dVarPosO][pos0] += denom
            M[dVarPosO][pos1] -= denom
            M[dVarPosO][dVarPosI] -= numer
        elif elmt.model == 'HZ':
            dVarPosO = varIndex['I_o_' + elmt.refDes]
            dVarPosI = varIndex['I_i_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            (zoN, zoD) = getValues(elmt, 'zo', numeric, parDefs)
            M[pos0][dVarPosO] += 1
            M[pos1][dVarPosO] -= 1
            M[pos2][dVarPosI] += 1
            M[pos3][dVarPosI] -= 1
            M[dVarPosI][pos2] += 1
            M[dVarPosI][pos3] -= 1
            M[dVarPosO][pos0] += denom * zoD
            M[dVarPosO][pos1] -= denom * zoD
            M[dVarPosO][dVarPosI] -= numer * zoD
            M[dVarPosO][dVarPosO] -= zoN * denom
        elif elmt.model == 'N':
            dVarPos = varIndex['I_o_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos2] += 1
            M[dVarPos][pos3] -= 1
        elif elmt.model == 'T':
            dVarPos = varIndex['I_o_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += value
            M[pos1][dVarPos] -= value
            M[pos2][dVarPos] += 1
            M[pos3][dVarPos] -= 1
            M[dVarPos][pos0] += value
            M[dVarPos][pos1] -= value
            M[dVarPos][pos2] += 1
            M[dVarPos][pos3] -= 1
        elif elmt.model == 'V':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            dVarPos = varIndex['I_' + elmt.refDes]
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
        elif elmt.model == 'VZ':
            (zoN, zoD) = getValues(elmt, 'zo', numeric, parDefs)
            pos1 = varIndex[elmt.nodes[1]]
            pos0 = varIndex[elmt.nodes[0]]
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += zoD
            M[dVarPos][pos1] -= zoD
            M[dVarPos][dVarPos] -= zoN
        elif elmt.model == 'W':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos2] += value
            M[pos0][pos3] -= value
            M[pos1][pos2] -= value
            M[pos1][pos3] += value
            M[pos2][pos0] -= value
            M[pos2][pos1] += value
            M[pos3][pos0] += value
            M[pos3][pos1] -= value
        elif elmt.model == 'K':
            refPos1 = varIndex['I_' + elmt.refs[0]]
            refPos0 = varIndex['I_' + elmt.refs[1]]
            ind0    = getValue(cir.elements[elmt.refs[0]].params['value'])
            ind1    = getValue(cir.elements[elmt.refs[1]].params['value'])
            value = getValue(elmt, 'value', numeric, parDefs)
            value = value * ini.Laplace * sqrt(ind0 * ind1)
    M = matrix(M)
    gndPos = varIndex['0']
    M.row_del(gndPos)
    M.col_del(gndPos)
    Vv = matrix(Vv)
    Vv.row_del(gndPos)
    if gainType == 'direct' or gainType == 'loopgain' or gainType == 'servo':
        cir.elements[lgRef].params['value'] = lgValue
    elif gainType == 'asymptotic':
        cir.elements[lgRef].model = lgRefModel
        cir.updateMdata()
    return (M, Vv)

def makeSrcVector(cir, parDefs, elid, value = 'id', numeric = True):
    """
    Creates the vector with independent variables with only the
    source with refdes 'elID'. The value will be equal to the
    refdes of that source.
    This can be used for determination of a transfer using Cramer's rule.
    Just substitute this vector in the detector col, calculate the transfer
    with Cramer's rule and divide the result by the refDes.
    It is an alternative for using cofactors.
    This method is used for determination of gain factors for noise sources
    and for DC variance sources.
    """
    varIndex = cir.varIndex
    dim = len(cir.varIndex.keys())
    Iv = [0 for i in range(dim)]
    if elid == 'all':
        elements = [cir.elements[key] for key in cir.elements.keys()]
    elif elid in cir.elements.keys():
        elements = [cir.elements[elid]]
    for elmt in elements:
        if value == 'id':
            val = sp.Symbol(elmt.refDes)
        elif value == 'value':
            val = getValue(elmt, 'value', numeric, parDefs)
        elif value == 'noise':
            val = getValue(elmt, 'noise', numeric, parDefs)
        elif value == 'dc':
            val = getValue(elmt, 'dc', numeric, parDefs)
        elif value == 'dcvar':
            val = getValue(elmt, 'dcvar', numeric, parDefs)
        if elmt.model == 'I':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            Iv[pos0] += val
            Iv[pos1] += -val
        elif elmt.model == 'V':
            dVarPos = varIndex['I_' + elmt.refDes]
            Iv[dVarPos] += val
    gndPos = varIndex['0']
    Iv = matrix(Iv)
    Iv.row_del(gndPos)
    return Iv

if __name__ == '__main__':
    ini.projectPath = ini.installPath + 'testProjects/PIVA/'
    ini.circuitPath = ini.projectPath + 'cir/'
    ini.htmlPath    = ini.projectPath + 'html/'
    ini.htmlIndex   = 'index.html'
    ini.htmlPages = []
    t1=time()
    LIB = makeLibraries()
    t2=time()
    fi = 'PIVA.cir'
    print "\nCheking:", fi
    myCir = checkCircuit(fi )
    t3=time()
    keys = myCir.elements.keys()
    for key in keys:
        el = myCir.elements[key]
        print '\nElement    :', key
        print 'Nodes      :', el.nodes
        print 'Refs       :', el.refs
        print 'Model      :', el.model
        print 'Params     :'
        for par in el.params.keys():
            print ' ', par, '=', el.params[par]
    
    print '\nCircuit parameter definitions:'
    for par in myCir.parDefs.keys():
        print ' ', par, '=', myCir.parDefs[par]          
    t4=time()
    for el in myCir.elements.keys():
        for par in  myCir.elements[el].params.keys():
            parNum = fullSubs(myCir.elements[el].params[par], myCir.parDefs)
            print el,'\t', par, sp.N(parNum, DISP)
    t5=time()
    (Iv, M, Vv) = makeMatrices(myCir, myCir.parDefs, False)
    t6=time()
    print M
    (Iv, M, Vv) = makeMatrices(myCir, myCir.parDefs, True)
    t7=time()
    #display.display(M)
    charPoly = M.determinant()
    t8=time()
    print charPoly
    print "\nmakeLibraries         : %fs."%(t2-t1)
    print "checkCircuit          : %fs."%(t3-t2)
    print "makeMatrices symbolic : %fs."%(t6-t3)
    print "makeMatrices numeric  : %fs."%(t7-t6)
    print "determinant()         : %fs."%(t8-t7)