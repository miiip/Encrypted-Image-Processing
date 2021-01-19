from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
import matplotlib.pyplot as plt
from PIL import Image
import math


def read_input_image():
    data = [x/dim for x in range(dim)]
    delta = 0.24
    data = [x * delta - 0.12 for x in data]
    constant1 = [1.9142]*dim
    constant2 = [1]*dim
    constant3 = [0.5]*dim
    return {'data': data, 'constant1': constant1, 'constant2': constant2, 'constant3': constant3}

def aprox_heaviside(x, constant1, constant2, constant3, r):
    for i in range(r):
        tmp = x * (constant1 - (x**2))
        x = tmp
    tmp = tmp - constant2
    tmp = tmp * constant3
    return tmp


def non_aprox_heaviside(input):
    ans = []
    for x in input:
        if x < 0:
            ans.append(-1)
        if x == 0:
            ans.append(0)
        if x > 0:
            ans.append(1)
    return {'data': ans}

def mae(x, y):
    sum = 0
    for i in range(len(x)):
        sum = sum + abs(x[i]-y[i])
    sum = sum / len(x)
    return sum

dim = 256
encrypted_comparasion_heaviside = EvaProgram('encrypted_comparasion_heaviside', vec_size=dim)
with encrypted_comparasion_heaviside:
    data = Input('data')
    constant1 = Input('constant1')
    constant2 = Input('constant2')
    constant3 = Input('constant3')

    r = 6
    data = aprox_heaviside(data, constant1, constant2, constant3, r)
    Output('data', data)



encrypted_comparasion_heaviside.set_input_scales(40)
encrypted_comparasion_heaviside.set_output_ranges(30)



input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_comparasion_heaviside)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)
non_aprox_heavi_output = non_aprox_heaviside(input['data'])
print(input['data'])
print(outputs['data'])
print(reference['data'])
print('MSE', valuation_mse(outputs, reference))
print('MSE', valuation_mse(outputs, non_aprox_heavi_output))

plt.plot(input['data'], outputs['data'])
plt.title('Input vs semn aproximativ')
plt.show()

plt.plot(input['data'], non_aprox_heavi_output['data'])
plt.title('Input vs semn exact')
plt.show()







