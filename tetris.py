import pygame
import random
import subprocess

# 게임 초기화
pygame.init()

# 화면 설정
screen_width = 300
screen_height = 660  # 화면 높이를 늘림
cell_size = 30
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("테트리스")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 테트로미노 모양 및 색상
tetrominoes = [
    {
        '모양': [[1, 1, 1, 1]],  # I 블록
        '색상': (255, 0, 0)  # I 블록에 빨간색 지정
    },
    {
        '모양': [[1, 1], [1, 1]],  # O 블록
        '색상': (0, 255, 0)
    },
    {
        '모양': [[0, 1, 0], [1, 1, 1]],  # T 블록
        '색상': (0, 0, 255)
    },
    {
        '모양': [[1, 1, 0], [0, 1, 1]],  # Z 블록
        '색상': (255, 255, 0)
    },
    {
        '모양': [[0, 1, 1], [1, 1, 0]],  # S 블록
        '색상': (0, 255, 255)
    },
    {
        '모양': [[1, 0, 0], [1, 1, 1]],  # J 블록
        '색상': (255, 0, 255)
    },
    {
        '모양': [[0, 0, 1], [1, 1, 1]],  # L 블록
        '색상': (255, 165, 0)
    }
]

# 게임 변수 초기화
board_width = screen_width // cell_size
board_height = screen_height // cell_size
board = [[0] * board_width for _ in range(board_height)]
current_tetromino = None
current_tetromino_x = 0
current_tetromino_y = 0
time_to_fall = 0.4  # 블록이 한 칸씩 아래로 떨어지는 주기 (초) - 감소된 값
fall_timer = 0.0  # 블록을 아래로 떨어뜨리기 위한 타이머

# 함수: 블록 생성
def spawn_tetromino():
    global current_tetromino, current_tetromino_x, current_tetromino_y
    current_tetromino = random.choice(tetrominoes)
    current_tetromino_x = board_width // 2 - len(current_tetromino['모양'][0]) // 2
    current_tetromino_y = 0

# 함수: 블록 이동
def move_tetromino(dx, dy):
    global current_tetromino_x, current_tetromino_y
    if not check_collision(current_tetromino['모양'], current_tetromino_x + dx, current_tetromino_y + dy):
        current_tetromino_x += dx
        current_tetromino_y += dy
        return True
    return False

# 함수: 충돌 검사
def check_collision(tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                board_row = y + row
                board_col = x + col
                if board_row < 0 or board_col < 0 or board_col >= board_width or board_row >= board_height or board[board_row][board_col]:
                    return True
    return False

# 함수: 행 삭제
def clear_rows():
    global board
    rows_to_clear = [i for i, row in enumerate(board) if all(row)]
    for row in rows_to_clear:
        del board[row]
        board.insert(0, [0] * board_width)

# 함수: 게임 오버 여부 확인
def is_game_over():
    global current_tetromino
    if current_tetromino_y <= 0:
        return True
    return False

# 함수: 블록 회전 (90도씩)
def rotate_tetromino():
    global current_tetromino
    rotated_tetromino = [[current_tetromino['모양'][y][x] for y in range(len(current_tetromino['모양']))] for x in range(len(current_tetromino['모양'][0]) - 1, -1, -1)]
    if not check_collision(rotated_tetromino, current_tetromino_x, current_tetromino_y):
        current_tetromino['모양'] = rotated_tetromino

# 게임 루프
running = True
spawn_tetromino()
clock = pygame.time.Clock()

# 키 입력 딜레이 설정
move_delay = 100  # 밀리초 단위로 지연 시간 설정
rotate_delay = 200  # 밀리초 단위로 지연 시간 설정
last_move_time = 0
last_rotate_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    # 왼쪽으로 이동
    if keys[pygame.K_LEFT] and current_time - last_move_time > move_delay:
        move_tetromino(-1, 0)
        last_move_time = current_time

    # 오른쪽으로 이동
    if keys[pygame.K_RIGHT] and current_time - last_move_time > move_delay:
        move_tetromino(1, 0)
        last_move_time = current_time

    # 아래로 이동
    if keys[pygame.K_DOWN] and current_time - last_move_time > move_delay:
        move_tetromino(0, 1)
        last_move_time = current_time

    # 방향 전환
    if keys[pygame.K_UP] and current_time - last_rotate_time > rotate_delay:
        rotate_tetromino()
        last_rotate_time = current_time

    # 타이머 업데이트
    elapsed_time = clock.tick(60)  # 초당 60프레임
    fall_timer += elapsed_time

    # 시간 경과에 따라 블록을 아래로 이동
    if fall_timer >= time_to_fall * 1000:
        if not move_tetromino(0, 1):
            for row in range(len(current_tetromino['모양'])):
                for col in range(len(current_tetromino['모양'][row])):
                    if current_tetromino['모양'][row][col]:
                        board[current_tetromino_y + row][current_tetromino_x + col] = 1
            clear_rows()
            if is_game_over():
                pygame.quit()
                running = False
                subprocess.run(["python", "gamemain.py"])
                break
            else:
                spawn_tetromino()
        fall_timer = 0

    screen.fill(BLACK)

    for row in range(board_height):
        for col in range(board_width):
            if board[row][col]:
                pygame.draw.rect(screen, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))

    if current_tetromino:
        for row in range(len(current_tetromino['모양'])):
            for col in range(len(current_tetromino['모양'][row])):
                if current_tetromino['모양'][row][col]:
                    block_color = current_tetromino['색상']
                    pygame.draw.rect(screen, block_color, (current_tetromino_x * cell_size + col * cell_size, current_tetromino_y * cell_size + row * cell_size, cell_size, cell_size))

    pygame.display.update()
