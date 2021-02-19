from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random
import time
from time import mktime
import datetime

z = 0
monkey_stage = 0
mcol = 2
has_prev_key_release = False
main_time = 0
time_s, tot_time = 0, 0
pt, pend, pstart = 0, 0, 0
paused = False
startflag = 1
endexec = False
savetime = 0
has_prev_key_release = False
bonus_health = False
monkey_speed = False
side_switch = False


def hello():
    print('Hello, world!')


class Ball(object):
    def __init__(self, canvas, x=10, y=10, radius=10,
                 color="red", speed=1, dropped=False):
        self.canvas = canvas
        self.speed = speed
        self.dropped = dropped
        self.canvas_id = canvas.create_oval(
          x-radius, y-radius, x+radius, y+radius, outline=color, fill=color)


def monkey_move():
    global monkey_stage
    global mleft
    if mleft:
            canvas.itemconfig(monkey, image=iml[(monkey_stage+1) % 24])
    else:
            canvas.itemconfig(monkey, image=imr[(monkey_stage+1) % 24])
    monkey_stage += 1


def move(event):
    global mleft, side_switch
    global mcol
    xmov = 0
    moved = False
    """Move the sprite image with a d w and s when click them"""
    if side_switch:
        if mcol == 0 and event.char == "a":
            xmov = 1195
            mcol = 5
            moved = True
        elif mcol == 5 and event.char == "d":
            xmov = -1195
            mcol = 0
            moved = True

    if event.char == "a" and mcol != 0 and not moved:
        if mcol == 2 or mcol == 4:
            xmov = -475
            mcol -= 1
        elif mcol == 1 or mcol == 3 or mcol == 5:
            xmov = -80
            mcol -= 1

    elif event.char == "d" and mcol != 5 and not moved:
        if mcol == 1 or mcol == 3:
            xmov = 475
            mcol += 1
        elif mcol == 0 or mcol == 2 or mcol == 4:
            xmov = 80
            mcol += 1

    canvas.move(monkey, xmov, 0)
    canvas.itemconfig(monkey, image=iml[monkey_stage % 24])

    if xmov != 0:
        if mleft:
            mleft = False
        else:
            mleft = True


def on_key_release(event):
    global has_prev_key_release
    has_prev_key_release = None


def on_key_press(event):
    global monkey_speed
    if monkey_speed:
        m = 30
    else:
        m = 15
    if event.char == "w":
        canvas.move(monkey, 0, -m)
    else:
        canvas.move(monkey, 0, m)


def on_key_release_repeat(event):
    global has_prev_key_release
    has_prev_key_release = win.after_idle(on_key_release, event)


def on_key_press_repeat(event):
    global has_prev_key_release
    global monkey_speed
    if monkey_speed:
        m = 30
    else:
        m = 15
    if has_prev_key_release:
        win.after_cancel(has_prev_key_release)
        has_prev_key_release = None
        if event.char == "w":
            canvas.move(monkey, 0, -m)
        else:
            canvas.move(monkey, 0, m)
    else:
        on_key_press(event)


def make_ball(pos="z"):
    if pos == "z":
        a = random.randint(0, 5)
        if a == 0:
            ball = Ball(canvas, ws//2-50, hs//2-300, 20, "saddle brown", 20)
        elif a == 1:
            ball = Ball(canvas, ws//2+75, hs//2-300, 20, "saddle brown", 20)
        elif a == 2:
            ball = Ball(canvas, ws//2-650, hs//2-300, 20, "saddle brown", 20)
        elif a == 3:
            ball = Ball(canvas, ws//2-450, hs//2-300, 20, "saddle brown", 20)
        elif a == 4:
            ball = Ball(canvas, ws//2+450, hs//2-300, 20, "saddle brown", 20)
        elif a == 5:
            ball = Ball(canvas, ws//2+650, hs//2-300, 20, "saddle brown", 20)
    else:
        ball = Ball(canvas, float(pos[:pos.index(",")]),
                    hs//2-300, 20, "saddle brown", 1, True)

    balls.append(ball)


def overlapping(mnk, ccn):
    if ((canvas.coords(mnk)[0]-70 <
         canvas.coords(ccn.canvas_id)[2] and canvas.coords(mnk)[0]+70 >
         canvas.coords(ccn.canvas_id)[2]) and (canvas.coords(mnk)[1]-85 <
        canvas.coords(ccn.canvas_id)[3] and canvas.coords(mnk)[1]+85 >
         canvas.coords(ccn.canvas_id)[3])):

        return True
    elif ((canvas.coords(mnk)[0]-70 <
           canvas.coords(ccn.canvas_id)[0] and canvas.coords(mnk)[0]+70 >
           canvas.coords(ccn.canvas_id)[0]) and (canvas.coords(mnk)[1]-85 <
          canvas.coords(ccn.canvas_id)[1] and canvas.coords(mnk)[1]+85 >
           canvas.coords(ccn.canvas_id)[1])):

        return True
    return False


def reposition(s1):
    # balls.remove(ball)
    # canvas.delete(s1.canvas_id)
    a = random.randint(0, 5)
    if a == 0:
        m = ws//2-50 - canvas.coords(s1.canvas_id)[0] - 20
    elif a == 1:
        m = ws//2+60 - canvas.coords(s1.canvas_id)[0] - 20
    elif a == 2:
        m = ws//2-650 - canvas.coords(s1.canvas_id)[0] + 30
    elif a == 3:
        m = ws//2-450 - canvas.coords(s1.canvas_id)[0] - 45
    elif a == 4:
        m = ws//2+450 - canvas.coords(s1.canvas_id)[0] + 30
    elif a == 5:
        m = ws//2+650 - canvas.coords(s1.canvas_id)[0] - 45

    canvas.move(s1.canvas_id, m, -(canvas.coords(s1.canvas_id)[1]//2+325))
    if not s1.dropped:
        s1.dropped = True
    # print(canvas.coords(s))


def pause_game(event):
    global paused, pt, pstart, pend, time_s, replay_image
    global quit_image, quitter, replayer, bossimage, bimg
    global pause_text
    if time_s-savetime.seconds > 5:

        if event.char == "p":
            win.unbind("<Key>")
            win.unbind("<KeyRelease-w>")
            win.unbind("<KeyPress-w>")
            win.unbind("<KeyRelease-s>")
            win.unbind("<KeyPress-s>")
            win.unbind("<KeyPress-b>")
            quitter.place(x=ws//2-200, y=hs//2+180, anchor=N)
            replayer.place(x=ws//2+200, y=hs//2+180, anchor=N)
            if not paused:
                paused = True
                pause_text = canvas.create_text(ws//2, hs//2-150,
                                                font=("Purisa", 50),
                                                text="PAUSED")
                pstart = datetime.datetime.now()
            else:
                canvas.itemconfig(pause_text, text="Resuming in 3...")
                win.update()
                time.sleep(1)
                canvas.itemconfig(pause_text, text="Resuming in 2...")
                win.update()
                time.sleep(1)
                canvas.itemconfig(pause_text, text="Resuming in 1...")
                win.update()
                paused = False
                pend = (datetime.datetime.now()+datetime
                        .timedelta(microseconds=1200000))
                pt = pend - pstart
                win.bind("<Key>", move)
                win.bind("<KeyRelease-w>", on_key_release_repeat)
                win.bind("<KeyPress-w>", on_key_press_repeat)
                win.bind("<KeyRelease-s>", on_key_release_repeat)
                win.bind("<KeyPress-s>", on_key_press_repeat)
                win.bind("<KeyPress-b>", pause_game)
                quitter.place_forget()
                replayer.place_forget()
                canvas.delete(pause_text)
                time.sleep(1)

        elif event.char == "b":
            win.unbind("<Key>")
            win.unbind("<KeyRelease-w>")
            win.unbind("<KeyPress-w>")
            win.unbind("<KeyRelease-s>")
            win.unbind("<KeyPress-s>")
            win.unbind("<KeyPress-p>")
            if not paused:
                paused = True
                pstart = datetime.datetime.now()
                pause_text = canvas.create_text(ws//2, hs//2-150,
                                                font=("Purisa", 50),
                                                text="PAUSED")
                bimg = canvas.create_image(ws//2, hs//2-50, image=bossimage)
            else:
                canvas.delete(bimg)
                win.update()
                canvas.itemconfig(pause_text, text="Resuming in 3...")
                win.update()
                time.sleep(1)
                canvas.itemconfig(pause_text, text="Resuming in 2...")
                win.update()
                time.sleep(1)
                canvas.itemconfig(pause_text, text="Resuming in 1...")
                win.update()
                paused = False
                pend = (datetime.datetime.now()+datetime
                        .timedelta(microseconds=1200000))
                pt = pend - pstart
                win.bind("<Key>", move)
                win.bind("<KeyRelease-w>", on_key_release_repeat)
                win.bind("<KeyPress-w>", on_key_press_repeat)
                win.bind("<KeyRelease-s>", on_key_release_repeat)
                win.bind("<KeyPress-s>", on_key_press_repeat)
                win.bind("<KeyPress-p>", pause_game)
                quitter.place_forget()
                replayer.place_forget()
                canvas.delete(pause_text)
                time.sleep(1)


def insert_score(vals, names, tt):
    if len(vals) == 0:
        vals[0:0] = [tt]
        names[0:0] = ["NAM"]
    else:
        for z in vals:
            if tt > z and tt not in vals:
                insert_pos = vals.index(z)
                vals[insert_pos:insert_pos] = [tt]
                names[insert_pos:insert_pos] = ["NAM"]
    if tt not in vals:
        vals.append(tt)
        names.append("NAM")


def highscore(vals, names, tt):
    highscore = canvas.create_text(ws//2, hs//2-140, anchor=N, fill="white",
                                   font=("Purisa", 30),
                                   text="New All Time High Score!")
    insert_score(vals, names, tt)


def boardscore(vals, names, tt):
    board = canvas.create_text(ws//2, hs//2-140, anchor=N, fill="white",
                               font=("Purisa", 30),
                               text="New Top 5 Score!")
    insert_score(vals, names, tt)


def quitgame():
    global endexec, startgame
    MsgBox = messagebox.askyesno('Exit Application',
                                 'Are you sure you want to quit?',
                                 icon='warning')
    if MsgBox:
        if startgame:
            if not endexec:
                MsgBox2 = messagebox.askyesno('Exit Application',
                                              '''Would you like to
                                               save progress and quit?
                                               Any unsaved changes
                                               will be lost.''',
                                              icon='warning')
                if MsgBox2:
                    save_game()
                home_return()
            else:
                home_return()
        else:
            win.destroy()
    else:
        pass


def restart():
    MsgBox = messagebox.askyesno('Restart Application',
                                 'Are you sure you want to restart?',
                                 icon='warning')
    if MsgBox:
        canvas.delete("all")
        win.destroy()
        initialiser()
    else:
        pass


def save_game():
    global bonus_health, monkey_speed, side_switch
    with open("savefile.txt", "w") as save:
        save.write(str(len(balls))+"\n")
        for x in balls:
            save.write(str(canvas.coords(x.canvas_id)[0] + 20) +
                       "," + str(canvas.coords(x.canvas_id)[0] + 20) +
                       "\n")
        print(canvas.coords(monkey))
        save.write(str(canvas.coords(monkey)[0])+"\n")
        save.write(str(canvas.coords(monkey)[1])+"\n")
        save.write(str(mleft)+"\n")
        save.write(str(mcol)+"\n")
        save.write(str(len(hearts))+"\n")
        save.write(str((main_time.seconds//60) % 60)+"\n")
        save.write(str((main_time.seconds) % 60)+"\n")
        save.write(str(main_time.microseconds)+"\n")
        if bonus_health or monkey_speed or side_switch:
            save.write("T"+"\n")
        else:
            save.write("F"+"\n")


def temp_ghost():
    global ghost
    ghost = False


def mover(s1, s2):
    global fintime, paused, startflag, main_time, endexec, savetime
    global bonus_health, monkey_speed, side_switch, ghost, cc_act_val
    global hearts, ccv

    if len(hearts) > 0 and not paused:
        moved = False
        if canvas.coords(s1.canvas_id)[-3] > hs-50:
            reposition(s1)

        if not overlapping(monkey, s1):
            dmin = 99999
            for x in [z for z in balls
                      if canvas.coords(z.canvas_id)[0] == canvas.coords(
                        s1.canvas_id)[0]]:
                k = -(canvas.coords(s1.canvas_id)[1]-canvas.coords(
                  x.canvas_id)[1])
                if k < dmin and k > 0:
                    dmin = k
            if dmin != 0 and (dmin > 300 or (not s1.dropped)):
                canvas.move(s1.canvas_id, 0, 3+int(time_s)/10)

        else:
            if not ghost:
                ghost = True
                reposition(s1)
                canvas.delete("heart_"+str(len(hearts)-1))
                hearts.pop(len(hearts)-1)
                canvas.move(monkey, 0, 125)
                canvas.after(2000, temp_ghost)
            else:
                dmin = 99999
                for x in [z for z in balls
                          if canvas.coords(z.canvas_id)[0] == canvas.coords(
                            s1.canvas_id)[0]]:
                    k = -(canvas.coords(s1.canvas_id)[1]-canvas.coords(
                      x.canvas_id)[1])
                    if k < dmin and k > 0:
                        dmin = k
                if dmin != 0 and (dmin > 300 or (not s1.dropped)):
                    canvas.move(s1.canvas_id, 0, 3+int(time_s)/10)

        if balls.index(s1) == len(balls)-1:
            startflag = 0
    elif len(hearts) == 0 and not endexec:
        win.unbind("<Key>")
        win.unbind("<KeyRelease-w>")
        win.unbind("<KeyPress-w>")
        win.unbind("<KeyRelease-s>")
        win.unbind("<KeyPress-s>")
        win.unbind("<KeyPress-p>")
        # win.unbind("<KeyPress-b>") remains binded
        canvas.create_rectangle(ws//2-300, hs//2-250, ws//2+300,
                                hs//2+250, fill="black")
        txt = canvas.create_text(ws//2, hs//2-220, anchor=N,
                                 fill="white", font=("Purisa", 30),
                                 text="Game Over!")
        scores = []
        with open("leaderboard.txt") as board:
            scores = board.read().split()
        vals = [int(x) for x in scores if scores.index(x) % 2]
        names = [x for x in scores if not scores.index(x) % 2]
        tt = main_time.seconds*1000+main_time.microseconds//1000
        userscore = canvas.create_text(ws//2, hs//2-180, anchor=N,
                                       fill="white", font=("Purisa", 30),
                                       text="Your Score: "+str(tt))

        if not cheat_used:
            if len(vals) == 0:
                highscore(vals, names, tt)
            elif tt > vals[0]:
                highscore(vals, names, tt)
            elif len(vals) < 5:
                boardscore(vals, names, tt)
            elif tt > vals[min(4, len(vals)-1)]:
                boardscore(vals, names, tt)
        else:
            endtext = canvas.create_text(ws//2, hs//2-140, anchor=N,
                                         fill="white", font=("Purisa", 30),
                                         text="Score Not Saved - Code Used")

        if len(vals) < 5:
            border = len(vals)
            # print(border,"t")
        else:
            border = 5
            # print(border)

        canvas.create_text(ws//2-200, hs//2-80, anchor=N,
                           fill="white", font=("Purisa", 16),
                           text="Position")
        canvas.create_text(ws//2, hs//2-80, anchor=N,
                           fill="white", font=("Purisa", 16),
                           text="Name")
        canvas.create_text(ws//2+200, hs//2-80, anchor=N,
                           fill="white", font=("Purisa", 16),
                           text="Score")
        for x in range(border):
            canvas.create_text(ws//2-200, hs//2-80+40*(x+1),
                               anchor=N, fill="white", font=("Purisa", 16),
                               text=x+1)
        for x in range(border):
            canvas.create_text(ws//2, hs//2-80+40*(x+1),
                               anchor=N, fill="white", font=("Purisa", 16),
                               text=names[x])
        for x in range(border):
            canvas.create_text(ws//2+200, hs//2-80+40*(x+1),
                               anchor=N, fill="white", font=("Purisa", 16),
                               text=vals[x])
        if border < 5:
            for x in range(5-border):
                canvas.create_text(ws//2-200, hs//2-80+40*(x+border+1),
                                   anchor=N, fill="white",
                                   font=("Purisa", 16), text=5-x)
            for x in range(5-border):
                canvas.create_text(ws//2, hs//2-80+40*(x+border+1),
                                   anchor=N, fill="white",
                                   font=("Purisa", 16), text="---")
            for x in range(5-border):
                canvas.create_text(ws//2+200, hs//2-80+40*(x+border+1),
                                   anchor=N, fill="white",
                                   font=("Purisa", 16), text="-----")

        with open("leaderboard.txt", "w") as lboard:
            for x in range(len(vals)):
                lboard.write(names[x]+" "+str(vals[x])+"\n")

        endexec = True

        quitter.place(x=ws//2-200, y=hs//2+180, anchor=N)
        replayer.place(x=ws//2+200, y=hs//2+180, anchor=N)
        with open("savefile.txt", "w") as save:
            save.write("No_Save_Data!")


def update_time():
    global pt, pstart, pend, st, main_time, time_s, savetime
    # delta = datetime.datetime.fromtimestamp(mktime(savetime))
    ct = datetime.datetime.now()+savetime
    if pt != 0:
        tdiff = ct-st
        tdiff = tdiff - pt
        st += pt
        pt, pstart, pend = 0, 0, 0
    else:
        tdiff = ct-st
        mins = str(((tdiff).seconds//60) % 60)
        main_time = tdiff
        time_s = tdiff.seconds
        # print(tdiff)
        # tot_time = tdiff.microseconds
        secs = str(((tdiff).seconds) % 60).zfill(2)
        milsecs = str((tdiff).microseconds//1000).zfill(3)
        timetext = mins+":"+secs+"."+milsecs
        canvas.itemconfig(timeplayed, text=timetext)


def cloudfall(c):
    global paused
    if len(hearts) > 0 and not paused:
        if canvas.coords(c)[1] > hs:
            canvas.move(c, 0, -(canvas.coords(c)[1]//2+450))
        else:
            canvas.move(c, 0, 3+int(time_s)/10)


def animator():
    global startflag, delta, nopause, delta, time_s, savetime, clouds, paused
    # print(paused)
    if len(hearts) > 0 and not paused:
        update_time()
        canvas.after(200, monkey_move)
        for ball in balls:
            canvas.after(-500*(startflag-1) +
                         (500*startflag*balls.index(ball)),
                         mover, ball, balls[balls.index(ball)-1])
        for cloud in clouds:
            canvas.after(2000*clouds.index(cloud), cloudfall, cloud)
    canvas.after(30, animator)
    if time_s-savetime.seconds > 5:
        canvas.delete(nopause)
    if time_s-savetime.seconds == 12 and len(balls) < 2:
        make_ball()
    if time_s-savetime.seconds == 24 and len(balls) < 3:
        make_ball()
    if time_s-savetime.seconds == 36 and len(balls) < 4:
        make_ball()
    if time_s-savetime.seconds == 48 and len(balls) < 5:
        make_ball()
    if time_s-savetime.seconds == 60 and len(balls) < 6:
        make_ball()


def initialiser():
    global tree_1, tree_2, tree_3, monkey, mleft, timelabel
    global timeplayed, balls, hearts, z, monkey_stage, mcol
    global has_prev_key_release, main_time, time_s, tot_time
    global pt, pend, pstart, paused, startflag, endexec, t1, t2
    global ws, hs, win, canvas, replay_image, quit_image, mkl, mkr
    global imagelist, iml, imr, st, savetime, nopause, pause_image
    global quitter, replayer, bossimage, bonus_health, c1, c2
    global c_im1, clouds, sun, sunrise, startgame, ghost, heart_img

    print("Loading... Please Wait...")
    win = Tk()
    win.title("Gorilla War")
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    win.geometry('%dx%d' % (ws, hs))

    win.bind("<KeyRelease-w>", on_key_release_repeat)
    win.bind("<KeyPress-w>", on_key_press_repeat)
    win.bind("<KeyRelease-s>", on_key_release_repeat)
    win.bind("<KeyPress-s>", on_key_press_repeat)
    win.bind("<KeyPress-p>", pause_game)
    win.bind("<KeyPress-b>", pause_game)
    win.bind("<Key>", move)

    win.title('Hello, Tkinter!')
    win.attributes('-topmost', 1)
    win.attributes('-topmost', 0)
    win.focus_force()

    canvas = Canvas(win, bg="DeepSkyBlue4", width=ws, height=hs)

    canvas.pack()

    ghost = False

    balls = []
    hearts = []
    clouds = []
    monkey_x = ws//2-ws//50
    monkey_y = hs//2-65

    mleft = True

    if not bonus_health:
        len_hearts = 3
    else:
        len_hearts = 5
    mcol = 2
    savetime = datetime.timedelta(minutes=0, seconds=0, microseconds=0)

    with open("savefile.txt") as savegame:
        savedata = savegame.read().strip().split("\n")
        # print(savedata)
        if len(savedata) > 2:
            num_ccn = int(savedata[0])
            for x in range(1, num_ccn+1):
                make_ball(savedata[x])
            monkey_x = float(savedata[num_ccn+1])
            monkey_y = float(savedata[num_ccn+2])
            mleft = (savedata[num_ccn+3])
            if mleft == "False":
                mleft = False  # Tricky!
            else:
                mleft = True
            mcol = int(savedata[num_ccn+4])
            len_hearts = int(savedata[num_ccn+5])

            delta = [savedata[num_ccn+6], savedata[num_ccn+7],
                     savedata[num_ccn+8]]
            savetime = datetime.timedelta(minutes=int(delta[0]),
                                          seconds=int(delta[1]),
                                          microseconds=int(delta[2]))

    z = 0
    monkey_stage = 0
    has_prev_key_release = False
    main_time = 0
    time_s, tot_time = 0, 0
    pt, pend, pstart = 0, 0, 0
    paused = False
    startflag = 1
    endexec = False

    t1 = PhotoImage(file='tree.png')
    quit_image = PhotoImage(file="quit.png")
    replay_image = PhotoImage(file="replay.png")
    pause_image = PhotoImage(file="nopause.png").subsample(25, 25)
    bossimage = PhotoImage(file="bossimage.PNG").subsample(2, 2)
    sunrise = PhotoImage(file="sunrise.png").subsample(2, 2)
    c_im1 = PhotoImage(file="cloud.png").subsample(2, 2)
    heart_img = PhotoImage(file="heart.png").subsample(10, 10)

    c1 = canvas.create_image(ws//2-275, -50, image=c_im1)
    clouds.append(c1)
    c2 = canvas.create_image(ws//2+275, -50, image=c_im1)
    clouds.append(c2)
    sun = canvas.create_image(ws//2, hs-250, image=sunrise)

    mkl = PhotoImage(file='mkl.png')
    mkr = PhotoImage(file='mkr.png')
    t2 = t1.subsample(2, 1)

    imagelist = ["monkey_run_1.png", "monkey_run_2.png", "monkey_run_3.png",
                 "monkey_run_4.png", "monkey_run_5.png", "monkey_run_6.png",
                 "monkey_run_7.png", "monkey_run_8.png"]

    iml, imr = [], []

    for imagefile in imagelist:
        photor = PhotoImage(file="lmp001/"+imagefile)
        photol = PhotoImage(file="lmp002/"+imagefile)
        iml.append(photol)
        iml.append(photol)
        iml.append(photol)
        imr.append(photor)
        imr.append(photor)
        imr.append(photor)

    tree_1 = canvas.create_image(ws//2, hs//2-250, image=t2)
    tree_2 = canvas.create_image(ws//2-550, hs//2-250, image=t2)
    tree_3 = canvas.create_image(ws//2+550, hs//2-250, image=t2)
    nopause = canvas.create_image(50, 50, image=pause_image)

    monkey = canvas.create_image(monkey_x, monkey_y, image=mkl)

    timelabel = canvas.create_text(ws//2+300, 0, anchor=NW,
                                   font=("Purisa", 16), text="Time: ",
                                   fill="white")
    timeplayed = canvas.create_text(ws//2+375, 0, anchor=NW,
                                    font=("Purisa", 16), text="0:00.000",
                                    fill="white")

    quitter = Button(win, bg="black", image=quit_image,
                     width="250", height="120",
                     command=lambda: quitgame())
    replayer = Button(win, bg="black", image=replay_image,
                      width="250", height="120",
                      command=lambda: restart())

    if len(balls) == 0:
        for i in range(1):
            make_ball()

    for x in range(len_hearts):
        canvas.create_image(ws//2-300+x*50, 30, image=heart_img,
                            tag="heart_"+str(x))
        hearts.append("H")

    st = datetime.datetime.now()
    startgame = True

    animator()


def opening():
    global ws, hs, quit_out, title_img
    quit_out.place(x=0, y=0, anchor=NW)
    centralbox = canvas.create_rectangle(ws//2-300, hs//2-300,
                                         ws//2+300, hs//2+300,
                                         fill="black")
    starttext = canvas.create_image(ws//2, hs//2-250,
                                    anchor=N,
                                    image=title_img)
    starter_text = canvas.create_text(ws//2, hs//2+100,
                                      anchor=N, fill="white",
                                      font=("Purisa", 30),
                                      text="PRESS G TO GO!")


def options():
    global instr
    canvas.delete("all")
    load_game_b.place_forget()
    new_game_b.place_forget()
    options_b.place_forget()
    mainbox = canvas.create_rectangle(ws//2-400, 100, ws//2+400,
                                      hs-100, fill="black")
    inst = canvas.create_image(ws//2, hs//2, image=instr)


def load_cheat(loader="f"):
    global bonus_health, monkey_speed, side_switch, bon_h_val, speed_b_val
    global ete_j_val, cc_act_val, cheat_used
    # win.withdraw()
    code = simpledialog.askstring(title="Secret Code",
                                  prompt="Enter Secret Code: ")
    if code is not None:
        if code.upper() == "M0R3L1F3":
            if loader != "f":
                if not bonus_health:
                    MsgBox = messagebox.showinfo("Code Activated",
                                                 '''Congratulations! Secret
                                                  Code Accepted''')
                    canvas.itemconfig(bon_h_val, text="Y")
                    canvas.itemconfig(cc_act_val, text="Y")
                    cheat_used = True
                    bonus_health = True
                else:
                    MsgBox = messagebox.showinfo("Code Unavailable",
                                                 '''This Secret Code has
                                                  already been
                                                  activated''',
                                                 icon="warning")
            else:
                MsgBox = messagebox.showinfo("Code Unavailable",
                                             '''The MOR3L1F3 code
                                              grants extra hearts - however
                                              this is not available on an
                                              existing save''',
                                             icon="warning")

        elif code.upper() == "R34LF45T":
            if not monkey_speed:
                MsgBox = messagebox.showinfo("Code Activated",
                                             '''Congratulations!
                                              Secret Code Accepted''')
                canvas.itemconfig(speed_b_val, text="Y")
                canvas.itemconfig(cc_act_val, text="Y")
                cheat_used = True
                monkey_speed = True
            else:
                MsgBox = messagebox.showinfo("Code Unavailable",
                                             '''This Secret Code has
                                              already been activated''',
                                             icon="warning")

        elif code.upper() == "SW1TCHUP":
            if not side_switch:
                MsgBox = messagebox.showinfo("Code Activated",
                                             '''Congratulations! Secret
                                              Code Accepted''')
                canvas.itemconfig(ete_j_val, text="Y")
                canvas.itemconfig(cc_act_val, text="Y")
                cheat_used = True
                side_switch = True
            else:
                MsgBox = messagebox.showinfo("Code Unavailable",
                                             '''This Secret Code has
                                              already been activated''',
                                             icon="warning")
        else:
            MsgBox = messagebox.showinfo("Code Unavailable",
                                         "Invalid Secret Code",
                                         icon="warning")


def load_board():
    global codes, board
    canvas.delete("all")
    codes.place_forget()
    board.place_forget()
    startup.place_forget()

    canvas.create_rectangle(ws//2-300, hs//2-250, ws//2+300, hs//2+250,
                            fill="black")
    scores = []
    with open("leaderboard.txt") as board:
        scores = board.read().split()
        vals = [int(x) for x in scores if scores.index(x) % 2]
        names = [x for x in scores if not scores.index(x) % 2]
        userscore = canvas.create_text(ws//2, hs//2-180, anchor=N,
                                       fill="white", font=("Purisa", 30),
                                       text="Current Leaderboard (Top 5):")

    if len(vals) < 5:
        border = len(vals)
    else:
        border = 5

    canvas.create_text(ws//2-200, hs//2-80, anchor=N,
                       fill="white", font=("Purisa", 16), text="Position")
    canvas.create_text(ws//2, hs//2-80, anchor=N,
                       fill="white", font=("Purisa", 16), text="Name")
    canvas.create_text(ws//2+200, hs//2-80, anchor=N,
                       fill="white", font=("Purisa", 16), text="Score")
    for x in range(border):
        canvas.create_text(ws//2-200, hs//2-80+40*(x+1),
                           anchor=N, fill="white", font=("Purisa", 16),
                           text=x+1)
    for x in range(border):
        canvas.create_text(ws//2, hs//2-80+40*(x+1), anchor=N,
                           fill="white", font=("Purisa", 16), text=names[x])
    for x in range(border):
        canvas.create_text(ws//2+200, hs//2-80+40*(x+1), anchor=N,
                           fill="white", font=("Purisa", 16), text=vals[x])
    if border < 5:
        for x in range(5-border):
            canvas.create_text(ws//2-200, hs//2-80+40*(x+border+1),
                               anchor=N, fill="white", font=("Purisa", 16),
                               text=5-x)
        for x in range(5-border):
            canvas.create_text(ws//2, hs//2-80+40*(x+border+1), anchor=N,
                               fill="white", font=("Purisa", 16),
                               text="---")
        for x in range(5-border):
            canvas.create_text(ws//2+200, hs//2-80+40*(x+border+1), anchor=N,
                               fill="white", font=("Purisa", 16),
                               text="-----")


def start_game():
    MsgBox = messagebox.askyesno('Start Application',
                                 'Are you sure you want to start?',
                                 icon='warning')
    if MsgBox:
        canvas.delete("all")
        win.destroy()
        initialiser()
    else:
        pass


def load_game():
    global load_game_b, new_game_b, options_b, codes, board, bon_h_val
    global speed_b_val, ete_j_val, cc_act_val, cheat_used
    load_game_b.place_forget()
    new_game_b.place_forget()
    options_b.place_forget()
    canvas.delete("all")

    with open("savefile.txt") as savegame:
        savedata = savegame.read().strip().split("\n")
        num_ccns = int(savedata[0])
        mcol = int(savedata[num_ccns+4])+1
        len_hearts = savedata[num_ccns+5]
        delta = [savedata[num_ccns+6], savedata[num_ccns+7],
                 savedata[num_ccns+8]]
        cheat_used = savedata[num_ccns+9]
        if cheat_used == "T":
            cheatused_text = "Y"
        else:
            cheatused_text = "N"

    mainbox = canvas.create_rectangle(ws//2-700, 100, ws//2+100,
                                      hs-100, fill="black")
    sidebox = canvas.create_rectangle(ws//2+300, 100, ws//2+600,
                                      hs-100, fill="black")
    mid = canvas.create_rectangle(ws//2+100, 100, ws//2+300,
                                  hs-100, fill="black")

    main_posx = (canvas.coords(mainbox)[0]+canvas.coords(mainbox)[2])//2
    main_posy = (canvas.coords(mainbox)[1]+canvas.coords(mainbox)[3])//2
    codes.place(x=main_posx, y=main_posy-100, anchor=N)
    board.place(x=main_posx, y=main_posy+100, anchor=N)
    startup.place(x=main_posx, y=main_posy-300, anchor=N)

    pos_x = (canvas.coords(sidebox)[0]+canvas.coords(sidebox)[2])//2
    pos_y = (canvas.coords(sidebox)[1]+canvas.coords(sidebox)[3])//2

    stats = canvas.create_text(pos_x, pos_y-300, anchor=N, fill="white",
                               font=("Purisa", 16), text="GAME STATS")

    num_cc = canvas.create_text(pos_x-50, pos_y-225, anchor=N, fill="white",
                                font=("Purisa", 12), text="Time Played: ")
    num_ccn = canvas.create_text(pos_x+100, pos_y-225, anchor=N,
                                 fill="white", font=("Purisa", 12),
                                 text=(delta[0]+":"+delta[1]
                                       .zfill(2)+"."+delta[2][:3].zfill(3)))

    num_h = canvas.create_text(pos_x-50, pos_y-175, anchor=N, fill="white",
                               font=("Purisa", 12),
                               text="Number of hearts: ")
    num_hs = canvas.create_text(pos_x+100, pos_y-175, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text=len_hearts)

    num_m = canvas.create_text(pos_x-50, pos_y-125, anchor=N,
                               fill="white", font=("Purisa", 12),
                               text="Number of coconuts: ")
    num_mk = canvas.create_text(pos_x+100, pos_y-125, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text=num_ccns)

    num_t = canvas.create_text(pos_x-50, pos_y-75, anchor=N,
                               fill="white", font=("Purisa", 12),
                               text="Current monkey column: ")
    num_tp = canvas.create_text(pos_x+100, pos_y-75, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text=mcol)

    cheats = canvas.create_text(pos_x, pos_y+50, anchor=N,
                                fill="white", font=("Purisa", 16),
                                text="SECRET CODES")

    bon_h = canvas.create_text(pos_x-50, pos_y+100, anchor=N,
                               fill="white", font=("Purisa", 12),
                               text="Bonus Health: ")
    bon_h_val = canvas.create_text(pos_x+100, pos_y+100, anchor=N,
                                   fill="white", font=("Purisa", 12),
                                   text="N")

    speed_b = canvas.create_text(pos_x-50, pos_y+150, anchor=N,
                                 fill="white", font=("Purisa", 12),
                                 text="Speed Boost: ")
    speed_b_val = canvas.create_text(pos_x+100, pos_y+150, anchor=N,
                                     fill="white", font=("Purisa", 12),
                                     text="N")

    ete_j = canvas.create_text(pos_x-50, pos_y+200, anchor=N,
                               fill="white", font=("Purisa", 12),
                               text="End to End Jumping: ")
    ete_j_val = canvas.create_text(pos_x+100, pos_y+200, anchor=N,
                                   fill="white", font=("Purisa", 12),
                                   text="N")

    cc_act = canvas.create_text(pos_x-50, pos_y+250, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text="Secret Code Used: ")
    cc_act_val = canvas.create_text(pos_x+100, pos_y+250, anchor=N,
                                    fill="white", font=("Purisa", 12),
                                    text=cheatused_text)


def opening_screen():
    global win, ws, hs, canvas, mkl, quit_image, load_game_b, new_game_b
    global options_b, codes, board, startup, quit_out, homepage, startgame
    global load_save, new_game_img, options_image, home_image, start_game_img
    global entercode, leader_img, bonus_health, monkey_speed, side_switch
    global title_img, instr
    win = Tk()
    win.title("Grease Monkey")
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    win.geometry('%dx%d' % (ws, hs))
    startgame = False
    win.title('Hello, Tkinter!')

    canvas = Canvas(win, bg="DeepSkyBlue4", width=ws, height=hs)

    canvas.pack()
    win.bind("<KeyPress-g>", go)
    mkl = PhotoImage(file="mkl.png")
    bonus_health = False
    monkey_speed = False
    side_switch = False

    # Images created using CoolText.com
    quit_image = PhotoImage(file="quit.png")
    home_image = PhotoImage(file="home.png")
    load_save = PhotoImage(file="loadsave.png")
    new_game_img = PhotoImage(file="newgame.png")
    options_image = PhotoImage(file="options.png")
    start_game_img = PhotoImage(file="startgame.png")
    entercode = PhotoImage(file="entercode.png")
    leader_img = PhotoImage(file="leaderboard.png")
    title_img = PhotoImage(file="title.png")
    instr = PhotoImage(file="instructions.PNG").subsample(2, 2)
    # Images created using CoolText.com
    with open("savefile.txt") as save:
        savedata = save.read().strip().split()
        if len(savedata) < 3:
            load_game_b = Button(win, bg="black", image=load_save,
                                 width="350", height="150",
                                 state="disabled",
                                 command=lambda: load_game())
        else:
            load_game_b = Button(win, bg="black", image=load_save,
                                 width="350", height="150", state="normal",
                                 command=lambda: load_game())
    new_game_b = Button(win, bg="black", image=new_game_img,
                        width="350", height="150",
                        command=lambda: new_game())
    options_b = Button(win, bg="black", image=options_image, width="350",
                       height="150", command=lambda: options())
    codes = Button(win, bg="black", image=entercode, width="400",
                   height="150", command=lambda: load_cheat("t"))
    board = Button(win, bg="black", image=leader_img, width="400",
                   height="150", command=lambda: load_board())
    startup = Button(win, bg="black", image=start_game_img, width="400",
                     height="150", command=lambda: start_game())
    quit_out = Button(win, bg="black", image=quit_image, width="250",
                      height="120", command=lambda: quitgame())
    homepage = Button(win, bg="black", image=home_image, width="250",
                      height="120", command=lambda: home_return())

    opening()


def home_return():
    win.destroy()
    opening_screen()


def new_game():
    global load_game_b, new_game_b, options_b, codes, board, bon_h_val
    global speed_b_val, ete_j_val, cc_act_val, cheat_used
    cheat_used = False

    load_game_b.place_forget()
    new_game_b.place_forget()
    options_b.place_forget()
    canvas.delete("all")
    mainbox = canvas.create_rectangle(ws//2-700, 100, ws//2+100,
                                      hs-100, fill="black")
    sidebox = canvas.create_rectangle(ws//2+300, 100, ws//2+600, hs-100,
                                      fill="black")
    mid = canvas.create_rectangle(ws//2+100, 100, ws//2+300, hs-100,
                                  fill="black")
    main_posx = (canvas.coords(mainbox)[0]+canvas.coords(mainbox)[2])//2
    main_posy = (canvas.coords(mainbox)[1]+canvas.coords(mainbox)[3])//2
    codes.place(x=main_posx, y=main_posy-100, anchor=N)
    board.place(x=main_posx, y=main_posy+100, anchor=N)
    startup.place(x=main_posx, y=main_posy-300, anchor=N)

    pos_x = (canvas.coords(sidebox)[0]+canvas.coords(sidebox)[2])//2
    pos_y = (canvas.coords(sidebox)[1]+canvas.coords(sidebox)[3])//2
    stats = canvas.create_text(pos_x, pos_y-300, anchor=N,
                               fill="white", font=("Purisa", 16),
                               text="GAME STATS")

    num_cc = canvas.create_text(pos_x-50, pos_y-225, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text="Time Played: ")
    num_ccn = canvas.create_text(pos_x+100, pos_y-225, anchor=N,
                                 fill="white", font=("Purisa", 12),
                                 text="0:00.000")

    num_h = canvas.create_text(pos_x-50, pos_y-175, anchor=N,
                               fill="white", font=("Purisa", 12),
                               text="Number of hearts: ")
    num_hs = canvas.create_text(pos_x+100, pos_y-175,
                                anchor=N, fill="white", font=("Purisa", 12),
                                text="3")

    num_m = canvas.create_text(pos_x-50, pos_y-125, anchor=N,
                               fill="white", font=("Purisa", 12),
                               text="Number of coconuts: ")
    num_mk = canvas.create_text(pos_x+100, pos_y-125, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text="1")

    num_t = canvas.create_text(pos_x-50, pos_y-75, anchor=N, fill="white",
                               font=("Purisa", 12),
                               text="Current monkey column: ")
    num_tp = canvas.create_text(pos_x+100, pos_y-75, anchor=N, fill="white",
                                font=("Purisa", 12), text="3")

    cheats = canvas.create_text(pos_x, pos_y+50, anchor=N, fill="white",
                                font=("Purisa", 16), text="SECRET CODES")

    bon_h = canvas.create_text(pos_x-50, pos_y+100, anchor=N, fill="white",
                               font=("Purisa", 12), text="Bonus Health: ")
    bon_h_val = canvas.create_text(pos_x+100, pos_y+100, anchor=N,
                                   fill="white", font=("Purisa", 12),
                                   text="N")

    speed_b = canvas.create_text(pos_x-50, pos_y+150, anchor=N,
                                 fill="white", font=("Purisa", 12),
                                 text="Speed Boost: ")
    speed_b_val = canvas.create_text(pos_x+100, pos_y+150, anchor=N,
                                     fill="white", font=("Purisa", 12),
                                     text="N")

    ete_j = canvas.create_text(pos_x-50, pos_y+200, anchor=N, fill="white",
                               font=("Purisa", 12),
                               text="End to End Jumping: ")
    ete_j_val = canvas.create_text(pos_x+100, pos_y+200, anchor=N,
                                   fill="white", font=("Purisa", 12),
                                   text="N")

    cc_act = canvas.create_text(pos_x-50, pos_y+250, anchor=N,
                                fill="white", font=("Purisa", 12),
                                text="Secret Code Used: ")
    cc_act_val = canvas.create_text(pos_x+100, pos_y+250, anchor=N,
                                    fill="white", font=("Purisa", 12),
                                    text="N")


def go(event):
    global load_game_b, new_game_b, options_b, quit_out, homepage
    # print(ws,hs)
    if event.char == "g":
        win.unbind("<KeyPress-g>")
        quit_out.place_forget()
        homepage.place(x=0, y=0, anchor=NW)
        canvas.delete("all")
        mainbox = canvas.create_rectangle(ws//2-400, 100, ws//2+400,
                                          hs-100, fill="black")
        starter_text = canvas.create_text(ws//2, hs//2-400, anchor=N,
                                          fill="black", font=("Purisa", 30),
                                          text="MAIN MENU")
        load_game_b.place(x=ws//2, y=150, anchor=N)
        new_game_b.place(x=ws//2, y=350, anchor=N)
        options_b.place(x=ws//2, y=550, anchor=N)


def load_home():
    global load_game_b, new_game_b, options_b, quitter, homepage
    # print(ws,hs)
    homepage.place(x=0, y=0, anchor=NW)
    canvas.delete("all")
    mainbox = canvas.create_rectangle(ws//2-400, 100, ws//2+400,
                                      hs-100, fill="black")
    starter_text = canvas.create_text(ws//2, hs//2-400, anchor=N,
                                      fill="black", font=("Purisa", 30),
                                      text="MAIN MENU")
    load_game_b.place(x=ws//2, y=150, anchor=N)
    new_game_b.place(x=ws//2, y=350, anchor=N)
    options_b.place(x=ws//2, y=550, anchor=N)


opening_screen()


win.mainloop()
