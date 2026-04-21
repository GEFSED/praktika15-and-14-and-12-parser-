from PIL import Image, ImageDraw, ImageFont

# 7.1
img = Image.open("postcard.jpg")
cropped = img.crop((50, 50, 500, 350))
cropped.save("postcard_crop.jpg")
print("Обрезанное изображение сохранено: postcard_crop.jpg")

# 7.2
cards = {
    "новый год": "new_year.jpg",
    "8 марта": "march8.jpg",
    "день рождения": "birthday.jpg"
}

holiday = input("К кaкому празднику нужна открытка? ").lower()

if holiday in cards:
    card = Image.open(cards[holiday])
    card.show()
else:
    print("Такого праздника нет.")

# 7.3
holiday = input("Введите праздник: ").lower()
name = input("Введите имя: ")

if holiday in cards:
    img = Image.open(cards[holiday])
    draw = ImageDraw.Draw(img)

    text = f"{name}, поздравляю!"

    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (img.width - text_width) // 2
    y = img.height - text_height - 20

    draw.text((x, y), text, font=font, fill="red")

    img.save("greeting.png")
    img.show()
    print("Новая открытка сохранена: greeting.png")
else:
    print("Такого праздника нет.")