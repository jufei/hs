# -*- coding: UTF-8 -*-
import pyautogui
import pyscreeze
import time

from time import sleep, localtime, ctime

win_pos_x, win_pos_y = 200, 123

# 平台软件里面，启动HS的按钮的位置
pos_app_start_x, pos_app_start_y = 396, 689

# HS里面，如果有新任务，确认键按钮的位置；其实没有按钮，点击任意位置即可
pos_player_new_task_x, pos_player_new_task_y = 1166, 406

# HS里面， 启动对战按钮的位置；
pos_player_start_battle_x, pos_player_start_battle_y = 811, 332

# HS里面，选择职业的按钮的位置；这里可以指定刷的职业，
pos_player_select_carrier_x, pos_player_select_carrier_y = 506, 591

# HS里面，选择狂野还是标准模式的按钮的位置，我们选择狂野
pos_player_select_wild_x, pos_player_select_wild_y = 925, 117

# HS里面，选择休闲模式还是天梯模式的按钮的位置，我们选择天梯；
pos_player_select_tianti_x, pos_player_select_tianti_y = 1134, 230

# HS里面，真正启动对战的按钮，点击后就开始匹配
pos_player_start_round_x, pos_player_start_round_y = 1070, 677

# HS里面，发了新卡后，换牌后，确认的按钮的位置，我们不换牌
pos_player_confirm_new_card_x, pos_player_confirm_new_card_y = 802, 650

# HS里面，右上角 选项 按钮的位置
pos_player_option_x, pos_player_option_y = 1373, 782

# HS里面，选项中，投降按钮的位置
pos_player_option_giveup_x, pos_player_option_giveup_y = 806, 369

pos_player_return_x, pos_player_return_y = 1190, 745

# HS里面，匹配对战的时候等待的时间
timer_for_match = 90

# HS里面，等待对方主动投降的时间，如果对方不投降，我们投降。
timer_for_waiting_giveup = 120

png_start_player = 'start_player.png'
png_enter_battle = 'enter_battle.png'
png_wild_mode = 'is_wide_mode.png'
png_select_wild_mode = 'select_wild.png'
png_carrier = 'carrier.png'
png_tianti = 'tianti.png'
png_level_17 = 'level_17.png'
png_start_match = 'start_match.png'
png_is_matching = 'is_martching.png'
png_select_card = 'select_card.png'
png_i_win = 'iwin.png'
png_option = 'option.png'
png_option_giveup = 'giveup.png'


win_count = 0
total_win = 0

def click_position(x, y):
    pyautogui.moveTo(x, y, duration=2, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    sleep(3)


def click_png(png):
    # location = pyautogui.locateOnScreen(png)
    location = pyscreeze.locateOnScreen(png)
    if location:
        print(location)
        log('Found image%s' % png)
        # center_x, center_y = pyautogui.locateCenterOnScreen(png)
        center_x, center_y = pyscreeze.center(location)
        click_position(center_x, center_y)
    else:
        log('Could not find the image: %s' % png)
        raise Exception('Locate image %s failed.' % png)

def found_image(png):
    # location = pyscreeze.locateOnScreen(png)
    location = pyautogui.locateOnScreen(png)
    return location is not None

# 一轮对战，从主界面 点击对战开始，到投降结束；
def enter_a_round():
    click_position(pos_player_new_task_x, pos_player_new_task_y)
    # click_position(pos_player_new_task_x, pos_player_new_task_y)
    # 点击对战
    log('Start Battale')
    # click_png(png_enter_battle)
    click_position(pos_player_start_battle_x, pos_player_start_battle_y)

    # 选择职业
    log('Select carrier')
    # click_position(pos_player_select_carrier_x, pos_player_select_carrier_y)
    # click_png(png_carrier)

    # 判断当前是否是狂野模式，如果不是，切换到狂野模式
    # if not is_wild_mode():
    #     click_png(png_select_wild_mode)

    # 选择天梯
    log('Select Tianti')
    # click_png(png_tianti)
    # click_position(pos_player_select_tianti_x, pos_player_select_tianti_y)

def play_a_round():
    global win_count
    global total_win
    log('Total win: %s' % total_win)
    win_count = 0
    must_give_up = False
    for i in range(3):
        if found_image('level_16.png'):
            log('current is level 16, must give up')
            must_give_up = True
            break
        else:
            log('not found level 16')


    # 点击开始
    log('Start Match')
    # click_png(png_start_match)
    click_position(pos_player_start_round_x, pos_player_start_round_y)

    start_time = time.time()
    match_times = 0
    matched = False
    while time.time() - start_time < 60:
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        if found_image('matching.png'):
            log('Still matching')
            pass
        else:
            log('Not found matching.png, maybe match done')
            match_times += 1
            if match_times == 3:
                log('matching done')
                matched = True
                break


    if must_give_up:
        pyautogui.press('esc')
        click_position(pos_player_option_giveup_x, pos_player_option_giveup_y)
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        win_count = 0
        return 0

    sleep(10)
    click_position(pos_player_confirm_new_card_x, pos_player_confirm_new_card_y)

    log('wait for succeed')
    sleep(15)
    click_position(pos_player_new_task_x, pos_player_new_task_y)
    click_position(pos_player_new_task_x, pos_player_new_task_y)
    click_position(pos_player_new_task_x, pos_player_new_task_y)

    #check if i succeed
    log('begin to check if win')
    i_win = False
    count = 0
    start_time = time.time()

    for i in range(8):
        if found_image('bk1.png'):
            log('Found back to background')
            count += 1
        i_win = count>3
        if i_win:
            break
    if not i_win:
        log('I Give up')
        pyautogui.press('esc')
        click_position(pos_player_option_giveup_x, pos_player_option_giveup_y)
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        click_position(pos_player_new_task_x, pos_player_new_task_y)
        win_count = 0
    else:
        log('I win the game.')
        win_count += 1
        total_win += 1
        # click_position(pos_player_new_task_x, pos_player_new_task_y)
        # click_position(pos_player_new_task_x, pos_player_new_task_y)
        # click_position(pos_player_new_task_x, pos_player_new_task_y)


# 从暴雪平台，启动HS
def start_player():
    # 在暴雪平台上，启动HS
    log('Start HS Player')
    # click_png(png_start_player)
    click_position(pos_app_start_x, pos_app_start_y)
    # 等待HS启动成功
    sleep(20)


# 关闭HS
def stop_player():
    import os
    log('关闭炉石')
    os.system("TASKKILL /F /IM Hearthstone.exe")
    sleep(10)


# 启动暴雪平台
def start_platform():
    # 检查暴雪平台是否已经启动，如果没有，启动暴雪平台
    import os
    lines = os.popen('tasklist |find /I "TmaApplication"').readlines()
    print(lines)
    if True:
        os.popen('run platform.exe')
    pass


# 完整一轮, 从平台启动HS开始，到HS关闭结束。
def play_full_round():
    # start_player()
    try:
        play_a_round()
    finally:
        pass
        # stop_player()


def log(str):
    with open('hs.log', 'a') as f:
        output = '%s  %s ' % (ctime(), str)
        f.write(output)
        print(output)


# 判断当前是否是狂野模式，这个可以用来作为切换模式的前提
def is_wild_mode():
    return pyautogui.locateOnScreen(png_wild_mode)


# 判断是否匹配成功，进入游戏, 通过判断是否进入了换牌界面，来判断是否匹配成功
# 也可以考虑反过来，看匹配界面是否还在
def match_succeed():
    return pyautogui.locateOnScreen(png_select_card)


# 判断是否获胜，通过界面图片
def i_win():
    return pyautogui.locateOnScreen(png_i_win)

def match_win():
    return pyautogui.locateOnScreen('victory.png')

# 主函数，只在凌晨2点到3点工作
def main():
    log(r'Start HS Player')
    # enter_a_round()
    while True:
        clock, minute = localtime().tm_hour, localtime().tm_min
        if clock >= 0 and clock < 24:
            log(r'Now: %s %s, I will play ' % (clock, minute))
            play_a_round()
            # play_full_round()
        else:
            log('Now: %s %s , I will sleep' % (clock, minute))
            sleep(60)


if __name__ == '__main__':
    main()
