# AD5272 C++\python
📝 How to activate AD5272 with I2C&amp;python using FTDI's  function

### 🔌 Part 1 – Initialize FTDI Communication
🔄 In this setup, we used **FTDI** as the communication interface.  
While not mandatory, FTDI was part of the environment I worked with, enabling a bridge between the PC and the target device as well for other peripherals on board.

🖧 Through the FTDI lines, we implemented **I²C communication**, mapping the pins to act as **SDA** and **SCL**.  
This allowed the computer to drive I²C transactions directly to the physical bus.

This first requires working with the FTDI functions in C++, can find all the neccesry function in this repostiry - the main change will be under i2c_test. need to cahnge the address acording to your setup and the words you would like to send.
🐍 Once that is set up and working, a Python wrapper can be used

📷 Below is the schematic illustrating the connection.




**This video demonstrates the I²C write sequence to the AD5272 digital potentiometer, captured using a Saleae Logic Analyzer.  
It highlights the process of choosing the right slave address selection  according to your setup on - board\matrix and shows the data bytes being transmitted over the bus.**

https://github.com/user-attachments/assets/994c5b5e-93e7-4537-b7fe-cd90625dc2b7


<img width="936" height="148" alt="i2c transmition" src="https://github.com/user-attachments/assets/5e4cadb7-8a84-4497-8cbb-4732758aaa19" />
