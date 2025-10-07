import os 


def main():
    name = os.getenv("USERNAME")
    print(f"Hello, {name}! Estoy en GitHub Actions")


if __name__ == "__main__":
    main()