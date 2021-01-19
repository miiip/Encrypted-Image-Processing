from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image
import matplotlib.pyplot as plt

def read_input_image():
    image1 = Image.open('baboon.png').convert('L')
    image_data1 = [x / 255.0 for x in list(image1.getdata())]
    image2 = Image.open('lena.png').convert('L')
    image_data2 = [x / 255.0 for x in list(image2.getdata())]
    return {'image1': image_data1, 'image2': image_data2}

h = 64
w = 64

encrypted_mse = EvaProgram('encrypted_mse', vec_size=h*w)
with encrypted_mse:
    image1 = Input('image1')
    image2 = Input('image2')
    mse = image1-image2
    mse = mse**2
    mse = (1/(h*w))*mse
    Output('mse', mse)

'''
scales_results = []
scales = []
for scale in range(5, 200, 5):
    scales.append(scale)
    encrypted_mse.set_input_scales(scale)
    encrypted_mse.set_output_ranges(30)
    input = read_input_image()
    compiler = CKKSCompiler()
    compiled, params, signature = compiler.compile(encrypted_mse)
    public_ctx, secret_ctx = generate_keys(params)
    enc_inputs = public_ctx.encrypt(input, signature)
    enc_outputs = public_ctx.execute(compiled, enc_inputs)
    outputs = secret_ctx.decrypt(enc_outputs, signature)
    reference = evaluate(compiled, input)
    dif = abs(sum(outputs['mse'])-sum(reference['mse']))
    scales_results.append(dif)
plt.scatter(scales, scales_results)
plt.show()
'''

ranges_results = []
ranges = []
for range in range(5, 500, 2):
    ranges.append(range)
    encrypted_mse.set_input_scales(20)
    encrypted_mse.set_output_ranges(range)
    input = read_input_image()
    compiler = CKKSCompiler()
    compiled, params, signature = compiler.compile(encrypted_mse)
    public_ctx, secret_ctx = generate_keys(params)
    enc_inputs = public_ctx.encrypt(input, signature)
    enc_outputs = public_ctx.execute(compiled, enc_inputs)
    outputs = secret_ctx.decrypt(enc_outputs, signature)
    reference = evaluate(compiled, input)
    dif = abs(sum(outputs['mse'])-sum(reference['mse']))
    ranges_results.append(dif)
plt.plot(ranges, ranges_results)
plt.show()









