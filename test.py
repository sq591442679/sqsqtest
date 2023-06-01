if __name__ == '__main__':
    read_file = open("/home/sqsq/Desktop/test.cc", "r")
    lines = read_file.readlines()
    print(lines[47])
    lines[47] = "#define SQSQ_HOP                               114541\n"
    read_file.close()

    write_file = open("/home/sqsq/Desktop/test.cc", "w")
    write_file.writelines(lines)
    write_file.close()
