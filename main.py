import pandas as pd
import os

def loginOption():
    print('\n                                                       __________________________________________')
    print("                                                      |____________ Online Shop 0.10 ____________|")
    print("                                                      |  1. Daftar Akun                          |")
    print("                                                      |  2. Login                                |")
    print("                                                      |  3. Exit                                 |")
    print('                                                      |__________________________________________|')
            
def mainMenu():
    print('\n                                                       __________________________________________')
    print("                                                      |_______________ Menu Utama _______________|")
    print("                                                      |  1. Add Product (Admin Only)             |")
    print("                                                      |  2. Top Up                               |")
    print("                                                      |  3. Buy Product                          |")
    print("                                                      |  4. Add to Favorites                     |")
    print("                                                      |  5. View Purchase History                |")
    print("                                                      |  6. View Favorites                       |")
    print("                                                      |  7. Check Balance                        |")
    print("                                                      |  8. Exit                                 |")
    print('                                                      |__________________________________________|')

def bubble_sort_products(products):
        n = len(products)
        for i in range(n):
            for j in range(0, n-i-1):
                if products.iloc[j]['price'] > products.iloc[j+1]['price']:
                    products.iloc[j], products.iloc[j+1] = products.iloc[j+1].copy(), products.iloc[j].copy()
        return products

def displayProducts():
    if os.path.exists('product.csv'):
        df = pd.read_csv('product.csv')
        if not df.empty:
            sorted_df = bubble_sort_products(df.copy())
            
            print("\nDaftar Produk yang Tersedia (Diurutkan dari harga terendah):")
            print("---------------------------------------------------------------------------------------------------")
            for index, row in sorted_df.iterrows():
                print(f"  Nama: {row['name']}, Harga: Rp.{row['price']:,}, Kategori: {row['category']}")
                print("---------------------------------------------------------------------------------------------------")
        else:
            print("\nBelum ada produk yang tersedia\n")
    else:
        print("\nBelum ada produk yang tersedia\n")
    
class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.balance = self.load_balance()
        self.favorite = []
        self.history = self.load_history()

    def load_balance(self):
        if os.path.exists('user_balance.csv'):
            df = pd.read_csv('user_balance.csv')
            user_balance = df[df['username'] == self.name]
            if not user_balance.empty:
                return user_balance['balance'].values[0]
        return 0

    def save_balance(self):
        if os.path.exists('user_balance.csv'):
            df = pd.read_csv('user_balance.csv')
            df.loc[df['username'] == self.name, 'balance'] = self.balance
        else:
            df = pd.DataFrame({'username': [self.name], 'balance': [self.balance]})
        df.to_csv('user_balance.csv', index=False)

    def load_history(self):
        if os.path.exists('purchase_history.csv'):
            df = pd.read_csv('purchase_history.csv')
            user_history = df[df['username'] == self.name]
            if not user_history.empty:
                return user_history.to_dict('records')
        return []

    def save_history(self, product_name, price, category):
        new_record = pd.DataFrame({
            'username': [self.name],
            'name': [product_name],
            'price': [price],
            'category': [category]
        })
        
        if os.path.exists('purchase_history.csv'):
            existing_history = pd.read_csv('purchase_history.csv')
            updated_history = pd.concat([existing_history, new_record], ignore_index=True)
        else:
            updated_history = new_record
            
        updated_history.to_csv('purchase_history.csv', index=False)
        self.history = self.load_history()
        
class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
        
class OnlineShop:
    def __init__(self):
        self.users = {}
        self.currentUser = None
        self.csvFile = 'product.csv'
        
        if not os.path.isfile(self.csvFile):
            df = pd.DataFrame(columns=['name', 'price', 'category'])
            df.to_csv(self.csvFile, index=False)

        # Create user_balance.csv if it doesn't exist
        if not os.path.exists('user_balance.csv'):
            df = pd.DataFrame(columns=['username', 'balance'])
            df.to_csv('user_balance.csv', index=False)
            
        # Create purchase_history.csv if it doesn't exist
        if not os.path.exists('purchase_history.csv'):
            df = pd.DataFrame(columns=['username', 'name', 'price', 'category'])
            df.to_csv('purchase_history.csv', index=False)
            
    def register(self, username, password):
        if not os.path.exists('user.txt'):
            with open('user.txt', 'w') as file:
                file.write('user,password\n')
        
        with open('user.txt', 'r') as file:
            for line in file:
                if line.strip().split(',')[0] == username:
                    print("Username telah digunakan")
                    return
                
        with open('user.txt', 'a') as file:
            file.write(f'{username},{password}\n')

        # Initialize user balance
        df = pd.read_csv('user_balance.csv')
        new_user = pd.DataFrame({'username': [username], 'balance': [0]})
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv('user_balance.csv', index=False)
        
        print("Pendaftaran berhasil!")

    def login(self, username, password):
        if username == 'admin' and password == 'admin123':
            print('\nBerhasil login sebagai Admin!')
            self.currentUser = User(username, password)
            return True

        with open('user.txt', 'r') as file:
            baris = file.readlines()
            for i in range(len(baris)):
                if i == 0:  
                    continue
                x = baris[i].strip().split(',')
                if username == x[0]:
                    if password == x[1]:
                        print('\nBerhasil login!')
                        self.currentUser = User(username, password)
                        print(f"Selamat datang, {username}!")
                        print(f"Saldo anda: Rp.{self.currentUser.balance:,}")
                        return True
                    else:
                        print('\nPassword salah!')
                        return False
            print('\nUsername tidak ditemukan!')
            return False
                
    def addProduct(self):
        name = input("Masukkan nama produk: ")
        price = int(input("Masukkan harga produk (Contoh: 1,000): ").replace(',', ''))
        category = input("Masukkan kategori produk: ")
        
        if price <= 0:
            print("Harga tidak boleh 0 atau kurang")
            return
        
        df = pd.read_csv(self.csvFile)
        newRow = pd.DataFrame({'name': [name], 'price': [price], 'category': [category]})
        df = pd.concat([df, newRow], ignore_index=True)
        df.to_csv(self.csvFile, index=False)
        print(f"Produk {name}, berhasil ditambahkan!\n")
        
    def topUp(self):
        balance = input("Masukkan nominal uang (Contoh: 1,000,000): Rp.")
        balance = int(balance.replace(',', ''))
        self.currentUser.balance += balance
        self.currentUser.save_balance()
        print(f"Saldo sejumlah Rp.{balance:,} berhasil ditambahkan!")
        print(f"Saldo anda sekarang: Rp.{self.currentUser.balance:,}\n")

    def cekSaldo(self):
        print(f'Saldo yang anda miliki sebanyak: Rp.{self.currentUser.balance}\n')

    def removeProduct(self, product_name):
        df = pd.read_csv(self.csvFile)
        df = df[df['name'] != product_name]
        df.to_csv(self.csvFile, index=False)
    
    
        
    def buyProduct(self):
        displayProducts()
        productName = input("Masukkan nama produk yang ingin dibeli: ")
        df = pd.read_csv(self.csvFile)
        product = df[df['name'] == productName]
        
        if not product.empty:
            price = product['price'].values[0]
            nego = input('Apakah anda ingin melakukan nego? (y/n): ')
            if nego.lower() == 'y':
                self.nego(productName)
            else:
                price = product['price'].values[0]
                validate = input(f"Yakin ingin membeli produk {productName} seharga Rp.{price:,}? (y/n): ")
                if validate.lower() == 'y':
                    if self.currentUser.balance >= price:
                        self.currentUser.balance -= price
                        self.currentUser.save_balance()
                        self.currentUser.save_history(
                            productName, 
                            price, 
                            product['category'].values[0]
                        )
                        self.removeProduct(productName)
                        print(f"Produk {productName} berhasil dibeli seharga Rp.{price:,}")
                        print(f"Sisa saldo anda: Rp.{self.currentUser.balance:,}\n")
                    else:
                        print("Saldo tidak cukup untuk membeli produk ini\n")
                else:
                    print("Pembelian dibatalkan\n")
        else:
            print("Produk tidak ditemukan\n")
    
    def nego(self, productName):
        df = pd.read_csv('product.csv')
        product = df[df['name'] == productName]
        
        if not product.empty:
            originalPrice = product['price'].values[0]
            negoPrice = int(input(f"Masukkan harga nego untuk produk {productName} (Contoh: 1,000): ").replace(',', ''))
            minAcceptance = originalPrice * 0.8
            
            if negoPrice >= minAcceptance:
                print(f"Nego diterima! Anda dapat membeli {productName} seharga {negoPrice:,}")
                validate = input(f"Yakin ingin membeli produk {productName} seharga Rp.{negoPrice:,}? (y/n): ")
                if validate.lower() == 'y':
                    if self.currentUser.balance >= negoPrice:
                        self.currentUser.balance -= negoPrice
                        self.currentUser.save_balance()
                        self.currentUser.save_history(
                            productName, 
                            negoPrice, 
                            product['category'].values[0]
                        )
                        self.removeProduct(productName)
                        print(f"Produk {productName} berhasil dibeli seharga Rp.{negoPrice:,}")
                        print(f"Sisa saldo anda: Rp.{self.currentUser.balance:,}\n")
                    else:
                        print("Saldo tidak cukup untuk membeli produk ini\n")
                else:
                    print("Pembelian dibatalkan\n")
            else:
                print("Nego tidak diterima. Harga nego harus setidaknya 80% dari harga asli\n")
        else:
            print("Produk tidak ditemukan\n")
        
    def addFavorite(self):
        displayProducts()
        productName = input("Masukkan nama produk yang ingin ditambahkan ke favorit: ")
        df = pd.read_csv(self.csvFile)
        product = df[df['name'] == productName]
        
        if not product.empty:
            if productName not in self.currentUser.favorite:
                self.currentUser.favorite.append(productName)
                print(f"Produk {productName} berhasil ditambahkan ke favorit\n")
            else:
                print(f"Produk {productName} sudah ada di favorit\n")
        else:
            print("Produk tidak ditemukan\n")
        
    def viewHistory(self):
        if not self.currentUser.history:
            print("Belum ada riwayat pembelian\n")
            return
        
        print("\nRiwayat Pembelian:")
        print("------------------")
        for item in self.currentUser.history:
            print(f"Nama: {item['name']}, Harga: Rp.{item['price']:,}, Kategori: {item['category']}")
        print()
    
    def viewFavorite(self):
        if not self.currentUser.favorite:
            print("Anda tidak memiliki produk favorit\n")
            return
        
        print("\nDaftar produk favorit:")
        print("--------------------")
        for productName in self.currentUser.favorite:
            df = pd.read_csv(self.csvFile)
            product = df[df['name'] == productName]
            
            if not product.empty:
                price = product['price'].values[0]
                category = product['category'].values[0]
                print(f"Nama: {productName}, Harga: Rp.{price:,}, Kategori: {category}")
        print()

def main():
    shop = OnlineShop()
    
    while True:
        loginOption()
        choice = input("Pilih opsi: ")
        
        if choice == '1':
            username = input("Masukkan username: ")
            password = input("Masukkan password: ")
            shop.register(username, password)
            
        elif choice == '2':
            login_successful = False
            while not login_successful:
                username = input("\nMasukkan username: ")
                password = input("Masukkan password: ")
                login_successful = shop.login(username, password)
                
                if not login_successful:
                    print("Silakan coba login kembali atau pilih opsi lain")
                    retry = input("Ingin mencoba login lagi? (y/n): ")
                    if retry.lower() != 'y':
                        break
            
            if login_successful:
                while True:
                    mainMenu()
                    option = input("Pilih opsi: ")
                    
                    if option == '1':
                        if shop.currentUser.name == 'admin':
                            shop.addProduct()
                        else:
                            print("Maaf, fitur ini hanya untuk admin!")
                    elif option == '2':
                        shop.topUp()
                    elif option == '3':
                        shop.buyProduct()
                    elif option == '4':
                        shop.addFavorite()
                    elif option == '5':
                        shop.viewHistory()
                    elif option == '6':
                        shop.viewFavorite()
                    elif option == '7':
                        shop.cekSaldo()
                    elif option == '8':
                        print("                                                      Terima kasih telah menggunakan layanan kami!\n")
                        break
                        
                    else:
                        print("Pilihan tidak valid, mohon masukkan ulang")
                        
        elif choice == '3':
            print("                                                      Terima kasih sudah berkunjung!")
            break
            
if __name__ == '__main__':
    main()