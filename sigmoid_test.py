import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def aproximation_sigmoid(x):
    #return 1/2 + x/4 - (x**3)/48 + (x**5)/480 - 17*(x**7)/80640 + 31*(x**9)/1451520 - 691*(x**11)/319334400
    return 1/2 + x/4 - (x**3)/48 + (x**5)/480 - 17*(x**7)/80640


def aproximation_sigmoid_2(x):
    return 1/2 + x/2 - (x**3)/6 + (x**5)/15 - 17*(x**7)/630

def aproximation_sigmoid_32(x):
    return 1/2 + 8*x - 2048*(x**3)/3 + 1048576*(x**5)/15 - 2281701376*(x**7)/315

def sig7_paper(x):
    return 0.5 - 1.734*x/8 + 4.19407*((x/8)**3) - 5.43402*((x/8)**5) + 2.50739*((x/8)**7)


x = 2
print(sigmoid(x))
print(sig7_paper(x))
print(aproximation_sigmoid(x))

