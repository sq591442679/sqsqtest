if __name__ == '__main__':
    with open("/home/sqsq/Desktop/test.cc", "r+") as f:
        lines = f.readlines()

        print(lines[47])
        lines[47] = "#define SQSQ_HOP                               4\n"

        f.seek(0)
        f.writelines(lines)
    f.close()
