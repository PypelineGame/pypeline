
                elif col in list('1234567'):
                    if col == "1":
                        enemy = GarbageCollector(x-32, y-64)
                    elif col == "2":
                        enemy = GreenPysnake(x-32, y-64)
                        entities.add(enemy)
                        enemies.append(enemy)
                        enemy_sprites.add(enemy)
                    elif col == "3":
                        enemy = RedPysnake(x-32, y-64)
                    elif col == "4":
                        enemy = BluePysnake(x-32, y-64)
                    elif col == "5":
                        enemy = PurplePysnake(x-32, y-64)
                    elif col == "6":
                        enemy = RedGhost(x, y)
                    elif col == "7":
                        enemy = WhiteGhost(x, y)
                    #entities.add(enemy)
                    #enemies.append(enemy)
                    #enemy_sprites.add(enemy)