import json
with open("products.json", "r", encoding="utf-8") as file:
    data = json.load(file)
print("Содержимое файла products.json:\n")
for product in data["products"]:
    print("Название:", product["name"])
    print("Цена:", product["price"])
    print("Вес:", product["weight"])
    if product["available"]:
        print("В наличии")
    else:
        print("Нет в наличии!")
    print()
answer = input("Добавить новый продукт? (да/нет): ")
if answer.lower() == "да":
    name = input("Введите название: ")
    price = int(input("Введите цену: "))
    weight = int(input("Введите вес: "))
    available = input("Есть в наличии? (да/нет): ").lower() == "да"
    new_product = {
        "name": name,
        "price": price,
        "available": available,
        "weight": weight
    }
    data["products"].append(new_product)
    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("\nОбновлённое содержимое файла products.json:\n")
    for product in data["products"]:
        print("Название:", product["name"])
        print("Цена:", product["price"])
        print("Вес:", product["weight"])
        if product["available"]:
            print("В наличии")
        else:
            print("Нет в наличии!")
        print()

# 9.3
ru_en = {}

with open("en-ru.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line == "":
            continue

        line = line.replace("–", "-")
        en_word, ru_words = line.split(" - ")
        ru_words = ru_words.split(", ")

        for ru_word in ru_words:
            if ru_word not in ru_en:
                ru_en[ru_word] = []
            if en_word not in ru_en[ru_word]:
                ru_en[ru_word].append(en_word)

with open("ru-en.txt", "w", encoding="utf-8") as file:
    for ru_word in sorted(ru_en):
        file.write(ru_word + " - " + ", ".join(ru_en[ru_word]) + "\n")

print("Файл ru-en.txt создан.")
