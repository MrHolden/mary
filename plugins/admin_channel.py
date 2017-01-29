from cloudbot import hook


def mode_cmd(mode, text, text_inp, chan, conn, notice):
    """ generic mode setting function """
    split = text_inp.split(" ")
    if split[0].startswith("#"):
        channel = split[0]
        target = split[1]
        notice("Attempting to {} {} in {}...".format(text, target, channel))
        conn.send("PRIVMSG chanserv {} {} {}".format(mode, channel, target))
    else:
        channel = chan
        target = split[0]
        notice("Attempting to {} {} in {}...".format(text, target, channel))
        conn.send("PRIVMSG chanserv {} {} {}".format(mode, channel, target))


def mode_cmd_no_target(mode, text, text_inp, chan, conn, notice):
    """ generic mode setting function without a target"""
    split = text_inp.split(" ")
    if split[0].startswith("#"):
        channel = split[0]
        notice("Attempting to {} {}...".format(text, channel))
        conn.send("MODE {} {}".format(channel, mode))
    else:
        channel = chan
        notice("Attempting to {} {}...".format(text, channel))
        conn.send("MODE {} {}".format(channel, mode))


@hook.command()
def ban(text, conn, chan, notice):
    """[channel] <user> - bans <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("ban", "ban", text, chan, conn, notice)


@hook.command()
def unban(text, conn, chan, notice):
    """[channel] <user> - unbans <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("unban", "unban", text, chan, conn, notice)


@hook.command()
def halfop(text, conn, chan, notice):
    """[channel] <user> - halfops <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("halfop", "halfop", text, chan, conn, notice)


@hook.command()
def dehalfop(text, conn, chan, notice):
    """[channel] <user> - dehalfops <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("dehalfop", "dehalfop", text, chan, conn, notice)


@hook.command()
def voice(text, conn, chan, notice):
    """[channel] <user> - voices <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("voice", "voice", text, chan, conn, notice)


@hook.command()
def devoice(text, conn, chan, notice):
    """[channel] <user> - devoices <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("devoice", "devoice", text, chan, conn, notice)


@hook.command()
def op(text, conn, chan, notice):
    """[channel] <user> - ops <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("op", "op", text, chan, conn, notice)


@hook.command()
def deop(text, conn, chan, notice):
    """[channel] <user> - deops <user> in [channel], or in the caller's channel if no channel is specified"""
    mode_cmd("deop", "deop", text, chan, conn, notice)


@hook.command()
def kick(text, chan, conn, notice):
    """[channel] <user> - kicks <user> from [channel], or from the caller's channel if no channel is specified"""
    split = text.split(" ")

    if split[0].startswith("#"):
        channel = split[0]
        target = split[1]
        if len(split) > 2:
            reason = " ".join(split[2:])
            out = "KICK {} {}: {}".format(channel, target, reason)
        else:
            out = "KICK {} {}".format(channel, target)
    else:
        channel = chan
        target = split[0]
        if len(split) > 1:
            reason = " ".join(split[1:])
            out = "KICK {} {} :{}".format(channel, target, reason)
        else:
            out = "KICK {} {}".format(channel, target)

    notice("Attempting to kick {} from {}...".format(target, channel))
    conn.send(out)
