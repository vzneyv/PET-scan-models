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

# Function to calculate intersection of a photon line with the detector ring
def photon_to_detector(x_source, y_source, angle):
    dx = np.cos(angle)
    dy = np.sin(angle)
    
    a = dx**2 + dy**2
    b = 2 * (x_source * dx + y_source * dy)
    c = x_source**2 + y_source**2 - DETECTOR_RADIUS**2
    discriminant = b**2 - 4 * a * c
    
    if discriminant < 0:
        return None, None
    
    sqrt_discriminant = np.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)
    
    x1 = x_source + t1 * dx
    y1 = y_source + t1 * dy
    x2 = x_source + t2 * dx
    y2 = y_source + t2 * dy
    
    return (x1, y1), (x2, y2)

# Function to detect photons and simulate scattering or randomness
def detect_photons(x_source, y_source, correlated=True):
    angle1 = np.random.uniform(0, 2 * np.pi)
    photon1, _ = photon_to_detector(x_source, y_source, angle1)
    
    if correlated:
        angle2 = (angle1 + np.pi) % (2 * np.pi)
    else:
        angle2 = np.random.uniform(0, 2 * np.pi)
    
    photon2, _ = photon_to_detector(x_source, y_source, angle2)
    
    return photon1, photon2

# Function to filter photon pairs based on angular correlation (delta-phi)
def filter_photons(event_data):
    filtered_data = []
    for event in event_data:
        (x1, y1), (x2, y2), correlated = event
        if (x1 is not None and y1 is not None and x2 is not None and y2 is not None):
            # Calculate the angle between the lines
            delta_phi = np.arctan2(y2 - y1, x2 - x1)
            if correlated and (abs(delta_phi) >= np.pi - np.pi/4 and abs(delta_phi) <= np.pi + np.pi/4):
                filtered_data.append(((x1, y1), (x2, y2)))
            elif not correlated:
                filtered_data.append(((x1, y1), (x2, y2)))
    return filtered_data

# Simulation loop: Generating events and detecting photons
event_data = []
for _ in range(NUM_EVENTS):
    x_source, y_source = generate_photon_pair()
    correlated = np.random.uniform() < CORRELATED_PROB
    
    photon1, photon2 = detect_photons(x_source, y_source, correlated)
    event_data.append((photon1, photon2, correlated))

# Filter the events based on our "entanglement" (angular correlation) concept
filtered_events = filter_photons(event_data)

# Visualization
def plot_events(events, title):
    plt.figure(figsize=(8, 8))
    circle = plt.Circle((0, 0), DETECTOR_RADIUS, color='b', fill=False)
    plt.gca().add_artist(circle)
    
    source_position = (0, 0)  # Assuming the source is at the origin
    source_circle = plt.Circle(source_position, SOURCE_RADIUS, color='g', fill=False, linestyle='dotted', linewidth=2)
    plt.gca().add_artist(source_circle)

    for (x1, y1), (x2, y2) in events:
        if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
            plt.plot([x1, x2], [y1, y2], 'r-', alpha=0.3)  # Line between detectors
            plt.plot(x1, y1, 'go')  # Detector hit
            plt.plot(x2, y2, 'go')  # Detector hit

    plt.xlim([-DETECTOR_RADIUS-1, DETECTOR_RADIUS+1])
    plt.ylim([-DETECTOR_RADIUS-1, DETECTOR_RADIUS+1])
    plt.title(title)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()
    

# Plot unfiltered events
plot_events([(p1, p2) for p1, p2, _ in event_data], title="Unfiltered PET Events (Including Noise)")

# Plot filtered events (correlated photons only)
plot_events(filtered_events, title="Filtered PET Events (Correlated Photons)")
