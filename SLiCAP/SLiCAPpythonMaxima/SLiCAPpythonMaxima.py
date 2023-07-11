#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with symbolic math functions executed by maxima CAS.

Imported by the module **SLiCAPplots.py**.
"""
from SLiCAP.SLiCAPlex import *

def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
  mustend = time() + timeout
  while time() < mustend:
    if somepredicate:
        return True
    sleep(period)
  return False

class maximaHandler():
    mut = Lock()
    active = False

    def __init__(self, port, host, maxima, timeout = 0.5):
        self.PORT = port
        self.HOST = host
        self.maxima = maxima
        self.timeout = timeout

    def __del__(self):
        self.active = False

    def runMaxima(self):
        os.system(self.maxima + ' -s ' + str(self.PORT))

    @start_new_thread
    def startMaxima(self):
        thread = Thread(target = self.runMaxima)
        thread.start()

        self.mut.acquire() # lock the mutex so the other functions can't grab the
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen(1)
            self.conn, self.addr = s.accept()
            self.conn.settimeout(self.timeout)
            # Release mutex such that other functions can grab the connection
            self.mut.release()
            self.active = True
            while(self.active):
                sleep(1)
            print("Shutting down Maxima CAS.")
        thread.join()

    def restartMaxima(self):
        self.active = False
        sleep(2)
        self.startMaxima()

    def getResponse(self):
        receive_data = ""
        while True:
            try:
                while True:
                    receive_data += self.conn.recv(4096).decode()
            except BaseException:
                pass
            if receive_data != "":
                break
        #print(receive_data.encode("utf-8"))
        return receive_data

    def parseMaxima(self, maxInstr):
        output = "ERROR"
        send_data = ''

        wait_until(self.active, 2)
        self.mut.acquire() # Lock mutex, wait untill available
        #print(maxInstr.encode("utf-8"))
        self.conn.sendall(maxInstr.encode("utf-8"))

        # Check if a question is present?
        while True:
            # Grab the response
            receive_data = self.getResponse()
            if "?" in receive_data:
                while len(send_data) == 0:
                    send_data = input(receive_data.strip() + '\n>> ')
                    receive_data = ""
                if send_data == ';' or send_data == '$':
                    send_data = 'quit();'
                if len(send_data) > 0 and send_data[-1] != ';' and send_data[-1] != '$':
                    send_data += ';'
                self.conn.sendall(send_data.encode())
                if send_data == 'quit();' or send_data == 'quit()$':
                    break
            else:
                try:
                    output = receive_data.replace("\n","").replace("\\", "").split('"')[1]
                    break
                except IndexError:
                    output = "ERROR"
                    print(receive_data)
                    print("""
Error in Maxima instruction!

Known causes:

- syntax error
- invalid answer to a question
- symbolic indices
- divide by zero
- determinant of a non-square matrix
""")
                    print("MAXIMA INSTRUCTION:")
                    print(maxInstr)
                    break
        self.mut.release()
        return output

    def maxEval(self, maxExpr):
        """
        Evaluates the expression 'maxExpr' with Maxima CAS and returns the result.

        :param maxExpr: Expression in Maxima format to be evaluated.
        :type maxExpr: str

        :return: String that can be converted into a sympy expression.
        :rtype: str

        Example:

        >>> maxEval("result:ilt(1/(s^2 + a^2), s, t);")
        'sin(a*t)/a'
        """

        #print(maxExpr)

        result = self.parseMaxima(maxExpr)
        return result

def maxLimit(expr, var, val, pm, numeric = True):
    """
    Calculates the limit of an expression for 'var' approaches 'val' from 'pm'.

    :param expr: Expression of which the limit must be evaluated.
    :type expr: sympy.Expr, str
    :param var: Variable that should approach the limit value.
    :type var: sympy.Symbol, str
    :param val: Limit value of the variable.
    :type val:  sympy.Symbol, str, sp.Expr, int, float
    :param pm: Direction: 'plus' or 'minus'
    :type pm: str
    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Calculated limit
    :rtype: sympy.Expr
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxExpr = 'string(%s(limit(' + str(expr) + ',' + str(var) + ',' + str(val) + ',' + pm +' )));'%(numeric)
    result = maxEval(maxExpr)
    try:
        result = sp.sympify(result)
    except BaseException:
        exc_type, value, exc_traceback = sys.exc_info()
        print('\n', value)
        result = sp.sympify("ERROR")
    return result

def maxIntegrate(expr, var, start = None, stop = None, numeric = True):
    """
    Calculates definite or indefinite integral of 'expr'.

    :param expr: Integrand
    :type expr: sympy.Expr

    :param var: Integration variable
    :type var: sympy.Symbol, str

    :param start: Lower limit of the integral.
    :type start: Bool, int float, sympy.Expr

    :param stop: Upper limit of the integral.
    :type stop: Bool, int float, sympy.Expr

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Integral
    :rtype: sympy.Expr
    """
    if numeric:
        numeric = 'bfloat'
        expr=sp.N(expr)
    else:
        numeric = ''
    maxExpr = "assume_pos:true$assume_pos_pred:symbolp$ratprint:false$stringdisp:true$"
    if start != None and stop != None:
        maxExpr += 'string(%s(integrate(%s, %s, %s, %s)));'%(numeric, str(expr), str(var), str(start), str(stop))
    else:
        maxExpr += 'string(%s(integrate(%s, %s)));'%(numeric, str(expr), str(var))
    result = maxEval(maxExpr)
    try:
        result = sp.sympify(result)
    except BaseException:
        exc_type, value, exc_traceback = sys.exc_info()
        print('\n', value)
        result = sp.sympify("ERROR")
    return result

def python2maxima(expr):
    """
    Converts a sympy expression into a Maxima expression.

    :param expr: sympy expression
    :type expr: sympy.Ex

    :return: maxima expression
    :rtype: str
    """
    expr = str(expr) + ' ' # Add a space for expressions ending with pi, e, E or I
    # Remove extra brackets in matrix
    expr = re.sub(r'Matrix\(\[\[(.*)\]\]\)', r'matrix([\1])', expr)
    # Replace exp(1): e or E with %e
    expr = re.sub(r'([+-/\*^\(])[eE]([\s\)+-/\*^])', r'\1%e\2', expr)
    # Replace pi with %pi
    expr = re.sub(r'([+-/\*^\(])pi([\s\)+-/\*^])', r'\1%pi\2', expr)
    # Replace 1j or I with %i
    expr = re.sub(r'([0-9])j', r'\1*%i', expr)
    expr = re.sub(r'([+-/\*^\(\s])I([\s\)+-/\*^])', r'\1%i\2', expr)
    # Replace the sign() function with the signum() function-
    # This must be done recursively because of overlapping patterns
    new_expr = sign2signum(expr)
    while new_expr != expr:
        expr = new_expr
        new_expr = sign2signum(new_expr)
    return expr

def sign2signum(expr):
    """
    Performs a non-overlapping replacement of sign(expr) with signum(expr)

    :param expr: text string
    :type expr: str

    :return: expr
    :rtype: str
    """
    return re.sub(r'sign(\(.*\))', r'signum\1', expr)

def signum2sign(expr):
    """
    Performs a non-overlapping replacement of signum(expr) with sign(expr)

    :param expr: text string
    :type expr: str

    :return: expr
    :rtype: str
    """
    return re.sub(r'signum(\(.*\))', r'sign\1', expr)

def maxima2python(expr):
    """
    Converts a maxima expression into string that can be converted into a sympy expression.

    :param expr: maxima expression
    :type expr: str

    :return: sympy compatible expression
    :rtype: str
    """
    # Convert big float notation '12345b+123' to float notation '12345e+123':
    expr = re.sub(r'(([+-]?)(\d+)(\.?)(\d*))b(([+-]?)(\d+))', r'\1e\6', expr)
    # Convert complex number notation:
    expr = re.sub(r'%i','1j', expr)
    # Convert 'e' notation:
    expr = re.sub(r'%e','exp(1)', expr)
    # Convert 'pi' notation:
    expr = re.sub(r'%pi','pi', expr)
    # Convert Maxima matrix to sympy matrix:
    expr = re.sub(r'matrix\(\[(.*)\]\)', r'Matrix([[\1]])', expr)
    new_expr = signum2sign(expr)
    while new_expr != expr:
        expr = new_expr
        new_expr = signum2sign(new_expr)
    return expr

def maxEval(maxExpr):
    """
    Evaluates the expression 'maxExpr' with Maxima CAS and returns the result.

    :param maxExpr: Expression in Maxima format to be evaluated.
    :type maxExpr: str

    :return: String that can be converted into a sympy expression.
    :rtype: str

    Example:

    >>> maxEval("result:ilt(1/(s^2 + a^2), s, t);")
    'sin(a*t)/a'
    """
    if ini.assumePosMaxVars == True:
        maxExpr = "assume_pos:true$" + maxExpr
    else:
        maxExpr = "assume_pos:false$" + maxExpr
    if ini.socket == True:
        result = maxima2python(ini.maximaHandler.maxEval(maxExpr))
        if result == "ERROR":
            restartMaxima()
    else:
        preambule = 'load("' + ini.installPath + 'SLiCAPpythonMaxima/SLiCAP_python.mac")$'
        maxExpr = preambule + maxExpr
        output = "ERROR"
        try:
            output = subprocess.run([ini.maxima, '--very-quiet', '-batch-string', maxExpr], capture_output=True, timeout=ini.MaximaTimeOut, text=True)
            result = output.stdout.split('"')[-2] # The quoted string is the result of the calculation
            result = result.replace('\\\n', '')   # Remove the maxima newline characters from this result
            result = maxima2python(result)        # Convert the maxima output into a string that can be 'sympified' by python
        except BaseException:
            exc_type, value, exc_traceback = sys.exc_info()
            print('\n', value)
            print("""\nMaxima CAS calculation failed or timed out. A time-out occurs if Maxima requires additional input, or if Maxima CAS requires more time.
The latter case can be solved by increasing the time limit using the command: 'ini.MaximaTimeOut=nnn', where nnn is the number of seconds.\n""")
            result = output
            result = maxima2python(result)
    return result

def startMaxima():
    ini.maximaHandler = maximaHandler(port=ini.PORT, host=ini.HOST, maxima=ini.maxima, timeout=0.05)
    ini.maximaHandler.startMaxima()
    checkMaxima()

def restartMaxima():
    if ini.maximaHandler != None:
        ini.maximaHandler.restartMaxima()
        checkMaxima()
    else:
        startMaxima()

def checkMaxima():
    result = ini.maximaHandler.maxEval('stringdisp:true$string(1-1);')
    try:
        if result == '0':
            result = ini.maximaHandler.maxEval('load("' + ini.installPath + 'SLiCAPpythonMaxima/SLiCAP_python.mac")$M:matrix([a,b],[c,d])$string(det(M));')
            if result == 'a*d-b*c':
                print("Maxima CAS client is active and functions have been uploaded.")
            else:
                ini.socket = False
                print("Maxima CAS client is NOT active, switched to subprocess communication.")
        else:
            ini.socket = False
            print("Maxima CAS client is NOT active, switched to subprocess communication.")
    except BaseException:
        exc_type, value, exc_traceback = sys.exc_info()
        print('\n', value)
        print("Maxima CAS client is NOT active, switched to subprocess communication.")
        ini.socket = False

if __name__ == '__main__':
    ini.socket = True
    startMaxima()
    # ini.socket should not need to be global, classes are nice
    def test():
        x = sp.Symbol('x')
        y = (1+2*x+3*x**2)/(x*sp.exp(10)+2/sp.pi)
        for i in range(100):
            #print(maxIntegrate(y, x, numeric=False))
            maxIntegrate(y, x, numeric=False)

    #import cProfile
    #cProfile.run("test()")
    test()
    ## Restart maxima server example, uncomment next lines otherwise
    print(maxEval('stringdisp:true$string(ilt(1/(s^2+a),s,t));'))
    restartMaxima()
    # This generates an error which is handled properly
    print(maxEval('M:matrix([0, 0, 1, 0, 0, 0], [0, 0, 0, -A_v, 1, A_v], [1, 0, 1/R_s, -1/R_s, 0, 0], [0, 0, -1/R_s, 1/R_s, 0, 0], [0, 1, 0, 0, 1/R_ell + 1/R_a, -1/R_a])$ newdet(M);'))
    # This generates an error with a message and automatic recovery
    print(maxEval('M[a,1];'))
    print(maxEval('load("/home/anton/.local/lib/python3.8/site-packages/SLiCAP/SLiCAPpythonMaxima/SLiCAP_python.mac")$M : matrix([0, 0, 1, 0, 0, 0], [0, 0, 0, -A_v, 1, A_v], [1, 0, 1/R_s, -1/R_s, 0, 0], [0, 0, -1/R_s, 1/R_s, 0, 0], [0, 1, 0, 0, 1/R_ell + 1/R_a, -1/R_a], [0, 0, 0, 0, -1/R_a, 1/R_b + 1/R_a]) $detCols:[5,0]$Iv: matrix([1, 0, 0, 0, 0, 0]) $string(doLaplace(M,detCols,Iv));'))
    # This generates an error with a message and recovers after input.
    print(maxEval('load("/home/anton/.local/lib/python3.8/site-packages/SLiCAP/SLiCAPpythonMaxima/SLiCAP_python.mac")$M : matrix([0, 0, 1, 0, 0, 0], [0, 0, 0, -A_v, 1, A_v], [1, 0, 1/R_s, -1/R_s, 0, 0], [0, 0, -1/R_s, 1/R_s, 0, 0], [0, 1, 0, 0, 1/R_ell + 1/R_a, -1/R_a], [0, 0, 0, 0, -1/R_a, 1/R_b + 1/R_a]) $detCols:[V_alpha,0]$Iv: matrix([1, 0, 0, 0, 0, 0]) $string(doLaplace(M,detCols,Iv));'))
    # Recovered after error
    print(maxEval('stringdisp:true$string(ilt(1/(s^2+a),s,t));'))
    ini.maximaHandler.__del__()
    sleep(3)
    print("Nice")
