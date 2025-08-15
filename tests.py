from functions.get_files_info import get_files_info


res = get_files_info("calculator", ".")
print("Result for current directory:")
print(res)

res = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
print(res)

res = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(res)

res = get_files_info("calculator", "../")
print("Result for '../' directory:")
print(res)