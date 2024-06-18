function getRandomRamen() {
    const city = document.getElementById('city-select').value;
    fetch('/random_ramen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('random-ramen-result').innerText = data.error;
        } else {
            document.getElementById('random-ramen-result').innerText = 
                `店名: ${data.name}, 城市: ${data.city}`;
        }
    });
}

function getCurrentTime() {
    fetch('/current_time')
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-time-result').innerText = data.current_time;
        });
}

function startRamenGame(){
    window.location.href = "/ramen_game";
}
