import numpy as np
import matplotlib.pyplot as plt

# Constants
NUM_DETECTORS = 50          # Number of detectors in the ring
NUM_EVENTS = 1000           # Number of photon emission events
SOURCE_RADIUS = 0.5         # Radius of the source region (phantom model)
DETECTOR_RADIUS = 5         # Radius of the detector ring
CORRELATED_PROB = 0.7       # Probability that a photon pair is correlated

# Helper function to simulate photon emission
def generate_photon_pair():
    angle = np.random.uniform(0, 2 * np.pi)
    x_source = SOURCE_RADIUS * np.cos(angle)
    y_source = SOURCE_RADIUS * np.sin(angle)
    return (x_source, y_source)

# Function to detect photons and simulate scattering or randomness
def detect_photons(x, y, correlated=True):
    # True event: photon pairs are correlated (perfectly opposite)
    if correlated:
        angle1 = np.random.uniform(0, 2 * np.pi)
        angle2 = (angle1 + np.pi) % (2 * np.pi)  # Correlated angle opposite
    else:
        angle1 = np.random.uniform(0, 2 * np.pi)
        angle2 = np.random.uniform(0, 2 * np.pi)  # Uncorrelated angles
        
    # Detected position on the detector ring
    x1 = DETECTOR_RADIUS * np.cos(angle1)
    y1 = DETECTOR_RADIUS * np.sin(angle1)
    x2 = DETECTOR_RADIUS * np.cos(angle2)
    y2 = DETECTOR_RADIUS * np.sin(angle2)
    
    return (x1, y1), (x2, y2)

# Function to filter photon pairs based on angular correlation (parallel to entanglement)
def filter_photons(event_data):
    filtered_data = []
    for event in event_data:
        (x1, y1), (x2, y2), correlated = event
        delta_phi = np.arctan2(y2 - y1, x2 - x1)  # Angle difference
        
        if correlated and abs(delta_phi - np.pi) < np.pi / 4:  # Keep only "correlated" events
            filtered_data.append(((x1, y1), (x2, y2)))
            
    return filtered_data

# Simulation loop: Generating events and detecting photons
event_data = []
for _ in range(NUM_EVENTS):
    x, y = generate_photon_pair()
    correlated = np.random.uniform() < CORRELATED_PROB  # Decide if this pair is correlated
    
    photon1, photon2 = detect_photons(x, y, correlated)
    event_data.append((photon1, photon2, correlated))

# Filter the events based on our "entanglement" (angular correlation) concept
filtered_events = filter_photons(event_data)

# Visualization
def plot_events(events, title):
    plt.figure(figsize=(8, 8))
    circle = plt.Circle((0, 0), DETECTOR_RADIUS, color='b', fill=False)
    plt.gca().add_artist(circle)
    
    for (x1, y1), (x2, y2) in events:
        plt.plot([x1, x2], [y1, y2], 'r-', alpha=0.3)  # Line between detectors
        plt.plot(x1, y1, 'go')  # Detector hit
        plt.plot(x2, y2, 'go')  # Detector hit
    
    plt.xlim([-DETECTOR_RADIUS-1, DETECTOR_RADIUS+1])
    plt.ylim([-DETECTOR_RADIUS-1, DETECTOR_RADIUS+1])
    plt.title(title)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Plot unfiltered events
plot_events([(p1, p2) for p1, p2, _ in event_data], title="Unfiltered PET Events (Including Noise)")

# Plot filtered events (correlated photons only)
plot_events(filtered_events, title="Filtered PET Events (Correlated Photons)")

def plot_events_with_source(events, source_position, title):
    plt.figure(figsize=(8, 8))
    circle = plt.Circle((0, 0), DETECTOR_RADIUS, color='b', fill=False)
    plt.gca().add_artist(circle)
    
    for (x1, y1), (x2, y2) in events:
        plt.plot([x1, x2], [y1, y2], 'r-', alpha=0.3)  # Line between detectors
        plt.plot(x1, y1, 'go')  # Detector hit
        plt.plot(x2, y2, 'go')  # Detector hit
    
    # Plot the source region
    source_circle = plt.Circle(source_position, SOURCE_RADIUS, color='g', fill=False, linestyle='dotted', linewidth=2)
    plt.gca().add_artist(source_circle)
    
    plt.xlim([-DETECTOR_RADIUS-1, DETECTOR_RADIUS+1])
    plt.ylim([-DETECTOR_RADIUS-1, DETECTOR_RADIUS+1])
    plt.title(title)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Assume the source position is at the center of the phantom
source_position = (0, 0)  # Replace with the actual position if known

# Plot filtered events with the source region highlighted
plot_events_with_source(filtered_events, source_position, title="Filtered PET Events with Source Highlighted")
