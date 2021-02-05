from BoatGame import BoatGame


def main():
    g = BoatGame(on_play_mode=True)
    # g.show_start_screen()
    while True:
        g.init_game()
        g.run()
        # g.show_go_screen()


if __name__ == "__main__":
    main()