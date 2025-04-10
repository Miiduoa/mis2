// 建議採用運行時注入配置的方式
// 這裡假設後端提供了一個 API 端點返回配置
async function initializeFirebase() {
  try {
    // 選項 1: 從後端 API 獲取配置
    // const response = await fetch('/api/firebase-config');
    // const firebaseConfig = await response.json();
    
    // 選項 2: 使用環境變數注入的配置
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_PROJECT_ID.appspot.com",
      messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
      appId: "YOUR_APP_ID"
    };
    
    // 初始化 Firebase
    firebase.initializeApp(firebaseConfig);
    window.firebaseInitialized = true;
    console.log("Firebase 初始化成功");
    
    // 獲取 Firebase 服務
    window.auth = firebase.auth();
    window.db = firebase.firestore();
    
    // 如果啟用了 Analytics
    if (firebase.analytics) {
      window.analytics = firebase.analytics();
    }
    
    // 觸發初始化完成事件
    document.dispatchEvent(new CustomEvent('firebaseInitialized'));
    
  } catch (error) {
    console.error("Firebase 初始化失敗:", error);
    window.firebaseInitialized = false;
    document.dispatchEvent(new CustomEvent('firebaseInitializationFailed', { detail: error }));
  }
}

// 當 DOM 內容載入完成後初始化 Firebase
document.addEventListener('DOMContentLoaded', initializeFirebase);

// 如果要使用 Analytics (可選)
const analytics = window.firebaseInitialized && firebase.analytics ? firebase.analytics() : null; 