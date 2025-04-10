import admin from 'firebase-admin';
import { auth, firestore } from './admin';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: '只允許 POST 請求' });
  }

  try {
    const { name, email, password } = req.body;
    
    // 使用 Firebase Auth 創建使用者
    const userRecord = await auth.createUser({
      email,
      password,
      displayName: name,
    });
    
    // 在 Firestore 中存儲附加資訊
    await firestore.collection('users').doc(userRecord.uid).set({
      name,
      email,
      role: 'user',
      createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    return res.status(200).json({ 
      success: true, 
      message: '註冊成功',
      uid: userRecord.uid
    });
  } catch (error) {
    console.error('註冊處理錯誤:', error);
    return res.status(400).json({ 
      success: false, 
      error: error.message || '註冊失敗' 
    });
  }
} 