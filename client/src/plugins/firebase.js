import * as firebase from 'firebase'
// import "firebase/database";

// firebase init - add your own config here
const firebaseConfig = {
        apiKey: "AIzaSyAr-xDgcEBJxaCIQgyN5CXGHC2NWnbXW54",
        authDomain: "polarice-95e3e.firebaseapp.com",
        databaseURL: "https://polarice-95e3e-default-rtdb.firebaseio.com",
        projectId: "polarice-95e3e",
        storageBucket: "polarice-95e3e.appspot.com",
        messagingSenderId: "1088055969732",
        appId: "1:1088055969732:web:37c08c0cedebacffc28691"
};
firebase.initializeApp(firebaseConfig)
const database = firebase.database();

export default database;