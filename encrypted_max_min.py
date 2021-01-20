from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from random import random
import matplotlib.pyplot as plt
from PIL import Image
import math


def read_input_image():
    x = []
    y = []
    for i in range(dim):
        x.append(random())
        y.append(random())
    delta = 0.24
    x = [tmp * delta - 0.12 for tmp in x]
    y = [tmp * delta - 0.12 for tmp in y]
    constant1 = [1.9142]*dim
    constant2 = [1]*dim
    constant3 = [0.5]*dim
    return {'x': x, 'y': y, 'constant1': constant1, 'constant2': constant2, 'constant3': constant3}

def aprox_heaviside(x, constant1, constant2, constant3, r):
    for i in range(r):
        tmp = x * (constant1 - (x**2))
        x = tmp
    tmp = tmp - constant2
    tmp = tmp * constant3
    return tmp

def max(x, y, constant1, constant2, constant3, r) :
    sgn = aprox_heaviside(x-y, constant1, constant2, constant3, r)
    return constant3*(x+y+sgn*(x-y))

dim = 256
encrypted_comparasion_heaviside = EvaProgram('encrypted_comparasion_heaviside', vec_size=dim)
with encrypted_comparasion_heaviside:
    x = Input('x')
    y = Input('y')
    constant1 = Input('constant1')
    constant2 = Input('constant2')
    constant3 = Input('constant3')

    r = 5
    data = max(x, y, constant1, constant2, constant3, r)
    Output('data', data)



encrypted_comparasion_heaviside.set_input_scales(40)
encrypted_comparasion_heaviside.set_output_ranges(30)

def non_aprox_max(x, y):
    z = []
    for i in range(len(x)):
        if x[i] > y[i]:
            z.append(x[i])
        else:
            z.append(y[i])
    return {'data': z}

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_comparasion_heaviside)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)
non_aprox = non_aprox_max(input['x'], input['y'])
print(input['x'])
print(input['y'])
print(outputs['data'])
print('MSE', valuation_mse(outputs, reference))
print('MSE', valuation_mse(outputs, non_aprox))

plt.plot(range(dim), valuation_mse(outputs, non_aprox))
plt.title('MSE')
plt.show()










