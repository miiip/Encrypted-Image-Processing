from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image
import math


def read_input_image():
    data = [x/dim for x in range(-dim//2, dim//2, 1)]
    constant1 = [0.00001]*dim
    one = [1] * dim
    return {'data': data, 'constant1': constant1, 'one': one}





dim = 256
encrypted_abs = EvaProgram('encrypted_abs', vec_size=dim)
with encrypted_abs:
    data = Input('data')
    constant1 = Input('constant1')
    one = Input('one')
    sgn = data * constant1
    sgn = sgn + 1
    
    Output('data', data)



encrypted_abs.set_input_scales(40)
encrypted_abs.set_output_ranges(30)

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_abs)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)



print(input['data'])
print(outputs['data'])
print(reference['data'])


print('MSE', valuation_mse(outputs, reference))
print('MSE', valuation_mse(outputs, non_aprox_heavi_output))









