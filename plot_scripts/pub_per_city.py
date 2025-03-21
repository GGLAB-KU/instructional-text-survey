# This produces Fig. 4. Geographical distribution of publications
import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Sample data (replace with your data)
city_data = [
    {'city': 'Kharagpur', 'lat': 22.3174, 'lon': 87.3064, 'publications': 1},
    {'city': 'Mountain View', 'lat': 37.3861, 'lon': -122.0839, 'publications': 1},
    {'city': 'Abu Dhabi', 'lat': 24.4539, 'lon': 54.3773, 'publications': 1},
    {'city': 'Adelaide', 'lat': -34.9285, 'lon': 138.6007, 'publications': 1},
    {'city': 'Amherst', 'lat': 42.3736, 'lon': -72.5249, 'publications': 3},
    {'city': 'Ann Arbor', 'lat': 42.2808, 'lon': -83.7430, 'publications': 1},
    {'city': 'Atlanta', 'lat': 33.7490, 'lon': -84.3880, 'publications': 2},
    {'city': 'Austin', 'lat': 30.2672, 'lon': -97.7431, 'publications': 1},
    {'city': 'Beijing', 'lat': 39.9042, 'lon': 116.4074, 'publications': 7},
    {'city': 'Boston', 'lat': 42.3601, 'lon': -71.0589, 'publications': 2},
    {'city': 'Brescia', 'lat': 45.5416, 'lon': 10.2118, 'publications': 1},
    {'city': 'Cambridge Massachusetts', 'lat': 42.3736, 'lon': -71.1097, 'publications': 4},
    {'city': 'Canberra', 'lat': -35.2809, 'lon': 149.1300, 'publications': 1},
    {'city': 'Champaign', 'lat': 40.1164, 'lon': -88.2434, 'publications': 6},
    {'city': 'Chapel Hill', 'lat': 35.9132, 'lon': -79.0558, 'publications': 1},
    {'city': 'Chicago', 'lat': 41.8781, 'lon': -87.6298, 'publications': 2},
    {'city': 'Columbus', 'lat': 39.9612, 'lon': -82.9988, 'publications': 1},
    {'city': 'Darmstadt', 'lat': 49.8728, 'lon': 8.6512, 'publications': 1},
    {'city': 'Delft', 'lat': 52.0116, 'lon': 4.3571, 'publications': 1},
    {'city': 'Edinburgh', 'lat': 55.9533, 'lon': -3.1883, 'publications': 2},
    {'city': 'Freiburg im Breisgau', 'lat': 47.9990, 'lon': 7.8421, 'publications': 1},
    {'city': 'Galway', 'lat': 53.2707, 'lon': -9.0568, 'publications': 1},
    {'city': 'Ghent', 'lat': 51.0543, 'lon': 3.7174, 'publications': 2},
    {'city': 'Guangzhou', 'lat': 23.1291, 'lon': 113.2644, 'publications': 1},
    {'city': 'Hong Kong', 'lat': 22.3193, 'lon': 114.1694, 'publications': 1},
    {'city': 'Ikoma', 'lat': 34.6801, 'lon': 135.7010, 'publications': 1},
    {'city': 'Irvine', 'lat': 33.6846, 'lon': -117.8265, 'publications': 1},
    {'city': 'Ithaca', 'lat': 42.4430, 'lon': -76.5019, 'publications': 2},
    {'city': 'Kanpur', 'lat': 26.4499, 'lon': 80.3319, 'publications': 1},
    {'city': 'Kyoto', 'lat': 35.0116, 'lon': 135.7681, 'publications': 3},
    {'city': 'kyoto', 'lat': 35.0116, 'lon': 135.7681, 'publications': 3},
    {'city': 'Liverpool', 'lat': 53.4084, 'lon': -2.9916, 'publications': 1},
    {'city': 'London', 'lat': 51.5074, 'lon': -0.1278, 'publications': 2},
    {'city': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437, 'publications': 1},
    {'city': 'Munich', 'lat': 48.1351, 'lon': 11.5820, 'publications': 1},
    {'city': 'Maryland', 'lat': 39.0458, 'lon': -76.6413, 'publications': 1},
    {'city': 'Melbourne', 'lat': -37.8136, 'lon': 144.9631, 'publications': 1},
    {'city': 'Menlo Park', 'lat': 37.4529, 'lon': -122.1817, 'publications': 3},
    {'city': 'New Delhi', 'lat': 28.6139, 'lon': 77.2090, 'publications': 5},
    {'city': 'New York City', 'lat': 40.7128, 'lon': -74.0060, 'publications': 3},
    {'city': 'Paris', 'lat': 48.8566, 'lon': 2.3522, 'publications': 1},
    {'city': 'Philadelphia', 'lat': 39.9526, 'lon': -75.1652, 'publications': 9},
    {'city': 'Pittsburgh', 'lat': 40.4406, 'lon': -79.9959, 'publications': 4},
    {'city': 'Porto', 'lat': 41.1579, 'lon': -8.6291, 'publications': 1},
    {'city': 'Porto Alegre', 'lat': -30.0346, 'lon': -51.2177, 'publications': 1},
    {'city': 'Potsdam', 'lat': 52.3906, 'lon': 13.0645, 'publications': 1},
    {'city': 'Princeton', 'lat': 40.3573, 'lon': -74.6672, 'publications': 1},
    {'city': 'Providence', 'lat': 41.8240, 'lon': -71.4128, 'publications': 1},
    {'city': 'Ramat Gan', 'lat': 32.0684, 'lon': 34.8248, 'publications': 1},
    {'city': 'Saarbrücken', 'lat': 49.2402, 'lon': 6.9969, 'publications': 4},
    {'city': 'San Diego', 'lat': 32.7157, 'lon': -117.1611, 'publications': 1},
    {'city': 'San Francisco', 'lat': 37.7749, 'lon': -122.4194, 'publications': 2},
    {'city': 'Santa Barbara', 'lat': 34.4208, 'lon': -119.6982, 'publications': 2},
    {'city': 'Seattle', 'lat': 47.6062, 'lon': -122.3321, 'publications': 17},
    {'city': 'Shanghai', 'lat': 31.2304, 'lon': 121.4737, 'publications': 2},
    {'city': 'Singapore', 'lat': 1.3521, 'lon': 103.8198, 'publications': 2},
    {'city': 'Stanford', 'lat': 37.4275, 'lon': -122.1697, 'publications': 8},
    {'city': 'Stuttgart', 'lat': 48.7758, 'lon': 9.1829, 'publications': 2},
    {'city': 'Sunnyvale', 'lat': 37.3688, 'lon': -122.0363, 'publications': 1},
    {'city': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'publications': 1},
    {'city': 'Tel Aviv', 'lat': 32.0853, 'lon': 34.7818, 'publications': 1},
    {'city': 'Tempe', 'lat': 33.4255, 'lon': -111.9400, 'publications': 2},
    {'city': 'Tokyo', 'lat': 35.6895, 'lon': 139.6917, 'publications': 3},
    {'city': 'Verona', 'lat': 45.4384, 'lon': 10.9916, 'publications': 1},
    {'city': 'Vienna', 'lat': 48.2082, 'lon': 16.3738, 'publications': 1},
    {'city': 'Waltham', 'lat': 42.3765, 'lon': -71.2356, 'publications': 2},
    {'city': 'Yokohama', 'lat': 35.4437, 'lon': 139.6380, 'publications': 1},
    {'city': 'Yorktown Heights', 'lat': 41.2943, 'lon': -73.8375, 'publications': 3}
]

# Create a base map
m = folium.Map(location=[40.6331, 37.2363], zoom_start=5)  # Centered on Turkey

# Function to calculate circle radius based on publication count (adjust scaling factor as needed)
def get_radius(publications):
    return publications * 0.5  # Scale publication count to a suitable radius

for city in city_data:
    # Create circle marker with radius proportional to publications
    folium.CircleMarker(
        location=[city['lat'], city['lon']],
        radius=get_radius(city['publications']),
        color='red',
        fill_color='red',
        fill_opacity=0.4,
        tooltip=f"{city['city']}: {city['publications']} publications"
    ).add_to(m)

# Save the map as HTML
filename = 'map'
m.save(filename + '.html')

import time

# Save the map as HTML
filename = 'map'
m.save(filename + '.html')

# Use Selenium to open the HTML file and take a screenshot
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ensure the browser runs in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Set up the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.set_window_size(1200, 800)  # Set the window size to a suitable size

# Open the HTML file
driver.get('file://' + filename + '.html')

# Give it some time to load (increase wait time if necessary)
time.sleep(10)  # Wait for the map to load completely

# Take a screenshot and save it
driver.save_screenshot(filename + '.png')

# Close the browser
driver.quit()

print(f"Map saved as image: {filename}.png")
