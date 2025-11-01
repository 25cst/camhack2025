def uncapitalize_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Convert each line to lowercase
    lines = [line.lower() for line in lines]

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    file_path = input("Enter the path of the file to uncapitalize: ").strip()
    uncapitalize_file(file_path)
    print(f"All lines in '{file_path}' have been converted to lowercase.")