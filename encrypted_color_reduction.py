from eva import EvaProgram, Input, Output, evaluate
from eva.ckks import CKKSCompiler
from eva.seal import generate_keys
from eva.metric import valuation_mse
from PIL import Image
import math

def read_input_image():
    image = Image.open('baboon.png')
    image_data_r = [x[0] / 255.0 for x in list(image.getdata())]
    image_data_g = [x[1] / 255.0 for x in list(image.getdata())]
    image_data_b = [x[2] / 255.0 for x in list(image.getdata())]

    return {'image_r': image_data_r, 'image_g': image_data_g, 'image_b': image_data_b}

def write_output_image(outputs, tag):
    enc_result_image = Image.new('RGB', (w, h))
    enc_result_image.putdata([(int(outputs['image_r'][0:h*w][i] * 255.0),
                               int(outputs['image_g'][0:h*w][i] * 255.0),
                               int(outputs['image_b'][0:h*w][i] * 255.0)) for i in range(len(outputs['image_r'][0:h*w]))])

    enc_result_image.save(f'baboon_{tag}.png', "PNG")



h = 64
w = 64
encrypted_color_reduction = EvaProgram('encrypted_color_reduction', vec_size=h*w)
with encrypted_color_reduction:
    image1 = Input('image_r')
    image2 = Input('image_g')
    image3 = Input('image_b')
    Output('image_r', image1)
    Output('image_g', image2)
    Output('image_b', image3)


encrypted_color_reduction.set_input_scales(20)
encrypted_color_reduction.set_output_ranges(30)

input = read_input_image()

compiler = CKKSCompiler()
compiled, params, signature = compiler.compile(encrypted_color_reduction)
public_ctx, secret_ctx = generate_keys(params)
enc_inputs = public_ctx.encrypt(input, signature)
enc_outputs = public_ctx.execute(compiled, enc_inputs)
outputs = secret_ctx.decrypt(enc_outputs, signature)
reference = evaluate(compiled, input)
write_output_image(outputs, f'{compiled.name}_encrypted')
reference = evaluate(compiled, input)
write_output_image(reference, f'{compiled.name}_reference')
print('MSE', valuation_mse(outputs, reference))








