from cryptography.hazmat.primitives.serialization import load_pem_parameters
from cryptography.hazmat.backends import default_backend
import pandas as pd 

# with open("dhparams.pem", "rb") as file:
#     pem_data = file.read()
# # Load Diffie-Hellman parameters
# dh_parameters = load_pem_parameters(pem_data, backend=default_backend())
# # Lấy số nguyên p, g
# p = dh_parameters.parameter_numbers().p
# g = dh_parameters.parameter_numbers().g
# print("p =", p.__sizeof__())
# print("g =", g)


# Đọc file PEM
# result = []
# for i in range(100):
#     with open(f"dhparams{i}.pem", "rb") as file:
#         pem_data = file.read()

#     # Load Diffie-Hellman parameters
#     dh_parameters = load_pem_parameters(pem_data, backend=default_backend())

#     # Lấy số nguyên p, g
#     p = dh_parameters.parameter_numbers().p
#     g = dh_parameters.parameter_numbers().g
#     result.append([p,g])

#     # print("p =", p)
#     # print("g =", g)
#     # print(p.__sizeof__())
#     # if g != 2:
#     #     print("g not equal 2!!!")
#     #     break

# df = pd.DataFrame(result, dtype = object, columns = ["q","g"])
# df.to_csv("dfparam.csv")
a = pd.read_csv("dfparam.csv")
qs = a['q']
print(int(qs[0]))