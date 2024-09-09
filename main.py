from maze import Maze, Window

def main():
    print('Starting Process...')
    win = Window(800, 600)

    Maze(x1=0, y1=0, num_rows=5, num_cols=5, cell_size_x=20, cell_size_y=20, win=win)

    # win.draw_line(line, "black")
    win.wait_for_close()

    print("\nExiting...")


if __name__ == "__main__":
    main()