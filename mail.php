<?php
/*
 * Portfolio contact form handler.
 * The recipient is fixed here on purpose: never read it from the form,
 * or anyone could use this script to send email to any address.
 */
const RECIPIENT    = 'sanjulathilan12321@gmail.com';
const SITE_NAME    = 'Sanjula Thilan Portfolio';
const SENDER       = 'noreply@thilan.novalinkinnovations.com';
const MAX_NAME     = 100;
const MAX_MESSAGE  = 5000;
const MIN_SECONDS  = 3;   // reject forms submitted faster than a human could type

error_reporting(E_ALL);
ini_set('display_errors', 0);
header('Content-Type: text/plain; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
	http_response_code(405);
	exit('Method not allowed.');
}

function field($key) {
	return isset($_POST[$key]) ? trim((string) $_POST[$key]) : '';
}
function one_line($s) {
	// strip anything that could break out of an email header
	return trim(preg_replace('/[\r\n\t]+/', ' ', $s));
}

// Spam trap: a hidden field real visitors never fill in.
if (field('website') !== '') {
	echo 'success';   // pretend it worked so bots don't retry
	exit;
}
// Timing check: the form sets this when the page loads.
$started = (int) field('form_started');
if ($started > 0 && (time() - (int) floor($started / 1000)) < MIN_SECONDS) {
	echo 'success';
	exit;
}

$name    = one_line(field('Name'));
$email   = one_line(field('E-mail'));
$message = field('Message');

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
	http_response_code(400);
	exit('error: Please fill in your name, a valid email and a message.');
}
if (mb_strlen($name) > MAX_NAME || mb_strlen($message) > MAX_MESSAGE) {
	http_response_code(400);
	exit('error: Your message is too long.');
}

$h = function ($s) { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); };

$body = "<html><head><meta charset='utf-8'></head>"
	. "<body style='font-family:Arial,sans-serif;line-height:1.6;color:#333'>"
	. "<h2 style='color:#2c3e50'>New message from your portfolio</h2>"
	. "<p><b>Name:</b> " . $h($name) . "<br><b>Email:</b> " . $h($email) . "</p>"
	. "<p style='white-space:pre-wrap'>" . $h($message) . "</p>"
	. "</body></html>";

$subject = 'New contact form message - ' . mb_substr($name, 0, 60);

// Headers as an array so PHP writes the line endings itself. A hand-built "\r\n" string
// gets mangled by Hostinger's sendmail, which breaks the From header and Gmail drops the message.
// The sender is fixed to this domain (covered by its SPF record), whatever hostname the visitor used.
$headers = [
	'MIME-Version' => '1.0',
	'Content-Type' => 'text/html; charset=UTF-8',
	'From'         => SITE_NAME . ' <' . SENDER . '>',
	'Reply-To'     => $email,
	'X-Mailer'     => 'PHP/' . phpversion(),
];

if (mail(RECIPIENT, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers)) {
	echo 'success';
} else {
	error_log('Contact form: mail() failed');
	http_response_code(500);
	echo 'error: Failed to send.';
}
