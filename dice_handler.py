# dice_handler.py
import random

# Calls appropriate method for given command message
def roll_message_parse(message_content, message_author):
    message_arr = message_content.split(" ")
    
    rolls = []
    target = 0
    focus = 0
    ret = str(message_author)[:len(str(message_author))-5]
    
    # Parses dice roll (XdY)
    if len(message_arr) == 1:
        return "Error: no parameters inclueded. For help, type `!help`"
    elif message_arr[1].isnumeric():
        rolls = roll_dice(int(message_arr[1]), 6)
    elif message_arr[1].startswith("d"):
        if message_arr[1][1:].isnumeric():
            rolls = roll_dice(1, int(message_arr[1][1:]))
    elif "d" in message_arr[1]:
        message_arr_2 = message_arr[1].split("d")
        if message_arr_2[0].isnumeric() and message_arr_2[1].isnumeric():
            rolls = roll_dice(int(message_arr_2[0]), int(message_arr_2[1]))
        else:
            return "Error: both parameters must be numeric. For help, type `!help`"
    else:
        return "Error: incorrect syntax. For help, type `!help`"
    
    # Parses extra parameters
    if len(message_arr) > 2:
        for term in message_arr[2:]:
            if term.startswith("t"):
                if term[1:].isnumeric():
                    target = int(term[1:])
                else:
                    return "Error: the term \"tX\" requires X to be an integer. For help, type `!help`"
            elif term.startswith("f"):
                if term[1:].isnumeric():
                    focus = int(term[1:])
                else:
                    return "Error: the term \"fY\" requires X to be an integer. For help, type `!help`"
        if target > 0:
            pos = 0
            focus2 = focus
            # while pos < len(rolls) and rolls[pos] >= target:
            #    pos += 1
            while pos < len(rolls) and focus2 >= target - rolls[pos]:
                focus2 -= target - rolls[pos]
                pos += 1
            ret = ret + " rolled " + str(rolls) + ".\n`" + str(pos) + "` successes of difficulty `" + str(target) + "`, using `" + str(focus) + "` focus."
    else:
        dice_sum = 0
        for roll in rolls:
            dice_sum += roll
        ret = ret + " rolled `" + str(rolls) + "`.\n`" + str(dice_sum) + "` was the total."
    
    return ret

# Returns an array of rolled dice, sorted from largest to smallest
def roll_dice(count, faces):
    rolls = []
    for rollNum in range(int(count)):
        rolls.append(random.randint(1, int(faces)))
    rolls = sorted(rolls)
    rolls.reverse()
    return rolls