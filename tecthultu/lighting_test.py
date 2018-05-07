from ola.ClientWrapper import ClientWrapper
import array

"""Python 2 script to test operation of PAR lights with the DMX interface."""

def DmxHandler(status):
    if status.Succeeded():
        print('Success!')
    else:
        print('Error: ' + status.message)

if __name__ == '__main__':
    #Write to the 1st 8 channels. The array must be 512 bytes long, so all channels have a value.
    #Not doing this can result to undefined behaviour.

    #Set the light to fade mode, blue color, 75% speed/
    arr = array.array('B', [140, 80, 192, 0, 0, 0, 0, 0] + [0] * 504)

    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(0, arr, DmxHandler)
    #wrapper.Run()
