document.querySelectorAll('.explore-option').forEach(btn => {
  btn.addEventListener('click', async () => {
    const option = btn.dataset.option;
    document.querySelector('#explore-content').innerHTML = `<div class="loader"></div>`;
    
    try {
      const response = await fetch(`/explore/${option}`);
      const data = await response.json();
      console.log("Fetched data:", data);

      if (option === "apod") {
        document.querySelector('#explore-content').innerHTML = `
          <h2>${data.title}</h2>
          <img src="${data.url}" alt="${data.title}" />
          <p>${data.explanation}</p>
        `;
      } else if (option === "mars") {
        const photo = data.photos?.[0];
        if (photo) {
          document.querySelector('#explore-content').innerHTML = `
            <h2>Mars Rover Photo</h2>
            <img src="${photo.img_src}" alt="Mars" />
            <p>Rover: ${photo.rover.name}</p>
          `;
        } else {
          document.querySelector('#explore-content').innerHTML = `<p>No Mars photos found.</p>`;
        }
      } else if (option === "earth") {
        document.querySelector('#explore-content').innerHTML = `
          <h2>Earth Imagery</h2>
          <img src="${data.image}" alt="Earth" />
          <p>Coordinates: ${data.lat}, ${data.lon}</p>
        `;
      } else if (option === "iss") {
        document.querySelector('#explore-content').innerHTML = `
          <h2>ISS Current Location</h2>
          <p>Latitude: ${data.latitude}</p>
          <p>Longitude: ${data.longitude}</p>
        `;
      }
    } catch (err) {
      document.querySelector('#explore-content').innerHTML = `<p>Could not load data.</p>`;
    }
  });
});
