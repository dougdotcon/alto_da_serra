import os

def criar_pastas(qtd=50):
    for i in range(1, qtd + 1):
        pasta = f'M{i}'
        try:
            os.makedirs(pasta)
            print(f'Pasta criada: {pasta}')
        except FileExistsError:
            print(f'A pasta já existe: {pasta}')

if __name__ == '__main__':
    criar_pastas()
