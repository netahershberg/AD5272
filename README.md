# AD5272 C++\python
📝 How to activate AD5272 with I2C&amp;python using FTDI's  function

This repository focuses on the **software side** of communicating with the **AD5272 digital potentiometer** using **FTDI** and both **C++ and Python** implementations.  
⚡ Before using the software, make sure that your AD5272 is properly **wired to the correct FTDI pins** and powered according to the datasheet.

🔹 Features
- C++ examples for I²C communication with AD5272
- Python WRAPPER script for testing and automation
- Flow diagrams and documentation for initialization & command sequences
- Support for writing RDAC and control registers

🔹 Requirements
- FTDI module (I²C capable)
- C++ compiler (MSVC / GCC / Clang)
- swig interface to connect C++ program to python

### 🔌 Part 1 – Initialize FTDI Communication
🔄 In this setup, I used **FTDI** as the communication interface.  
While not mandatory, FTDI was part of the environment I worked with, enabling a bridge between the PC and the target device as well for other peripherals on board.

🖧 Through the FTDI lines, I implemented **I²C communication**, using FTDI all-ready made function(which I'll explain ater here) mapping the pins to act as **SDA** and **SCL**.  
This allowed the computer to drive I²C transactions directly to the physical bus.

The first step is to work with the FTDI functions in C++. All the necessary functions can be found in this repository — the main changes are under i2c_test.cpp, where you’ll need to adjust the I²C address according to your setup and the data (words) you want to send.

<img src="https://www.python.org/static/community_logos/python-logo.png" width="100"/>  Once this is configured and tested, a Python wrapper can be used for easier interaction.

📐 Below is the schematic illustrating the electrical connection.
You can notice that for pin ADDR, which determines one out of three possible ways for addressing, GND is connecting there, so the ADDR is: A0=1, A1=1

<img width="385" height="251" alt="image" src="https://github.com/user-attachments/assets/f5bbc546-ee33-440a-a134-1f5f7fe579a2" />

**This video demonstrates the I²C write sequence to the AD5272 digital potentiometer, captured using a Saleae Logic Analyzer.  
It highlights the process of choosing the right slave address selection  according to your setup on - board\matrix and shows the data bytes being transmitted over the bus.**

🎬 You can watch here the full video that show the process--> https://youtu.be/QBl_sJ1qO30

demo here  ⬇️
https://github.com/user-attachments/assets/994c5b5e-93e7-4537-b7fe-cd90625dc2b7


### 🔌 Part 2 – C++ script implement write command
TBD

