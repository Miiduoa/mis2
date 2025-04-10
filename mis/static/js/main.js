// 頁面載入完成後執行
document.addEventListener('DOMContentLoaded', function() {
    console.log('頁面已載入，靜態資源測試成功！');
    
    // 檢查是否存在歡迎訊息元素
    const welcomeMessage = document.getElementById('welcomeMessage');
    if (welcomeMessage) {
        console.log('找到歡迎訊息元素');
        
        // 添加一些互動效果
        welcomeMessage.addEventListener('mouseover', function() {
            this.style.color = '#0d6efd';
        });
        
        welcomeMessage.addEventListener('mouseout', function() {
            this.style.color = '';
        });
    }
    
    // 添加當前時間顯示
    const timeDisplay = document.createElement('div');
    timeDisplay.id = 'timeDisplay';
    timeDisplay.style.position = 'fixed';
    timeDisplay.style.bottom = '10px';
    timeDisplay.style.right = '10px';
    timeDisplay.style.background = 'rgba(0,0,0,0.7)';
    timeDisplay.style.color = 'white';
    timeDisplay.style.padding = '5px 10px';
    timeDisplay.style.borderRadius = '5px';
    timeDisplay.style.fontSize = '12px';
    document.body.appendChild(timeDisplay);
    
    // 更新時間函數
    function updateTime() {
        const now = new Date();
        timeDisplay.textContent = now.toLocaleString('zh-TW');
    }
    
    // 初始更新與定時更新
    updateTime();
    setInterval(updateTime, 1000);
}); 