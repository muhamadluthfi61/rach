import matplotlib.pyplot as plt
import numpy as np
import random as rd

"""
RACH Configuration
"""
numberOfRA_Preambles = [4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64] #n
preambleTransMax = [3,4,5,6,7,8,10,20,50,100,200] #n
ra_ResponseWindowSize = [2,3,4,5,6,7,8,10] #sf
mac_ContentionResolutionTimer = [8,16,24,32,40,48,56,64] #sf

"""
Simple Simulation
System = Multichannel slotted ALOHA
1 ms duration
With retransmission
No backoff duration

To-do list:
1. Retransmission mechanism
2. Success probability per arrival

Device parameter is used to identify it's status:
- 0   : Not run yet
- 1   : Success in first try
- n   : Total transmissions until success
- 404 : Failed
"""

trials = 1 #retry
channels = 15
devices = [*range(50, 151, 10)] #devices range
totaltransmissions = 10
duration = 1

slot = 5 #timeslot range
time = [i for i in range(duration+2+((totaltransmissions-1)*slot))] #timestamp

averageSuccessProbability = [0] * len(devices)

print("Trials = ", trials)
print("Transmission = ", totaltransmissions)
print("Devices = ", devices)
print("Channels = ", channels)
print("Duration = ", duration)

group = 0
while group < len(devices):
    device = [0] * devices[group]
    #Uniform distribution

    #Devices to timestamp
    loop = 1
    request = [0] * len(time)
    while loop <= duration:
        request[loop] = int(devices[group]/duration)
        loop += 1

    #Device timestamp to timeslot
    loop = 1
    pending = 0
    arrival = [0] * len(time)
    process = [0] * len(time)
    
    while loop <= duration+1:
        if(loop == 1):
            arrival[loop] = request[loop]
            aloha = slot + 1
        elif(loop%slot != 1):
            pending += request[loop]
        elif(loop%slot == 1):
            arrival[loop] = pending + request[loop]
            pending = 0
            aloha += slot 
        loop += 1

    loop = 1
    pending = 0
    while loop <= duration+1:
        if(loop == 1):
            process[loop] = request[loop]
            aloha = slot + 1
        elif(loop%slot != 1):
            pending += request[loop]
        elif(loop%slot == 1):
            process[loop] = pending + request[loop]
            pending = 0
            aloha += slot 
        loop += 1

    #Count timeslot
    """totalTimeSlot = 0
    for i in range(0,len(process)):
        if(process[i]!=0):
            totalTimeSlot += 1
    """
    """
    Print timeslot
    print("Total Time Slot = ",totalTimeSlot)
    print("===========================")
    """
    
    #Procedure  
    
    successProbability = [0] * (trials)

    trial = 0
    while trial < trials:
        loop = 1
        timeSlot = 1
        success = [0] * len(time)
        failed = [0] * len(time)
        choosenPreamble = [0] * len(time)
        collisionChannel = [0] * len(time)
        successfulChannel = [0] * len(time)
        barrier = 0
        transmission = 1
        
        # #Per trial
        # print("TRIAL = ",trial+1)
        # print("--------------------------")
        
        while loop < len(time):
            
            if(process[loop] != 0):
                preambleIdx = []
                failedPreambleIdx = []
                successPreambleIdx = []
                failedDevice = []
                previousSuccessfulDevice = []
                    
                for i in range(0,process[loop]):
                    n = rd.randint(0,channels)
                    preambleIdx.append(n)
                choosenPreamble[loop] = preambleIdx

                for i in range(0,len(preambleIdx)):
                    for l in range(i+1,len(preambleIdx)):
                        if(preambleIdx[i]==preambleIdx[l]):
                            failedPreambleIdx.append(preambleIdx[l])        
                failedPreambleIdx = list(dict.fromkeys(failedPreambleIdx))
                collisionChannel[loop] = failedPreambleIdx

                get_failed = lambda preambleIdx, xs: [i for (y, i) in zip(xs, range(len(xs))) if preambleIdx == y]
                for i in range(0,len(failedPreambleIdx)):
                    failedDevice.append(get_failed(failedPreambleIdx[i],preambleIdx))

                #UNDER DEVELOPMENT, IDENTIFY SUCCESSFULL DEVICES
                if(loop!=1):
                    get_device = lambda device, xs: [i for (y, i) in zip(xs, range(len(xs))) if device > y]
                    previousSuccessfulDevice = get_device(transmission,device)

                if(transmission<=totaltransmissions):
                    for k in range(0,len(previousSuccessfulDevice)):
                        for i in range(0,len(failedDevice)):
                            for j in range(0,len(failedDevice[i])):
                                if(failedDevice[i][j]>=previousSuccessfulDevice[k]):
                                    failedDevice[i][j] += 1
                    
                #UNTIL HERE

                for i in range(0,process[loop]):
                    if(i<process[loop]):
                        #device[barrier+i] = 1
                        if(device[i]==0):
                            device[i] = 1

                for i in range(0,len(failedDevice)):
                    for j in range(0,len(failedDevice[i])):
                        if(failedDevice[i][j]<=len(device)):
                            #device[barrier+failedDevice[i][j]] = 404
                            device[failedDevice[i][j]] += 1
                            if(device[failedDevice[i][j]]>totaltransmissions):
                                device[failedDevice[i][j]] = 404
                
                successPreambleIdx = preambleIdx
                for i in range(0,len(failedPreambleIdx)):
                    successPreambleIdx = list(filter(lambda a: a != failedPreambleIdx[i], successPreambleIdx))
                successfulChannel[loop] = successPreambleIdx
                
                success[loop] = len(successPreambleIdx)
                failed[loop] = process[loop]-success[loop]

                if(loop < max(time)-1):
                    process[loop+slot] = failed[loop]

                barrier = barrier+process[loop]
                transmission += 1
                
                #For checking
                # print("Time Slot = ",timeSlot)
                # print("Device = ", process[loop])
                # print("Choosen Preamble = ", choosenPreamble[loop])
                # print("Collision Channel = ", collisionChannel[loop])
                # print("Successful Channel = ", successfulChannel[loop])
                # print("Success Device = ", success[loop])
                # print("Failed Device = ", failed[loop])
                # print("Device Status = ", device)
                # print("--------------------------")
                
                if(failed[loop]==0):
                    loop=len(time)

                timeSlot += 1
                               
            loop += 1
        totalSuccess = sum(success)
        totalFailed = sum(failed)
        successProbability[trial] = totalSuccess/(devices[group])
        
        #Success probability in 1 try
        # print("Success = ", totalSuccess)
        # print("Success Probability = ", successProbability[trial])
        # print("=============================")
        
        trial += 1

    averageSuccessProbability[group] = sum(successProbability) / len(successProbability)
    
    #Success probability after retries
    # print("Success Probability = ", successProbability)
    # print("Average Success Probability = ", averageSuccessProbability[group])
    
    group += 1
    
#Plotting

averageSuccessProbability = list(np.round(averageSuccessProbability, 3))
plt.plot(devices, averageSuccessProbability, 'bo-', label='line 1' )

plt.xlabel('Devices')
plt.ylabel('Success Probability')

plt.xlim(min(devices), max(devices))

plt.title('Multi Channel Slotted Aloha')

# plt.xticks(devices, devices)
#plt.yticks(averageSuccessProbability, averageSuccessProbability)

plt.legend()

plt.show()


