elif buttons["home"].collidepoint(event.pos):
                print("Home button clicked")
                pygame.mixer.music.stop()
                exec(open("Home.py", encoding="utf-8").read())