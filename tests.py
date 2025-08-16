# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


# res = get_files_info("calculator", ".")
# print("Result for current directory:")
# print(res)

# res = get_files_info("calculator", "pkg")
# print("Result for 'pkg' directory:")
# print(res)

# res = get_files_info("calculator", "/bin")
# print("Result for '/bin' directory:")
# print(res)

# res = get_files_info("calculator", "../")
# print("Result for '../' directory:")
# print(res)


# res = get_file_content("calculator", "lorem.txt")
# print(res)
# res = get_file_content("calculator", "main.py")
# print(res)

# res = get_file_content("calculator", "pkg/calculator.py")
# print(res)

# res = get_file_content("calculator", "/bin/cat")
# print(res)

# res = get_file_content("calculator", "pkg/does_not_exist.py")
# print(res)

# res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(res)

# res = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(res)

# res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(res)


res = run_python_file("calculator", "main.py")
print(res)
res = run_python_file("calculator", "main.py", ["3 + 5"])
print(res)
res = run_python_file("calculator", "tests.py")
print(res)
res = run_python_file("calculator", "../main.py")
print(res)
res = run_python_file("calculator", "nonexistent.py")
print(res)