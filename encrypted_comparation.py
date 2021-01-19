from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image
import math

'''
def read_input_image():
    data = [x/128 for x in range(-dim//2, dim//2, 1)]
    #data = [x/129 for x in range(1, dim+1)]
    lower, upper = 1/2, 3/4
    l_norm = [lower + (upper - lower) * x for x in data]


    return {'data': l_norm}
'''


def read_input_image():
    data = [x/256 for x in range(-dim//2, dim//2, 1)]
    return {'data': data}

def non_taylor_comp(input):
    ans = []
    for x in input:
        tmp = x**2
        tmp = math.sqrt(tmp)
        ans.append(tmp)

    return {'data': ans}

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
        ans = base**exp_int
    log = logarithm(base, limit)
    tmp = exponential_expansion(exp_frac*log, limit)
    ans = ans * tmp
    return ans

def abs(data):
    data = data ** 2
    data = exponentiation(data, 1 / 2, 4)
    return data

dim = 256
encrypted_comparation = EvaProgram('encrypted_comparation', vec_size=dim)
with encrypted_comparation:
    data = Input('data')
    data = abs(data)
    Output('data', data)



encrypted_comparation.set_input_scales(40)
encrypted_comparation.set_output_ranges(30)

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_comparation)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)

non_taylor = non_taylor_comp(input['data'])

print(input['data'])
print(non_taylor['data'])
print(outputs['data'])
print(reference['data'])


print('MSE', valuation_mse(outputs, non_taylor))








