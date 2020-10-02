def menu():
    region_name = "default"
    while True:
        print ('Choose from the following regions: ')
        print ('1. us-east-1')
        print ('2. us-east-2')
        print ('3. us-west-1')
        print ('4. us-west-2')
        print ('5. ca-central-1')
        region_num = input("Enter a number from [1-5]: ")
        if not 1 <= int(region_num) <= 5:
            print ('Please enter a valid number!')
        else:
            if region_num == '1':
                region_name = "us-east-1"
            elif region_num == '2':
                region_name = "us-east-2"
            elif region_num == '3':
                region_name = "us-west-1"
            elif region_num == '4':
                region_name = "us-west-2"
            elif region_num == '5':
                region_name = "ca-central-1"
            break

    key_name = input("Enter your key name: ")
    github_repo = input("Enter your github repository url: ")    
    
    return region_name, key_name, github_repo
    

def main():
    inputs = menu()
    print (inputs[0], inputs[1], inputs[2])

if __name__ == "__main__":
    main()


