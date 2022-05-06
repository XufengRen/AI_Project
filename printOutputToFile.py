def printOutputToFile(path, output):
    f = open(path, "a")
    f.write(output)
    f.close
printOutputToFile("output.txt", "Hello World!")
