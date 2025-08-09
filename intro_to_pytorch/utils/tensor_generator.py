import torch


def tensor_gen(shape, dtype = torch.float32):
    # shape_input = input("Enter the shape of the tensor(comma-separated):")
    # shape = tuple(map(int, shape_input.split(',')))

    req_tensor =  torch.rand(shape, dtype= dtype)
    return req_tensor

# tensor1 = tensor_gen((4,5))
# print(tensor1)

def one_hot_gen(batch_size, num_classes, dtype = torch.float32):
    class_indices = torch.randint(low = 0, high= num_classes, size = (batch_size,))
    one_hot_target = torch.nn.functional.one_hot(class_indices, num_classes= num_classes).to(dtype)
    return one_hot_target