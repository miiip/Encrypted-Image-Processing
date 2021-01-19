from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image

def read_input_image():
    image = Image.open('baboon.png').convert('L')
    image.show()
    image_data = [x / 255.0 for x in list(image.getdata())]
    return {'image': image_data}

def write_output_image(outputs, tag):
    enc_result_image = Image.new('L', (w, h))
    enc_result_image.putdata([x * 255.0 for x in outputs['image'][0:h*w]])
    enc_result_image.save(f'baboon_{tag}.png', "PNG")

def rotate(l, n):
    return l[n:] + l[:n]

def convolution(image, width, filter):
    for i in range(len(filter)):
        for j in range(len(filter[0])):
            rotated = image << i * width + j
            partial = rotated * filter[i][j]
            if i == 0 and j == 0:
                convolved = partial
            else:
                convolved += partial
    return convolved

def generate_mean_filter(k):
    filter = [[0] * k] * k
    for i in range(k):
        for j in range(k):
            filter[i][j] = 1/(k**2)
    return filter



h = 64
w = 64
filter = generate_mean_filter(3)

apply_filter = EvaProgram('apply_filter', vec_size=h*w)
with apply_filter:
    image = Input('image')
    conv = convolution(image, w, filter)
    Output('image', conv)

apply_filter.set_input_scales(25)
apply_filter.set_output_ranges(10)

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(apply_filter)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
write_output_image(outputs, f'{compiled.name}_encrypted')
reference = evaluate(compiled, input)
write_output_image(reference, f'{compiled.name}_reference')
print('MSE', valuation_mse(outputs, reference))








