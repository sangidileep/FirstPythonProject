menu = ''
while menu != '1' or menu !='2':
    menu = input("Would you like to save a new password or view your old ones?"
                 "\n1. Input new password"
                 "\n2. view passwords"
                 "\n3. Exit"
                 "\n  Enter Number here:")

    if menu =='1':
        SoftwareName = input("Enter the name of the Software or Website: ")
        username = input("Enter  your username for this Software or Website: ")
        password = input("Enter your password for this Software or Webside:  ")
        file = open("SecutedData.txt", 'a')
        file.write('\nSoftwareName: '+SoftwareName +"  Id: "+ username +'  Password: '+ password)
        file.close()

    if menu =='2':
        file = open("SecutedData.txt", 'r')
        # print('soft or web \t username \t password','\n',file.read())
        for i in file:
            data = i.split(" ")
            print(data[3:])
            # print(data[0] + '\t' + data[2] + '\t' + data[3])
    if menu =='3':
        exit()

