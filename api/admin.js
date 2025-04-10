import admin from 'firebase-admin';

if (!admin.apps.length) {
  try {
    const serviceAccount = process.env.FIREBASE_SERVICE_ACCOUNT
      ? JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT)
      : {
          // 用於本地開發的備用值，生產中應使用環境變數
          "type": "service_account",
          "project_id": "project-7332910669653362321"
          // 不要在代碼中包含真實的私鑰
        };
    
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });
    console.log("Firebase Admin 初始化成功");
  } catch (error) {
    console.error("Firebase Admin 初始化失敗:", error);
  }
}

export const firestore = admin.firestore();
export const auth = admin.auth(); 