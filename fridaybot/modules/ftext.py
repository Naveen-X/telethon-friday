from uniborg.util import friday_on_cmd


@friday.on(friday_on_cmd(pattern="ftext ?(.*)"))
async def payf(event):
    if event.fwd_from:
        return
    if input_str := event.pattern_match.group(1):
        paytext = input_str
        pay = f"{paytext * 8}\n{paytext * 8}\n{paytext * 2}\n{paytext * 2}\n{paytext * 2}\n{paytext * 6}\n{paytext * 6}\n{paytext * 2}\n{paytext * 2}\n{paytext * 2}\n{paytext * 2}\n{paytext * 2}"
    else:
        pay = "╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯\n"
    # pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*8, paytext*8, paytext*2, paytext*2, paytext*2, paytext*6, paytext*6, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2)
    await event.edit(pay)
