from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image
import math

def read_input_image():
    image = Image.open('baboon.png').convert('L')
    image_data = [x / 255.0 for x in list(image.getdata())]

    return {'image': image_data}

def write_output_image(outputs, tag):
    enc_result_image = Image.new('L', (w, h))
    enc_result_image.putdata([x * 255.0 for x in outputs['image'][0:h * w]])
    enc_result_image.save(f'baboon_{tag}.png', "PNG")

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

h = 64
w = 64
gamma = 1.5
encrypted_gamma_gray = EvaProgram('encrypted_gamma_gray', vec_size=h*w)
with encrypted_gamma_gray:
    image = Input('image')
    image = exponentiation(image, 1/gamma, 20)
    Output('image', image)



encrypted_gamma_gray.set_input_scales(20)
encrypted_gamma_gray.set_output_ranges(30)

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_gamma_gray)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)
write_output_image(outputs, f'{compiled.name}_encrypted')
reference = evaluate(compiled, input)
write_output_image(reference, f'{compiled.name}_reference')
print('MSE', valuation_mse(outputs, reference))








