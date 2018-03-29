# -*- coding: UTF-8 -*-
import time
import os

import pyautogui

import pyscreeze

from time import sleep, localtime, ctime

win_pos_x, win_pos_y = 200, 123

# 平台软件里面，启动HS的按钮的位置
pos_app_start_x, pos_app_start_y = 396, 689

# HS里面，如果有新任务，确认键按钮的位置；其实没有按钮，点击任意位置即可
pos_player_new_task_x, pos_player_new_task_y = 988, 337

# HS里面， 启动对战按钮的位置；
pos_player_start_battle_x, pos_player_start_battle_y = 607, 237

# HS里面，选择职业的按钮的位置；这里可以指定刷的职业，
pos_player_select_carrier_x, pos_player_select_carrier_y = 506, 591

# HS里面，选择狂野还是标准模式的按钮的位置，我们选择狂野
pos_player_select_wild_x, pos_player_select_wild_y = 889, 60

# HS里面，选择休闲模式还是天梯模式的按钮的位置，我们选择天梯；
pos_player_select_tianti_x, pos_player_select_tianti_y = 947, 178

# HS里面，真正启动对战的按钮，点击后就开始匹配
pos_player_start_round_x, pos_player_start_round_y = 887, 582

# HS里面，发了新卡后，换牌后，确认的按钮的位置，我们不换牌
pos_player_confirm_new_card_x, pos_player_confirm_new_card_y = 613, 564

# HS里面，右上角 选项 按钮的位置
pos_player_option_x, pos_player_option_y = 1373, 782

# HS里面，选项中，投降按钮的位置
pos_player_option_giveup_x, pos_player_option_giveup_y = 608, 278

pos_player_return_x, pos_player_return_y = 988, 337

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
        # log('Could not find the image: %s' % png)
        raise Exception('Locate image %s failed.' % png)


def found_image(png):
    # location = pyscreeze.locateOnScreen(png)
    location = pyautogui.locateOnScreen(png)
    return location is not None

# 一轮对战，从主界面 点击对战开始，到投降结束；


class c_hs_helper(object):
    def __init__(self):
        self.win_count = 30
        self.day = 23
        self.main_x, self.main_y = 0, 0

    def log(self, str):
        with open('hs.log', 'a') as f:
            from datetime import datetime
            output = '%s  %s ' % (datetime.now().strftime('%m-%d %H:%M:%S'), str)
            f.write(output + '\n')
            print(output)

    def click_position(self, x=pos_player_new_task_x, y=pos_player_new_task_y,
                       speed=2, timer=3):
        pyautogui.moveTo(x + self.main_x, y + self.main_y,
                         duration=speed, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        sleep(timer)

    def simple_click(self):
        self.click_position(speed=1, timer=1)

    def click_png(self, png):
        if self.found_image(png):
            location = pyscreeze.locateOnScreen(png)
            if location:
                print(location)
                self.log('Found image %s' % png)
                center_x, center_y = pyscreeze.center(location)
                self.click_position(center_x, center_y)
        else:
            self.log('Could not find the image: %s' % png)
            raise Exception('Locate image %s failed.' % png)

    def get_main_position(self):
        import win32gui
        hwnd = win32gui.FindWindow(None,  u'炉石传说')
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            self.main_x, self.main_y = rect[0], rect[1]
            self.log('Find postion, x={rect[0]}, y={rect[1]}'.format(rect=rect))
        else:
            self.log('Could not find the game window.')
            self.click_position(pos_app_start_x, pos_app_start_y)
            self.click_position(pos_app_start_x, pos_app_start_y)
            # self.click_png('start_player.png')
            sleep(20)
            self.simple_click()

            self.main_x = 192
            self.main_y = 93
            # raise Exception('Could not find the game window.')

    def game_is_goon(self):
        import win32gui
        hwnd = win32gui.FindWindow(None,  u'炉石传说')
        if hwnd:
            self.log('Game is going on.')
            return True
        else:
            self.log('Game is over.')
            return False


    def setup(self):
        # self.start_platform_if_needed()
        self.start_player_if_needed()

    def start_platform_if_needed(self):
        self.log('Prepare Platform')
        lines = os.popen('tasklist |find /I "Battle.net"').readlines()
        if lines:
            self.log('Platform is already running.')
            print(lines)
        else:
            self.log('Platform have not startup, I will run it first')
            os.system(r'"D:\\tools\\Battle.net\\Battle.net Launcher.exe"')
            sleep(20)
            self.log('Start platform successfully.')

    def start_player_if_needed(self):
        lines = os.popen('tasklist |find /I "Hearthstone"').readlines()
        if lines:
            self.log('Close Player')
            os.system("TASKKILL /F /IM Hearthstone.exe")
            sleep(10)
        self.click_position(pos_app_start_x, pos_app_start_y)
        self.click_position(pos_app_start_x, pos_app_start_y)
        # self.click_png('start_player.png')
        sleep(20)
        self.simple_click()
        self.log('Start Player successfully.')

    def is_game_time(self):
        clock, day = localtime().tm_hour, localtime().tm_mday
        new_day = day <> self.day
        if new_day:
            self.log('New day is coming {}'.format(day))
            self.day = day
            self.win_count = 0
        return clock >= 2 and clock < 8 and self.win_count < 30

    def enter_a_round(self):
        self.simple_click()
        self.log('Start Battle')
        self.click_position(pos_player_start_battle_x, pos_player_start_battle_y)
        # if not self.found_image('wide.png'):
        #     self.click_position(pos_player_select_wild_x, pos_player_select_wild_y)


    def check_image(self, png):
        location = pyautogui.locateOnScreen(png)
        return location is not None

    def found_image(self, png = '', count = 5):
        self.log('Looking for image: ' + png)
        for i in range(count):
            if self.check_image(png):
                return True
        return False

    def is_back_on_battle_start(self):
        return self.found_image('bk1.png')

    def clean_gui(self):
        for i in range(8):
            # pyautogui.press('esc')
            # sleep(1)
            self.simple_click()

    def round_match(self):
        self.log('start round match')
        start_time = time.time()
        match_times = 0
        result = False
        while time.time() - start_time < 90:
            self.simple_click()
            if self.found_image('matching.png'):
                self.log('Still in matching')
            else:
                self.log('Not found matching.png, maybe match done')
                match_times += 1
                if match_times == 2:
                    self.log('matching done')  # match done, does not need for 60s timer
                    result = True
                    break
        return result

    def give_up(self):
        # 首先用ESC键进行投降
        pyautogui.press('esc')
        self.click_position(pos_player_option_giveup_x, pos_player_option_giveup_y)

        # 反复用ESC键，来清除哪些可能跳出的界面
        self.clean_gui()

        # 确认回到了开始战斗的背景页面
        for i in range(5):
            if not self.is_back_on_battle_start():
                self.simple_click()
            else:
                break

    def play_a_round(self):
        self.log('Total have win: %s' % self.win_count)
        must_give_up = False
        # if self.found_image('level_16.png', 3):
        #     self.log('Current is level 16, I must give up')
        #     must_give_up = True
        # else:
        #     self.log('Not level 16')
        #     must_give_up = False

        # 点击开始
        self.log('Start Match')
        self.click_position(pos_player_start_round_x, pos_player_start_round_y, 1, 1)

        # 等待匹配结束 timer = 60s
        if not self.round_match():
            self.win_count = 30
            return 0

        if not self.game_is_goon():
            self.win_count = 30
            return 0

        # 如果必须投降，马上投降
        if must_give_up:
            self.give_up()
        else:
            # 选卡，然后点击确定
            sleep(10)
            self.log('Select card.')
            self.click_position(pos_player_confirm_new_card_x, pos_player_confirm_new_card_y)

            self.log('Wait for succeed')
            if not self.game_is_goon():
                self.win_count = 30
                return 0

            for i in range(3):
                self.clean_gui()
                if not self.game_is_goon():
                    self.win_count = 30
                    return 0

                if self.is_back_on_battle_start():
                    self.log('I win this round')
                    self.win_count += 1
                    return 0

            self.log('I Give up')
            self.give_up()

    def start_video(self):
        pass
        # click_position(1493, 119)
        # click_position(1493, 119)

    def stop_video(self):
        pass
        # click_position(1525, 121)
        # click_position(1525, 121)

    def run(self):
        while True:
            if self.is_game_time():
                self.log('It is Game time.')
                self.setup()
                self.get_main_position()
                # raise Exception('Debug')
                self.enter_a_round()
                self.start_video()
                while self.win_count < 30:
                    self.play_a_round()
                self.win_count = 0
                self.stop_video()
            else:
                if self.win_count >= 30:
                    self.log('Have win 30, sleep...')
                else:
                    self.log('Not game time, sleep...')
                sleep(60)


if __name__ == '__main__':
    # main()
    helper = c_hs_helper()
    helper.run()
