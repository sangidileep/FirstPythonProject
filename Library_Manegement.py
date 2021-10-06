class Library:
    def __init__(self, list, name):
        self.bookslist = list
        self.name = name
        self.lendDict =  {}
        
    def displayBook(self):
        print("We have followings books in our library: {self.name} ")
        for book in self.bookslist:
            print(book)
            
    def lendBook(self, user, book):
        if book not in self.lendDict.keys():
            self.lendDict.update({book : user})
            print("Lender-book database has been updated. You can take the book now")
        else:
            print(f"Book is already being used by {self.lendDict[book]}")
            
            
    def addBook(self, book):
        self.bookslist.append(book)
        print("book has been added to the book list")
        
    def returnBook(self,book):
        self.bookslist.remove(book)

if __name__ == '__main__':
    harry = Library({'Python', 'Rich dad poor dad', 'Harry potter', 'C++ Basics', 'Algorithms by CLRS'}, "Code with shubham")
    
    while True:
        print("Welcome to the {harry.name} library. Enter your choice to continue")
        print('1. Display Books')
        print('2. Lend a Book')
        print('3. Add a Book')
        print('4. Return a Book')
        
        user_choice =int(input())
        
        if user_choice ==1:
            harry.displayBook()
            
        elif user_choice ==2:
            book = input("Enter the name of the book you want to lend: ")
            user = input("Enter your name : ")
            harry.lendBook(user, book)
            
        elif user_choice == 3:
            book = input("Enter the name of the book you want to add: ")
            harry.addBook(book)
            
            
        elif user_choice == 4:
            book = input("Enter the name of the book you want to return: ")
            harry.returnBook(book)
            
            
        else:
            print("Not a valid option")
            
        print("Press q to quit and c to continue")
        user_choice2 =""
        while (user_choice2!="c" and user_choice2!="q"):
            user_choice2 = input()
        if user_choice2 == "q":
            exit()
            
        if user_choice2 == "c":
            continue

            
        
            
            
        
