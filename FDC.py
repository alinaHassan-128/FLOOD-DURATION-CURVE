# 1. INPUT FLOW DATA
# Upstream flow rate values of Guddu Barrage
up_flow = [
    73619, 63990, 60085, 53220, 52108, 48289, 49018, 50201, 55601, 55430,
    53826, 50980, 50249, 51324, 50362, 51670, 53744, 54701, 51899, 53667, 
    53336, 49788, 48380, 46146, 44511, 44213, 43411, 42365, 44742, 44742,
    45867, 47967
]

# Downstream flow rate values of Guddu Barrage
down_flow = [
    67328, 56623, 53601, 46372, 45788, 42549, 42696, 43879, 49279, 49329,
    47483, 44879, 43927, 45223, 44055, 44640, 47025, 47982, 45223, 46948,
    46660, 43201, 41933, 40066, 37732, 37434, 36632, 35586, 37963, 37963,
    39088, 41188
]


# 2. CALCULATING AVERAGE FLOW FOR EACH DAY

avg_flow = []  # empty list for storing average flows

for i in range(len(up_flow)):
    # Average flow = (Upstream + Downstream) / 2
    avg_flow.append((up_flow[i] + down_flow[i]) / 2)


# 3. SORTING THE AVERAGE FLOWS (ASCENDING ORDER)

sorted_avg_flow = sorted(avg_flow)

# 4. CORRECT RANK CALCULATION 
# Flow Duration Curve rule:
# Lowest flow → rank 32
# Highest flow → rank 1

ranks = []          # empty list for ranks
n = len(sorted_avg_flow)

# Simply assign decreasing ranks:
# Example for 32 flows → [32, 31, 30, ..., 1]
for i in range(n):
    ranks.append(n - i) 

# 5. FLOW DURATION FORMULA
# Formula: P = 100 × (M / (n + 1))
# M = rank
# n = total number of values

def flow_duration(M, n):
    return 100 * (M / (n + 1))

# 6. CALCULATE FLOW DURATION (%) FOR EACH RANK

flow_duration_list = []

for M in ranks:
    flow_duration_list.append(flow_duration(M, n))


# 7. PLOT THE FLOW DURATION CURVE

import matplotlib.pyplot as plt

plt.figure(figsize=(7, 5))

# Scatter plot: duration (%) on x-axis, flow on y-axis
plt.scatter(flow_duration_list, sorted_avg_flow)

plt.xlabel("Flow Duration (%)")
plt.ylabel("Flow Rate (cumecs)")
plt.title("Flow Duration Curve")
plt.grid(True)

plt.show()


# # # # # # # # # # # # # # #
# # #   APPLICATIONS  # # # # 
# # # # # # # # # # # # # # #

def getQ(target):
    # FUNCTION TO GET FLOW CORRESPONDING TO A GIVEN PERCENTILE

    # We assume the first index is the closest to target
    # Calculate distance from target for the first point    
    # Loop through all remaining points
    # If this point is closer to the target, update closest_index
    # Return flow corresponding to the closest index
    closest_index=0
    smallest_distance=abs(flow_duration_list[0]-target)  
    for i in range(1, len(flow_duration_list)):
        distance=abs(flow_duration_list[i]-target)
        if distance<smallest_distance:
            smallest_distance=distance 
            closest_index=i 
    return sorted_avg_flow[closest_index]               

Q5 = getQ(5)
Q10 = getQ(10)
Q90 = getQ(90)
Q95 = getQ(95)

# FUNCTION TO ASSESS FLOOD & DROUGHT RISK FOR A GIVEN FLOW
def checkRisk(flow_value):

    # ---------- FLOOD RISK CHECK ----------
    # Higher flow = greater flood danger
    
    if flow_value >= Q5:                   
        flood_risk = "Extreme Flood Risk"      # Very high flow
    elif flow_value >= Q10:
        flood_risk = "High Flood Risk"         # Moderately high flow
    else:
        flood_risk = "Low Flood Risk"          # Safe / normal flow


    # ---------- DROUGHT RISK CHECK ----------
    # Lower flow = greater drought danger
    
    if flow_value <= Q95:
        drought_risk = "Extreme Drought Risk"  # extremely low flow
    elif flow_value <= Q90:
        drought_risk = "High Drought Risk"     # moderately low flow
    else:
        drought_risk = "Low Drought Risk"      # safe / healthy flow levels


    # ---------- PRINT RESULT ----------
    print("---- RISK ASSESSMENT REPORT ----")
    print("Flood Status  :", flood_risk)
    print("Drought Status:", drought_risk)
    print("--------------------------------")


def hydropower():
    rho = 1000      # kg/m³
    g = 9.81        # m/s²
    head = 5        # meters (rough value for Guddu Barrage)
    cf = 0.65       # capacity factor

    # 1. Compute power for each FDC flow
    power_MW = []
    for Q in sorted_avg_flow:
        P_watts = rho * g * Q * head * cf
        power_MW.append(P_watts / 1e6)

    # 2. Compute energy for each segment
    time_fraction = []
    time_fraction.append((100 - flow_duration_list[0])/100)  # first value

    for i in range(1, len(flow_duration_list)):
        time_fraction.append((flow_duration_list[i-1] - flow_duration_list[i])/100)

    total_hours = 24 * 32
    energy_MWh = []  # energy contribution for each FDC segment

    for i in range(len(sorted_avg_flow)):
        energy = power_MW[i] * time_fraction[i] * total_hours
        energy_MWh.append(energy)

    # 3. Total monthly energy:
    total_energy_month = sum(energy_MWh)
    print("------------ HYDROPOWER ENERGY REPORT -----------")
    print("Total energy generated in 32 days (MWh):", total_energy_month)
    print("Energy consumed by an average household in 32 days (MWh): 1.7")
    print("Approximate number of houses that receive energy:", int(total_energy_month/1.7))
    print("-------------------------------------------------")


def water_demand():
    # Calculating flow exceedence for given percentiles
    Q80 = getQ(80)  # Flow exceeded 80% of the time
    Q95 = getQ(95)  # Flow exceeded 95% of the time (low flow)

    # Total demand calculation (sample values)
    crop_demand = 50000
    urban_demand = 10000
    industrial_demand = 20000
    total_demand = crop_demand + urban_demand + industrial_demand

    print("Total water demand:", total_demand, "cumecs")

    # RELIABILITY CHECK

    # Compare Q95 and Q80 with total demand to assess river reliability
    if Q95>=total_demand:
        reliability="River can reliably meet water demand even during low flows."
    elif Q80>=total_demand:
        reliability="River can meet demand most of the time but not during low flows"
    else:
        reliability="River CANNOT reliably meet total water demand."

    print("----------- TOTAL WATER DEMAND REPORT -----------")
    print("Reliability:", reliability)
    print("-------------------------------------------------")

def main():
    # ASKING USER WHICH APPLICATION THEY REQUIRE

    print ("1: Drought Analysis")
    print ("2: HydroPower Energy Calculation")
    print ("3: Agricultural Water Demand")
    choice = int(input('Please enter your choice of application 1 , 2 or 3 : '))
    if choice == 1:
        user_value = float(input("Enter current flow value: "))
        checkRisk(user_value)
    elif choice == 2:
        hydropower()
    elif choice == 3:
        water_demand()
    else:
        print ("Invalid input!")

main()