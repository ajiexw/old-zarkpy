import web
def printEnv():
    for k, v in web.ctx.env.items():
        print k,':\t',v
    exit(0)
