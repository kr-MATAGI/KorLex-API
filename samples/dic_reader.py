

###
if "__main__" == __name__:
    with open("../dic/krx_syn.idx", mode='rb') as f:
        for data in f.readlines():
            print(type(data))
            print(data.decode("ascii", errors="ignore")) # Not Right Decode sentence
            break