<?php
// 取得當前時間
$current_time = date('Y-m-d H:i:s');
// 定義一個簡單的陣列，存放我的技能
$skills = [
    "前端開發" => ["HTML", "CSS", "JavaScript"],
    "後端技術" => ["Python", "Flask", "PHP"],
    "資料庫" => ["Firebase", "MySQL"]
];
?>
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>關於我 - PHP 版本</title>
    <style>
        body {
            font-family: '微軟正黑體', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #3498db;
            margin-top: 30px;
        }
        img {
            display: block;
            margin: 20px auto;
            border-radius: 50%;
            border: 3px solid #3498db;
        }
        p {
            margin: 10px 0;
        }
        a {
            color: #e74c3c;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #e0e0e0;
        }
        audio, iframe {
            display: block;
            margin: 20px auto;
            width: 80%;
        }
        .current-time {
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            color: #555;
        }
        .skill-category {
            font-weight: bold;
            color: #333;
        }
        .skill-list {
            margin-left: 20px;
            color: #555;
        }
    </style>
</head>
<body>
    <h1>個人簡介</h1>
    <p class="current-time">現在時間：<?php echo $current_time; ?></p>
    
    <!-- 添加頭像圖片 -->
    <img src="images/profile.jpg" alt="個人頭像" width="200">
    
    <h2>基本資料</h2>
    <p>姓名：王小明</p>
    <p>學校：資訊管理學系</p>
    <p>興趣：網頁設計、程式開發</p>
    
    <h2>技能專長</h2>
    <?php foreach($skills as $category => $skillList): ?>
        <p class="skill-category"><?php echo $category; ?>：</p>
        <ul class="skill-list">
            <?php foreach($skillList as $skill): ?>
                <li><?php echo $skill; ?></li>
            <?php endforeach; ?>
        </ul>
    <?php endforeach; ?>
    
    <h2>相關連結</h2>
    <p><a href="https://github.com/" target="_blank">我的 GitHub</a></p>
    <p><a href="https://www.linkedin.com/" target="_blank">LinkedIn 個人檔案</a></p>
    <p><a href="mailto:example@email.com">寄信給我</a></p>
    
    <h2>課程表</h2>
    <table border="1">
        <thead>
            <tr>
                <th>時間</th>
                <th>星期一</th>
                <th>星期二</th>
                <th>星期三</th>
                <th>星期四</th>
                <th>星期五</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>09:00-10:00</td>
                <td>資料結構</td>
                <td>程式設計</td>
                <td>資料庫</td>
                <td>網頁設計</td>
                <td>專題討論</td>
            </tr>
            <tr>
                <td>10:10-11:00</td>
                <td>作業系統</td>
                <td>資訊管理</td>
                <td>演算法</td>
                <td>人工智慧</td>
                <td>資訊安全</td>
            </tr>
            <tr>
                <td>11:10-12:00</td>
                <td>雲端運算</td>
                <td>行動應用</td>
                <td>系統分析</td>
                <td>專題實作</td>
                <td>專題發表</td>
            </tr>
        </tbody>
    </table>
    
    <h2>最愛的音樂</h2>
    <audio controls>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        您的瀏覽器不支援音訊元素
    </audio>
    
    <h2>推薦影片</h2>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    
    <h2 id="messageHeading">給訪客的留言</h2>
    <?php 
    // 根據時間顯示不同的歡迎訊息
    $hour = (int)date('H');
    if ($hour >= 5 && $hour < 12) {
        $greeting = "早安！祝您有美好的一天！";
    } elseif ($hour >= 12 && $hour < 18) {
        $greeting = "午安！希望您有個愉快的下午！";
    } else {
        $greeting = "晚安！感謝您在夜晚拜訪我的網頁！";
    }
    ?>
    <p id="welcomeMessage"><?php echo $greeting; ?></p>
    <p>您的IP位址：<?php echo $_SERVER['REMOTE_ADDR']; ?></p>
    <p>瀏覽器資訊：<?php echo $_SERVER['HTTP_USER_AGENT']; ?></p>
    
    <script>
        // 動態內容互動部分保留
        document.addEventListener('DOMContentLoaded', function() {
            // 為歡迎訊息添加滑鼠事件
            const welcomeMessage = document.getElementById('welcomeMessage');
            welcomeMessage.addEventListener('mouseover', function() {
                this.style.color = '#e74c3c';
                this.style.fontSize = '1.2em';
            });
            welcomeMessage.addEventListener('mouseout', function() {
                this.style.color = 'black';
                this.style.fontSize = '1em';
            });
        });
    </script>
</body>
</html> 