<?php
// Enable error reporting for debugging (disable in production if needed)
error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't display errors, but log them

header('Content-Type: text/plain; charset=utf-8');

$method = $_SERVER['REQUEST_METHOD'];

// Initialize message variable
$message = '';
$user_email = '';
$user_name = '';

// Only accept POST requests
if ( $method !== 'POST' ) {
	http_response_code(405);
	die('Method not allowed. Use POST.');
}

// Get and sanitize hidden form fields
$project_name = isset($_POST["project_name"]) ? htmlspecialchars(trim($_POST["project_name"])) : 'Portfolio Contact Form';
$admin_email  = isset($_POST["admin_email"]) ? filter_var(trim($_POST["admin_email"]), FILTER_SANITIZE_EMAIL) : '';
$form_subject = isset($_POST["form_subject"]) ? htmlspecialchars(trim($_POST["form_subject"])) : 'New Contact Form Message';

// Validate admin email
if ( empty($admin_email) || !filter_var($admin_email, FILTER_VALIDATE_EMAIL) ) {
	http_response_code(400);
	die('error: Invalid admin email configuration');
}

// Process form fields
$c = true;
foreach ( $_POST as $key => $value ) {
	if ( $value != "" && $key != "project_name" && $key != "admin_email" && $key != "form_subject" ) {
		// Capture user email for Reply-To
		if ( $key === "E-mail" || $key === "Email" || $key === "email" ) {
			$user_email = filter_var(trim($value), FILTER_SANITIZE_EMAIL);
		}
		
		// Capture user name
		if ( $key === "Name" || $key === "name" ) {
			$user_name = htmlspecialchars(trim($value));
		}
		
		$message .= "
		" . ( ($c = !$c) ? '<tr>':'<tr style="background-color: #f8f8f8;">' ) . "
			<td style='padding: 10px; border: #e9e9e9 1px solid;'><b>".htmlspecialchars($key)."</b></td>
			<td style='padding: 10px; border: #e9e9e9 1px solid;'>".htmlspecialchars($value)."</td>
		</tr>
		";
	}
}

// Check if we have a message
if ( empty($message) ) {
	http_response_code(400);
	die('error: No form data received');
}

// Build HTML email body
$email_body = "
<html>
<head>
	<meta charset='utf-8'>
	<title>Contact Form Message</title>
</head>
<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
	<h2 style='color: #2c3e50;'>New Contact Form Message</h2>
	<p>You have received a new message from your portfolio contact form.</p>
	<table style='width: 100%; border-collapse: collapse; margin-top: 20px;'>
		$message
	</table>
	<hr style='margin: 20px 0; border: none; border-top: 1px solid #ddd;'>
	<p style='color: #666; font-size: 12px;'>This email was sent from your portfolio contact form.</p>
</body>
</html>
";

// Email subject
$email_subject = $form_subject . ($user_name ? ' - ' . $user_name : '');

// Set Reply-To to user's email if available
$reply_to = !empty($user_email) && filter_var($user_email, FILTER_VALIDATE_EMAIL) ? $user_email : $admin_email;

// Email headers for better deliverability
$headers = "MIME-Version: 1.0" . PHP_EOL;
$headers .= "Content-Type: text/html; charset=UTF-8" . PHP_EOL;
$headers .= "From: " . $project_name . " <noreply@" . (isset($_SERVER['HTTP_HOST']) ? $_SERVER['HTTP_HOST'] : 'localhost') . ">" . PHP_EOL;
$headers .= "Reply-To: " . $reply_to . PHP_EOL;
$headers .= "X-Mailer: PHP/" . phpversion() . PHP_EOL;

// Send email
$mail_sent = @mail($admin_email, $email_subject, $email_body, $headers);

if ( $mail_sent ) {
	http_response_code(200);
	echo 'success';
} else {
	// Log error if mail fails
	error_log("Mail sending failed. To: $admin_email, Subject: $email_subject");
	http_response_code(500);
	echo 'error: Failed to send email. Please check server configuration.';
}
?>
