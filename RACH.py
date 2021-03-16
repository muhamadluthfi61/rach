import matplotlib.pyplot as plt
import numpy as np
import random as rd

"""
Simple Simulation
System = Multi Channel slotted ALOHA
1 ms duration
With retransmission
No backoff duration

Device parameter is used to identify it's status:
- 0   : Not run yet
- 1   : Success in first try
- n   : Total transmissions until success
- 404 : Failed
"""

# The Function
# Return Average Ns and Nc
# Input explanation:
#   trials          = Number of simulations
#   channels/N      = Number of preamble can be used
#   devices/M       = Number of devices, in range (e.g. 10-100)
#   transmissions   = Number of maximum transmissions for devices
def MultiChannelSlottedALOHA(trials, channels, devices, transmissions):
    trials = trials
    channels = channels
    devices= devices
    transmissions = transmissions
    duration = 1 # Distribution of devices in 1 slot

    slot = 5 #RA timeslot interval
    time = [i for i in range(duration+2+((transmissions-1)*slot))] #timestamp

    # Define variable that want to be achieve
    averageSuccessProbability = [0] * len(devices)
    averageNs = [0] * len(devices)
    averageNc = [0] * len(devices)
    averageNi = [0] * len(devices)

    # To show simulation configuration
    print("Trials =", trials)
    print("Transmission =", transmissions)
    print("Devices =", devices)
    print("Channels =", channels)
    print("Duration =", duration)

    group = 0 # Simulation for first devices range / devices[0]

    while group < len(devices): # Run for all devices range
        device = [0] * devices[group] # Get device number as device list
        
        
        # Uniform distribution / Still working on, for now only 1 shot
        # Devices to timestamp
        loop = 1
        request = [0] * len(time)
        while loop <= duration:
            request[loop] = int(devices[group]/duration)
            loop += 1

        # Device timestamp to RA timeslot
        loop = 1
        pending = 0
        arrival = [0] * len(time)
        process = [0] * len(time)
        
        # Arrival process
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

        # For arrival + retransmit process
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
        
        # Contain all variable that want to be achieve
        # For each trial/simulation will be saved here
        successProbability = [0] * (trials)
        Nc = [0] * (trials)
        Ns = [0] * (trials)
        Ni = [0] * (trials)

        trial = 0 # Simulation for selected number of device

        while trial < trials: # Run device simulation as defined
            runningTime = 1 # Timeslot in simulation
            RAtimeSlot = 1 # Number of RA timeSlot
            success = [0] * len(time) # Save number of device that success in timeslot
            failed = [0] * len(time) # Save number of device that failed in timeslot
            choosenPreamble = [0] * len(time) # Save preamble number that used for each device in timeslot
            collisionChannel = [0] * len(time) # Save collision channel in timeslot
            successfulChannel = [0] * len(time) # Save successful channel in timeslot
            idleChannel = [0] * len(time) # Save idle channel in timeslot
            transmission = 1 # Mark number of transmission for device
            
            # #As log to check per trial
            # print("TRIAL =",trial+1)
            # print("--------------------------")
            
            while runningTime < len(time): # Run in time variable
                
                if(process[runningTime] != 0): # Check time that contain device request

                    # Initialize RA process
                    preambleIdx = []
                    availableChannel = [*range(0, channels, 1)]
                    failedPreambleIdx = []
                    successPreambleIdx = []
                    failedDevice = []
                    previousSuccessfulDevice = []
                        
                    # Each device randomly choose a number for RA
                    for i in range(0,process[runningTime]):
                        n = rd.randint(0,channels-1)
                        preambleIdx.append(n)
                    choosenPreamble[runningTime] = preambleIdx

                    # Check in RA process for channel that used > 1
                    for i in range(0,len(preambleIdx)):
                        for l in range(i+1,len(preambleIdx)):
                            if(preambleIdx[i]==preambleIdx[l]):
                                failedPreambleIdx.append(preambleIdx[l])        
                    failedPreambleIdx = list(dict.fromkeys(failedPreambleIdx))
                    collisionChannel[runningTime] = failedPreambleIdx # Save collision channels here for each runningTime

                    # Count and save number of failed device of each transmission
                    get_failed = lambda preambleIdx, xs: [i for (y, i) in zip(xs, range(len(xs))) if preambleIdx == y]
                    for i in range(0,len(failedPreambleIdx)):
                        failedDevice.append(get_failed(failedPreambleIdx[i],preambleIdx))

                    # Get successful devices in previous transmission
                    if(runningTime!=1):
                        get_device = lambda device, xs: [i for (y, i) in zip(xs, range(len(xs))) if device > y]
                        previousSuccessfulDevice = get_device(transmission,device)

                    # Save the failed device in the RA process, and if the same as previous device add 1
                    if(transmission<=transmissions):
                        for k in range(0,len(previousSuccessfulDevice)):
                            for i in range(0,len(failedDevice)):
                                for j in range(0,len(failedDevice[i])):
                                    if(failedDevice[i][j]>=previousSuccessfulDevice[k]):
                                        failedDevice[i][j] += 1                    
                    
                    # For first transmission only, marked all device as success
                    for i in range(0,process[runningTime]):
                        if(i<process[runningTime]):
                            if(device[i]==0):
                                device[i] = 1

                    # For failed device, add to next transmission. If the transmission more than defined one, change to failed status
                    for i in range(0,len(failedDevice)):
                        for j in range(0,len(failedDevice[i])):
                            if(failedDevice[i][j]<=len(device)):
                                device[failedDevice[i][j]] += 1
                                if(device[failedDevice[i][j]]>transmissions):
                                    device[failedDevice[i][j]] = 404
                    
                    # Get successful channels
                    successPreambleIdx = preambleIdx
                    for i in range(0,len(failedPreambleIdx)):
                        successPreambleIdx = list(filter(lambda a: a != failedPreambleIdx[i], successPreambleIdx))
                    successfulChannel[runningTime] = successPreambleIdx

                    # Get idle channels
                    idlePreambleIdx = availableChannel
                    for i in range(0,len(failedPreambleIdx)):
                        idlePreambleIdx = list(filter(lambda a: a != failedPreambleIdx[i], idlePreambleIdx))
                    for i in range(0,len(successPreambleIdx)):
                        idlePreambleIdx = list(filter(lambda a: a != successPreambleIdx[i], idlePreambleIdx))
                    idleChannel[runningTime] = idlePreambleIdx
                    
                    success[runningTime] = len(successPreambleIdx) # Get number of success devices in time running
                    failed[runningTime] = process[runningTime]-success[runningTime] # Get number of failed devices in time running

                    # The next transmission, use failed devices
                    if(runningTime < max(time)-1):
                        process[runningTime+slot] = failed[runningTime]

                    transmission += 1 # Transmission number added
                    
                    # Save the variable result
                    Ni[trial] = Ni[trial] + len(idleChannel[runningTime])
                    Nc[trial] = Nc[trial] + len(collisionChannel[runningTime])
                    Ns[trial] = Ns[trial] + len(successfulChannel[runningTime])

                    # For checking
                    # print("Time Slot =",RAtimeSlot)
                    # print("Device =", process[runningTime])
                    # print("Avaiable Channel =", availableChannel)
                    # print("Choosen Preamble =", choosenPreamble[runningTime])
                    # print("Collision Channel =", collisionChannel[runningTime])
                    # print("Successful Channel =", successfulChannel[runningTime])
                    # print("Idle Channel =", idleChannel[runningTime])
                    # print("Success Device =", success[runningTime])
                    # print("Failed Device =", failed[runningTime])
                    # print("Device Status =", device)
                    # print("--------------------------")

                    # To stop simulation
                    if(failed[runningTime]==0):
                        runningTime=len(time)

                    RAtimeSlot += 1 # Add count of RA timeslot

                runningTime += 1 # Add count of running time

            # Save the variable result
            totalSuccess = sum(success)
            totalFailed = sum(failed)
            successProbability[trial] = totalSuccess/(devices[group])

            # For checking
            # print("Success =", totalSuccess)
            # print("Success Probability =", successProbability[trial])
            # print("=============================")
            
            trial += 1

        # Formulate the variable that what to achieved
        averageNs[group] = sum(Ns)/len(Ns)
        averageNc[group] = sum(Nc)/len(Nc)
        averageNi[group] = sum(Ni)/len(Ni)

        averageSuccessProbability[group] = sum(successProbability) / len(successProbability)
        
        # For checking
        # print("Success Probability =", successProbability)
        # print("Average Success Probability =", averageSuccessProbability[group])
        
        group += 1 # For the next devices number

    return (averageNs, averageNc) # Return result, can change here

# For N = 3 Scenario 

figure1 = plt.figure(1)

trials = 1 
channels = 3
devices = [*range(2, 31, 1)] 
transmissions = 1

averageNs, averageNc = MultiChannelSlottedALOHA(trials, channels, devices, transmissions)

MN = [x / channels for x in devices]
NsN = [x / channels for x in averageNs]
NcN = [x / channels for x in averageNc]

plt.plot(MN, NsN, 'o-', label='N = 3, Success Channel')
plt.plot(MN, NcN, 'o--', label='N = 3, Collision Channel')

# For N = 14 Scenario

trials = 1 #retry
channels = 14
devices = [*range(2, 141, 1)] #devices range
transmissions = 1

averageNs, averageNc = MultiChannelSlottedALOHA(trials, channels, devices, transmissions)

MN = [x / channels for x in devices]
NsN = [x / channels for x in averageNs]
NcN = [x / channels for x in averageNc]

plt.plot(MN, NsN, '-', label='N = 14, Success Channel')
plt.plot(MN, NcN, '--', label='N = 14, Collision Channel')

equationNs = [0] * len(devices)
equationNc = [0] * len(devices)

for i in range(0,len(equationNs)):
    equationNs[i] = devices[i] * np.exp(-devices[i]/channels)

for i in range(0,len(equationNc)):
    equationNc[i] = channels - (devices[i] * np.exp(-devices[i]/channels)) - (channels * np.exp(-devices[i]/channels))

equationNsN = [x / channels for x in equationNs]
equationNcN = [x / channels for x in equationNc]

plt.plot(MN, equationNsN, ':', label='Ns Equation')
plt.plot(MN, equationNcN, '-.', label='Nc Equation')

plt.xlabel('M/N')
plt.ylabel('RAOs/N')

#plt.xlim(min(devices), max(devices))

plt.title('Multi Channel Slotted Aloha')

# plt.xticks(devices, devices)
#plt.yticks(averageSuccessProbability, averageSuccessProbability)

plt.legend()

plt.show()