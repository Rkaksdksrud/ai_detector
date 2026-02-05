import torch

x = torch.randn(1000, 1000).cuda()
y = torch.mm(x, x)
print(y.shape)