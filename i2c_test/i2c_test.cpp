extern "C" {
    #include "ftdi_i2c.h"
}

#define SLAVE_ADDRESS 0x2f // Replace with your I2C slave address

int main() {
    FT_HANDLE handle;
    FT_STATUS status;
    DWORD numChannels;
    DWORD sizeTransferred;
    UCHAR writeBuffer[2] = { 0x08, 0x00 }; // Data to write
    UCHAR readBuffer[2]; // Buffer to store read data

    Init_libMPSSE();

    // Initialize the library and get the number of channels
    status = I2C_GetNumChannels(&numChannels);
    if (status != FT_OK) {
        printf("Failed to get number of channels. Status: %d\n", status);
        return -1;
    }

    // Open the first available channel
    status = I2C_OpenChannel(1, &handle);
    if (status != FT_OK) {
        printf("Failed to open channel. Status: %d\n", status);
        return -1;
    }

    // Configure the channel
    ChannelConfig config;
    config.ClockRate = I2C_CLOCK_STANDARD_MODE;
    config.LatencyTimer = 2;
    config.Options = 0; // No special options

    status = I2C_InitChannel(handle, &config);
    if (status != FT_OK) {
        printf("Failed to initialize channel. Status: %d\n", status);
        I2C_CloseChannel(handle);
        return -1;
    }

    // Write two bytes to the slave
    status = I2C_DeviceWrite(handle, SLAVE_ADDRESS, 2, writeBuffer, &sizeTransferred, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK || sizeTransferred != 2) {
        printf("Failed to write to device. Status: %d\n", status);
        I2C_CloseChannel(handle);
        return -1;
    }

    // Read two bytes from the slave
    status = I2C_DeviceRead(handle, SLAVE_ADDRESS, 2, readBuffer, &sizeTransferred, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK || sizeTransferred != 2) {
        printf("Failed to read from device. Status: %d\n", status);
        I2C_CloseChannel(handle);
        return -1;
    }

    // Print the read data
    printf("Read data: 0x%02X 0x%02X\n", readBuffer[0], readBuffer[1]);

    // Close the channel
    I2C_CloseChannel(handle);

    return 0;
}
