import matplotlib.pyplot as plt
def draw(x1,y1,x2,y2):
    del_X=(x2-x1)
    del_y=(y2-y1)
    steps=max(abs(del_X),abs(del_y))
    x_incr=del_X/steps
    y_incr=del_y/steps
    plot_x=[x1]
    plot_y=[y1]

    print("DEL_X", del_X)
    print("DEL_Y",del_y)
    print("x_incr",x_incr)
    print("y_incr",y_incr)
    for _ in range(steps):
        x1=(x1+x_incr)
        y1=(y1+y_incr)
        plot_x.append(round(x1))
        plot_y.append(round(y1))
    print(plot_x)
    print(plot_y)    
    
    plt.plot(plot_x,plot_y)
    plt.show()

x1=int(input("Enter x1:"))
y1=int(input("Enter y1:"))
x2=int(input("Enter x2:"))
y2=int(input("Enter y2:"))
draw(x1,y1,x2,y2)
