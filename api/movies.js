import admin from 'firebase-admin';
import { firestore } from './admin';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      // 從 Firestore 獲取電影資料
      const moviesSnapshot = await firestore.collection('movies').get();
      
      const movies = [];
      moviesSnapshot.forEach(doc => {
        movies.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return res.status(200).json({ success: true, movies });
    } catch (error) {
      console.error('獲取電影資料錯誤:', error);
      return res.status(500).json({ success: false, error: '獲取電影資料失敗' });
    }
  } else if (req.method === 'POST') {
    // 需要管理員權限
    try {
      const { title, director, year, poster } = req.body;
      
      // 添加電影到 Firestore
      const movieRef = await firestore.collection('movies').add({
        title,
        director,
        year,
        poster,
        createdAt: admin.firestore.FieldValue.serverTimestamp()
      });
      
      return res.status(200).json({ 
        success: true, 
        message: '電影添加成功',
        id: movieRef.id
      });
    } catch (error) {
      console.error('添加電影錯誤:', error);
      return res.status(500).json({ success: false, error: '添加電影失敗' });
    }
  }
  
  return res.status(405).json({ error: '不支持的請求方法' });
} 