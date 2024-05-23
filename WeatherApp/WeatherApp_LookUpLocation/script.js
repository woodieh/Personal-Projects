const apiKey = 'f8990c0b608db98efa87ba39847fe012';
const weatherApiUrl = 'https://api.openweathermap.org/data/2.5/weather?lat=';
const geoApiUrl = "http://api.openweathermap.org/geo/1.0/direct?q=";

const locationInput = document.getElementById('locationInput');
const searchButton = document.getElementById('searchButton');
const locationElement = document.getElementById('location');
const temperatureElement = document.getElementById('temperature');
const descriptionElement = document.getElementById('description');

searchButton.addEventListener('click', () => {
    let location = locationInput.value;
    location = location.replace(" ", "+");
    // find lat and long given city name
    if (location) {
        fetchLocation(location);
    }
});

function fetchWeather(lat, lon) {
    const url = `${weatherApiUrl}${lat}&lon=${lon}&appid=${apiKey}&units=imperial`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            locationElement.textContent = data.name;
            temperatureElement.textContent = `${Math.round(data.main.temp)}°F`;
            descriptionElement.textContent = data.weather[0].description;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
}

function fetchLocation(location) {
  const url = `${geoApiUrl}${location}&limit=1&appid=${apiKey}`;
  console.log(url);
  fetch(url)
      .then(response => response.json())
      .then(data => {
          locationElement.textContent = data.name;
          fetchWeather(data[0].lat, data[0].lon);
      })
      .catch(error => {
          console.error('Error fetching location data:', error);
      });
}