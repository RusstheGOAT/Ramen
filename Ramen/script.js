function getRandomRamen() {
    fetch('/random_ramen')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('random-ramen-result').innerText = data.error;
            } else {
                document.getElementById('random-ramen-result').innerText = 
                    `店名: ${data.name}, 地址: ${data.address}, 營業時間: ${data.hours}, 價格範圍: ${data.price_range}`;
            }
        });
}
