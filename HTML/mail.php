<?php

$method = $_SERVER['REQUEST_METHOD'];

// Initialize message variable
$message = '';

//Script Foreach
$c = true;
if ( $method === 'POST' ) {

	$project_name = isset($_POST["project_name"]) ? htmlspecialchars(trim($_POST["project_name"])) : '';
	$admin_email  = isset($_POST["admin_email"]) ? filter_var(trim($_POST["admin_email"]), FILTER_SANITIZE_EMAIL) : '';
	$form_subject = isset($_POST["form_subject"]) ? htmlspecialchars(trim($_POST["form_subject"])) : '';
	$user_email = '';

	foreach ( $_POST as $key => $value ) {
		if ( $value != "" && $key != "project_name" && $key != "admin_email" && $key != "form_subject" ) {
			// Capture user email for Reply-To
			if ( $key === "E-mail" || $key === "Email" || $key === "email" ) {
				$user_email = filter_var(trim($value), FILTER_SANITIZE_EMAIL);
			}
			
			$message .= "
			" . ( ($c = !$c) ? '<tr>':'<tr style="background-color: #f8f8f8;">' ) . "
				<td style='padding: 10px; border: #e9e9e9 1px solid;'><b>".htmlspecialchars($key)."</b></td>
				<td style='padding: 10px; border: #e9e9e9 1px solid;'>".htmlspecialchars($value)."</td>
			</tr>
			";
		}
	}
} else if ( $method === 'GET' ) {

	$project_name = isset($_GET["project_name"]) ? htmlspecialchars(trim($_GET["project_name"])) : '';
	$admin_email  = isset($_GET["admin_email"]) ? filter_var(trim($_GET["admin_email"]), FILTER_SANITIZE_EMAIL) : '';
	$form_subject = isset($_GET["form_subject"]) ? htmlspecialchars(trim($_GET["form_subject"])) : '';
	$user_email = '';

	foreach ( $_GET as $key => $value ) {
		if ( $value != "" && $key != "project_name" && $key != "admin_email" && $key != "form_subject" ) {
			// Capture user email for Reply-To
			if ( $key === "E-mail" || $key === "Email" || $key === "email" ) {
				$user_email = filter_var(trim($value), FILTER_SANITIZE_EMAIL);
			}
			
			$message .= "
			" . ( ($c = !$c) ? '<tr>':'<tr style="background-color: #f8f8f8;">' ) . "
				<td style='padding: 10px; border: #e9e9e9 1px solid;'><b>".htmlspecialchars($key)."</b></td>
				<td style='padding: 10px; border: #e9e9e9 1px solid;'>".htmlspecialchars($value)."</td>
			</tr>
			";
		}
	}
}

// Validate email addresses
if ( !filter_var($admin_email, FILTER_VALIDATE_EMAIL) ) {
	http_response_code(400);
	die('Invalid admin email');
}

// Build message table
$message = "<table style='width: 100%;'>$message</table>";

function adopt($text) {
	return '=?UTF-8?B?'.Base64_encode($text).'?=';
}

// Set Reply-To to user's email if available, otherwise use admin email
$reply_to = !empty($user_email) && filter_var($user_email, FILTER_VALIDATE_EMAIL) ? $user_email : $admin_email;

$headers = "MIME-Version: 1.0" . PHP_EOL .
"Content-Type: text/html; charset=utf-8" . PHP_EOL .
'From: '.adopt($project_name).' <'.$admin_email.'>' . PHP_EOL .
'Reply-To: '.$reply_to.'' . PHP_EOL;

// Send email
if ( mail($admin_email, adopt($form_subject), $message, $headers) ) {
	http_response_code(200);
	echo 'success';
} else {
	http_response_code(500);
	echo 'error';
}
