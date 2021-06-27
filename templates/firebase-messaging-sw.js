importScript('https://www.gstatic.com/firebasejs/8.6.7/firebase-app.js');
importScript('https://www.gstatic.com/firebasejs/8.6.7/firebase-messaging.js');

var firebaseConfig = {
	    apiKey: "AIzaSyDgARUKidNoH2Vwrld8NeZwu02pr67msG8",
	    authDomain: "noti1-23f83.firebaseapp.com",
	    projectId: "noti1-23f83",
	    storageBucket: "noti1-23f83.appspot.com",
	    messagingSenderId: "332004615889",
	    appId: "1:332004615889:web:47364dbd2f1a18a64887f0"
  	};

firebase.initializeApp(firebaseConfig);
const messaging=firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
	console.log(payload)
	const notification =JSON.parse(payload);
	const notificationOption={
		body:notification.body,
		icon:notification.icon
	};
	return self.registration.showNotification(payload.notification.title,notificationOption);
});