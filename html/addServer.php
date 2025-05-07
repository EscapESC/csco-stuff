<?php

$data = json_decode(file_get_contents('php://input'), true);

if (isset($data['serverAddress'])) {
    $file = 'addServer.txt';

    // Validate the input using a regex for IP:Port format
    if (preg_match('/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/', $data['serverAddress'], $matches)) {
        $ip = $matches[1];
        $port = (int)$matches[2];

        // Ensure the IP is valid
        if (filter_var($ip, FILTER_VALIDATE_IP) && $port >= 1024 && $port <= 65535) {
            // Open file in append mode and write the validated server address
            $handle = fopen($file, 'a');
            if ($handle) {
                if (fwrite($handle, $data['serverAddress'] . "\n") !== false) {
                    fclose($handle);
                    echo json_encode(['message' => 'Server address written to file successfully!']);
                } else {
                    echo json_encode(['message' => 'Failed to write to file.']);
                }
            } else {
                echo json_encode(['message' => 'Failed to open file.']);
            }
        } else {
            echo json_encode(['message' => 'Invalid IP or port range.']);
        }
    } else {
        echo json_encode(['message' => 'Invalid server address format. Expected format: IP:Port']);
    }
} else {
    echo json_encode(['message' => 'No server address provided.']);
}
?>

