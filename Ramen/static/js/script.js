function getRandomRamen() {
    fetch('/random_ramen')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('random-ramen-result').innerText = data.error;
            } else {
                document.getElementById('random-ramen-result').innerText = 
                    `店名: ${data.name}, 城市: ${data.city}, 地址: ${data.address || 'N/A'}, 營業時間: ${data.hours || 'N/A'}, 價格範圍: ${data.price_range || 'N/A'}`;
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

