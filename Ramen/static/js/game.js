const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 遊戲參數
const bowlWidth = 100;
const bowlHeight = 50;
const bowl = {
    x: canvas.width / 2 - bowlWidth / 2,
    y: canvas.height - bowlHeight - 10,
    width: bowlWidth,
    height: bowlHeight,
    speed: 5,
    moveLeft: false,
    moveRight: false
};

const ingredients = [];
const ingredientTypes = ['🍜', '🥚', '🍥', '🥬'];
const ingredientSize = 30;
const ingredientSpeed = 2;
let score = 0;
let missedCount = 0; // 錯過的食材數量
const maxMissed = 5; // 最多錯過5個食材

let gameOver = false; // 遊戲結束標誌

// 監聽鍵盤事件
document.addEventListener('mousemove', (event) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    bowl.x = mouseX - bowl.width / 2;
});

// 創建食材
function createIngredient() {
    if (!gameOver) {
        const x = Math.random() * (canvas.width - ingredientSize);
        ingredients.push({
            x: x,
            y: 0,
            type: ingredientTypes[Math.floor(Math.random() * ingredientTypes.length)]
        });
    }
}

// 更新遊戲狀態
function update() {
    if (!gameOver) {
        // 更新食材位置
        for (let i = 0; i < ingredients.length; i++) {
            ingredients[i].y += ingredientSpeed;

            // 檢查食材是否被接住
            if (ingredients[i].y + ingredientSize > bowl.y && 
                ingredients[i].x + ingredientSize > bowl.x && 
                ingredients[i].x < bowl.x + bowl.width) {
                ingredients.splice(i, 1);
                score += 10;
                i--;
            } else if (ingredients[i].y > canvas.height) {
                // 移除掉出屏幕的食材並增加錯過數量
                ingredients.splice(i, 1);
                missedCount++;
                i--;
                
                // 檢查是否達到最大錯過數量
                if (missedCount >= maxMissed) {
                    gameOver = true;
                }
            }
        }
    }
}

// 繪製遊戲畫面
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 碗
    ctx.fillStyle = 'brown';
    ctx.fillRect(bowl.x, bowl.y, bowl.width, bowl.height);

    // 食材
    for (let ingredient of ingredients) {
        ctx.font = `${ingredientSize}px Arial`;
        ctx.fillText(ingredient.type, ingredient.x, ingredient.y);
    }

    // 分數
    ctx.font = '20px Arial';
    ctx.fillText(`分數: ${score}`, 10, 20);
    ctx.fillText(`錯過: ${missedCount}`, 10, 50);

    // 如果遊戲結束，顯示 "遊戲結束" 訊息
    if (gameOver) {
        ctx.font = '40px Arial';
        ctx.fillText('遊戲結束', canvas.width / 2 - 100, canvas.height / 2);
    }
}

// 遊戲主循環
function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

// 每秒創建食材
setInterval(createIngredient, 1000);

// 開始遊戲循環
gameLoop();


function returnToHomepage(){
    window.location.href = "/";
}