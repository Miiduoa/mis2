import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyA74yCIdADHUNyeWAIrPg5jDLd7vHYdMIY",
  authDomain: "project-7332910669653362321.firebaseapp.com",
  projectId: "project-7332910669653362321",
  storageBucket: "project-7332910669653362321.firebasestorage.app",
  messagingSenderId: "510920038201",
  appId: "1:510920038201:web:f7396cad3ff1c407defae8",
  measurementId: "G-SLTJQRT9QD"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app); 