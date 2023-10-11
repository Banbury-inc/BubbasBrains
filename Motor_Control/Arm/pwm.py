if __name__=='__main__':
    controller = I2C_Controller(0x40, debug=False)
    controller.setPWMFreq(50)
    while True:
        for i in range(500,2500,10):
            controller.Set_Pulse(15,i)   #setting 15th pin of the servo header(forward direction)
            sleep(0.05)
   
        for i in range(2500,500,-10):
            controller.Set_Pulse(15,i)   #setting 15th pin of the servo header(backward direction)
            sleep(0.05)