import torch

print(torch.__version__)         # Ver versión de PyTorch
print(torch.cuda.is_available()) # Debe devolver True
print(torch.cuda.get_device_name(0)) # Nombre de tu GPU
