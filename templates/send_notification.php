<?php
function sendNotification(){
	$url = "https://fcm.googleapis.com/fcm/send";

	$fields = array(
		"to"=>$_REQUEST['token'],
		"notification"=>array(
			"body"=>$_REQUEST['message'],
			"title"=>$_REQUEST['title'],
			"icon"=>$_REQUEST['icon'],
			"click_action"=>"https://google.com"
		)
	);

	$headers=array(
		'Authorization: key=AAAATU0EZtE:APA91bEzkNMDAqlVFuEtQ0nMu1rZc4bM2yWjzjPktyeBVPywZpMNkbIXg0FBJj2alSONHZGllHzSXYRwSUdFN93jfbSRk4MkWHq-mCX9h2DTEy5RU_6kAeZ8I8ChLf59dP3K0MITzQvJ',
		'Content_Type:application/json',
	);

	$ch=curl_init();
	curl_setopt($ch, option:CURLOPT_URL,$url);
	curl_setopt($ch, option:CURLOPT_POST,value:true);
	curl_setopt($ch, option:CURLOPT_HTTPHEADER,$headers);
	curl_setopt($ch, option:CURLOPT_RETURNTRANSFER,value:true);
	curl_setopt($ch, option:CURLOPT_POSTFIELDS,json_encode($fields));
	$result=curl_exec($ch);
	print_r($result);
	curl_close($ch);
}
sendNotification();
?>	