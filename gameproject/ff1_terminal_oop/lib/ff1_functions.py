import os
from pynput import keyboard

# input("Who you gonna call? FRPS Module!")
# print(dir(frps))
#
# my_rps_game = frps.Game(ruleset=None, rounds=1, target_score=None)
# print(type(my_rps_game))
# print(my_rps_game)
# input()


def fullwidth_str(text: str) -> str:
    """
  Translate string to fullwidth unicode characters to avoid weird spacing (Can't do Umlauts!)
  :param text: String to convert
  :return: Converted string
  """
    to_fullwidth = str.maketrans(
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~ ',
        '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～　')
    return text.translate(to_fullwidth)


def fancy_string(
        string: str = "Hier könnte Ihre Werbung stehen!",
        width: int = 30) -> str:
    """
    :param string: Text
    :param width: width of the  box
    :return: fancystring
    """
    border = "#"
    padder = " "
    # We have a mix of even and uneven parameter. Add an extra char
    if len(string) % 2 != width % 2:
        topline = border + border
    else:
        topline = border

    for i in range(0, width-2):  # -2 because we have the border
        topline = topline + border

    topline = topline + border + "\n"
    padding = ""

    for i in range(0, int((width-1)/2-len(string)/2)):
        padding = padding + padder

    middleline = border + padding + string + padding + border + "\n"
    bottomline = topline
    fancystring = topline + middleline + bottomline
    return fullwidth_str(fancystring)


def clear():
    """
    Clears screen (needs "real" Terminal!)
    :return: No return
    """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def gameover(
        grid,
        reason: str = "Game Over!",
        ):
    """
    :param grid: current Grid
    :param reason: Reason for Game Over
    :return:
    """
    grid.update()
    print(fancy_string(reason, grid.size_y))
    print("Press CTRL+C to quit")
