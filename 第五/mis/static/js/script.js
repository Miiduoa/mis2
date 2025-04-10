// 頁面載入完成時執行
document.addEventListener('DOMContentLoaded', function() {
    console.log('MIS系統已載入');
    
    // 啟用 Bootstrap 提示工具（Tooltips）
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 啟用 Bootstrap 彈出框（Popovers）
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // 為表單添加驗證事件
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // 添加返回頂部按鈕功能
    if (document.getElementById('back-to-top')) {
        const backToTopButton = document.getElementById('back-to-top');
        
        // 監聽滾動事件
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) { // 滾動超過300px時顯示按鈕
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        // 點擊返回頂部
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // 添加選項卡切換功能
    const tabElements = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabElements.forEach(tabEl => {
        tabEl.addEventListener('shown.bs.tab', event => {
            console.log(`切換到分頁：${event.target.id}`);
        });
    });
    
    // 添加警示框關閉功能
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 150);
            });
        }
    });
    
    // 為動態元素添加事件（如課程列表中的按鈕）
    const detailButtons = document.querySelectorAll('.btn-outline-primary');
    detailButtons.forEach(btn => {
        btn.addEventListener('click', function(event) {
            const courseRow = this.closest('tr');
            const courseName = courseRow.querySelector('td:nth-child(2)').textContent;
            alert(`您點擊了課程：${courseName} 的詳情按鈕`);
        });
    });
    
    const enrollButtons = document.querySelectorAll('.btn-outline-success');
    enrollButtons.forEach(btn => {
        btn.addEventListener('click', function(event) {
            const courseRow = this.closest('tr');
            const courseName = courseRow.querySelector('td:nth-child(2)').textContent;
            const teacher = courseRow.querySelector('td:nth-child(3)').textContent;
            
            if (confirm(`確定要選修 ${teacher} 的 ${courseName} 課程嗎？`)) {
                alert(`您已成功選修 ${courseName} 課程！`);
                // 這裡可以添加AJAX請求來處理選課功能
            }
        });
    });
}); 