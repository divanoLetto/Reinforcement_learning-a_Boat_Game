from BoatGame import BoatGame


def main():
    g = BoatGame(on_play_mode=True)
    while True:
        g.init_game()
        g.run()


if __name__ == "__main__":
    main()