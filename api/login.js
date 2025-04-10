import { auth } from './admin';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: '只允許 POST 請求' });
  }

  try {
    const { email, password } = req.body;
    
    // 使用 Firebase Auth 驗證使用者
    const userRecord = await auth.getUserByEmail(email)
      .catch(error => {
        console.error('查詢使用者失敗:', error);
        throw new Error('使用者不存在或密碼錯誤');
      });
    
    // 注意: Admin SDK 無法直接驗證密碼
    // 這只是示範，實際上您應該使用客戶端 SDK 進行身份驗證
    // 然後在伺服器端驗證 ID 令牌
    
    // 創建自定義令牌
    const token = await auth.createCustomToken(userRecord.uid);
    
    return res.status(200).json({ 
      success: true, 
      token,
      user: {
        uid: userRecord.uid,
        email: userRecord.email,
        displayName: userRecord.displayName
      }
    });
  } catch (error) {
    console.error('登入處理錯誤:', error);
    return res.status(401).json({ 
      success: false, 
      error: error.message || '登入失敗' 
    });
  }
} 