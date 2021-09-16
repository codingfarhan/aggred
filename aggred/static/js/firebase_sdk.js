// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.0.2/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDa-bMwkHEvVh--oHMbHBV3Sf3TfCRVhw8",
    authDomain: "aggred-a46f3.firebaseapp.com",
    projectId: "aggred-a46f3",
    storageBucket: "aggred-a46f3.appspot.com",
    messagingSenderId: "1068772275258",
    appId: "1:1068772275258:web:7a9ae2794bae5d58ee3103",
    measurementId: "G-LNMC46RKF1",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);