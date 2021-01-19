from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image
import math

def read_input_image():
    data = [x for x in range(dim)]

    return {'data': data}



def exponential_expansion(x, limit):
    sum = 0
    prod = 1
    fact = 1
    for i in range(limit):
        sum = sum + prod * (1/fact)
        prod = prod * x
        fact = fact * (i + 1)
    return sum

def logarithm(x, limit):
    a = 0.5
    sum = math.log(a)
    prod = 1
    pow = 1
    for i in range(1, limit):
        prod = prod * (x - a)
        pow = pow * a
        if i%2 == 1:
            sum = sum + prod * (1/(i * pow))
        else:
            sum = sum - prod * (1/(i * pow))
    return sum

def exponentiation(base, exp, limit):
    exp_int = int(exp)
    exp_frac = exp - exp_int
    if exp_int == 0:
        ans = 1
    else:
        ans = base ** exp_int
    log = logarithm(base, limit)
    tmp = exponential_expansion(exp_frac*log, limit)
    ans = ans * tmp
    return ans

def clear_exp(data, exp):
    data = [x**exp for x in data]
    return {'data': data}

def exp_int(base, exp):
    return base**exp

dim = 256
encrypted_exponentiation = EvaProgram('encrypted_exponentiation', vec_size=dim)
with encrypted_exponentiation:
    data = Input('data')
    data = exp_int(data, 78)

    Output('data', data)


encrypted_exponentiation.set_input_scales(80)
encrypted_exponentiation.set_output_ranges(40)

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_exponentiation)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)
print(outputs['data'])
print(reference['data'])
print('MSE', valuation_mse(outputs, reference))









