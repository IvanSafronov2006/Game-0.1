# Добавление текста
my_font = pygame.font.Font("fonts/AmaticSC-Bold.ttf", 40)
text = my_font.render("Сам текст", True, (255, 255, 255))# Текст, сглаживание, цвет
screen.blit(text,(0, 0))

# Добавление картинки
picture = pygame.image.load("images/icon.png")
picture = pygame.transform.scale(picture, (100, 100))
screen.blit(picture, (0, 0))

spis_with_login1 = basa_cursor.execute('''SELECT login FROM people''').fetchall()
self.basa_cursor.execute('''INSERT INTO people_group (id_group, id_people, status) VALUES (?, ?, ?)''', (a, b, c))
self.basa_cursor.execute('''DELETE FROM people_group WHERE id_people = (?)''', (b[0][0],))
self.basa_d.commit()
self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (1, b))