from gc import mem_alloc, mem_free

def show_mem(message=False):
    used = mem_alloc()
    free = mem_free()
    total = used + free
    if message:
        print(message)
    print("Memory used :" + str(used) + " KB (" + str(total / used) + "%)\n")