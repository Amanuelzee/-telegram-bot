<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "finotehiwot";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// SQL to fetch users
$sql = "SELECT id, full_name, phone_number, telegram_username, bank_transaction_number, status, chat_id FROM users";
$result = $conn->query($sql);

// Check if query was successful
if ($result === false) {
    // If query fails, display error
    die("Error: " . $conn->error);
}

// Fetch data
$users = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $users[] = $row;
    }
}

// Function to send Telegram message
function sendTelegramMessage($telegramId, $message) {
    $telegramToken = '7695126763:AAHiG9FJ0t8SQXBGrcYlvqaaFtT_P_7aLBc';  // Your bot token
    $url = "https://api.telegram.org/bot$telegramToken/sendMessage?chat_id=$telegramId&text=" . urlencode($message);

    // Using file_get_contents to send the request
    $response = file_get_contents($url);
    if ($response === FALSE) {
        die('Error sending Telegram message');
    }
}

// Function to assign registration number and car number
function assignRegistrationAndCarNumber($userCount) {
    $carCapacity = 62;
    $carCount = 12;
    $carNumber = floor($userCount / $carCapacity) + 1;
    $seatNumber = $userCount % $carCapacity;

    if ($carNumber > $carCount) {
        return null; // No available cars
    }

    $registrationNumber = "FH" . str_pad($userCount, 4, '0', STR_PAD_LEFT) . "/4";
    return ['registration_number' => $registrationNumber, 'car_number' => $carNumber, 'seat_number' => $seatNumber + 1];
}

// Handle user status update or delete action
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['approve'])) {
        $userId = $_POST['user_id'];
        $status = 'approved';

        // Update user status
        $updateQuery = "UPDATE users SET status='$status' WHERE id='$userId'";
        $conn->query($updateQuery);

        // Send Telegram notification if approved
        if ($status == 'approved') {
            // Fetch the user's telegram_id and full name
            $user = $conn->query("SELECT chat_id, full_name FROM users WHERE id='$userId'")->fetch_assoc();
            $telegramId = $user['chat_id'];  // This should be numeric

            // Assign registration number and car number
            $registrationData = assignRegistrationAndCarNumber(count($users));
            if ($registrationData) {
                // Generate the message
                $message = "ሰላም! " . $user['full_name'] . " ስለተመዘገቡ እናመሰግናለን። ምዝገባዎ በቀን " . date('y-m-d') . " ተቀባይነ አግኝቷል። " . $registrationData['registration_number'] ."ይህ የእስዎ የምዝገባ ቁጥር ነው። ለጉዞ በሚመጡበት ጊዜ ይህንን የምዝገባ ቁጥር ይዘው መገኝት ይጠብቅብዎታል። እናመሰግናለን!";
                // Send the message to the user's chat_id (telegram_id)
                sendTelegramMessage($telegramId, $message);
            }
            $conn->query("UPDATE users SET registry_number = '{$registrationData['registration_number']}' WHERE id = '$userId'");

        }
    } elseif (isset($_POST['deny'])) {
        $userId = $_POST['user_id'];
        $status = 'denied';

        // Update user status
        $updateQuery = "UPDATE users SET status='$status' WHERE id='$userId'";
        $conn->query($updateQuery);
    } elseif (isset($_POST['delete'])) {
        $userId = $_POST['user_id'];

        // Delete user
        $deleteQuery = "DELETE FROM users WHERE id='$userId'";
        $conn->query($deleteQuery);
    }
}

// Fetch updated data after status change or delete action
$result = $conn->query("SELECT id, full_name, phone_number, telegram_username, bank_transaction_number, status FROM users");
if ($result === false) {
    // If query fails, display error
    die("Error: " . $conn->error);
}
$users = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $users[] = $row;
    }
}
$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5">
    <title>ፍኖተ ሕይወት </title>
    <link rel="stylesheet" href="styles.css">
    <script>
        // Function to filter table rows
        function filterTable() {
            const input = document.getElementById("searchInput").value.toLowerCase();
            const rows = document.querySelectorAll(".user-row");
            rows.forEach(row => {
                const fullName = row.querySelector(".user-name").textContent.toLowerCase();
                const phoneNumber = row.querySelector(".user-phone").textContent.toLowerCase();
                const transactionNumber = row.querySelector(".user-transaction").textContent.toLowerCase();
                row.style.display = (fullName.includes(input) || phoneNumber.includes(input) || transactionNumber.includes(input)) ? "" : "none";
            });
        }

        // Confirm action for buttons
        function confirmAction(action) {
            return confirm(`Are you sure you want to ${action} this user?`);
        }
    </script>
    <style>
        /* General Styles */
body {
    font-family: 'Roboto', Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f9f9f9;
    color: #333;
}

/* Container */
.container {
    max-width: 1200px;
    margin: 20px auto;
    padding: 20px;
    background: #ffffff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

/* Title */
h1 {
    font-size: 1.8rem;
    text-align: center;
    margin-bottom: 20px;
    color: #333;
    font-weight: 600;
}

/* Search Container */
.search-container {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 20px;
}

#searchInput {
    width: 100%;
    max-width: 400px;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    font-size: 1rem;
    outline: none;
    transition: all 0.3s ease;
}

#searchInput:focus {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.4);
}

/* Print Button */
.print-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

.print-container .btn {
    text-decoration: none;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    font-size: 1rem;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
    text-align: center;
}

.print-container .btn:hover {
    background-color: #0056b3;
}

/* Table Styles */
.users-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.users-table thead {
    background-color: #007bff;
    color: #fff;
}

.users-table th, 
.users-table td {
    padding: 10px 15px;
    text-align: left;
    border: 1px solid #ddd;
}

.users-table th {
    font-size: 1rem;
    font-weight: 600;
}

.users-table tbody tr:nth-child(even) {
    background-color: #f2f2f2;
}

.users-table tbody tr:hover {
    background-color: #f1f7ff;
}
/* General Button Styles */
.btn {
    padding: 8px 15px;
    font-size: 0.9rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

/* Approve Button */
.btn.approve {
    background-color: #28a745;
    color: #fff;
}

.btn.approve:hover {
    background-color: #218838;
}

/* Delete Button */
.btn.delete {
    background-color: #dc3545;
    color: #fff;
}

.btn.delete:hover {
    background-color: #c82333;
}

        </style>
</head>
<body>
    <div class="container">
        <h1>Manage Registered Users</h1>

        <!-- Search Input -->
        <div class="search-container">
            <input
                type="text"
                id="searchInput"
                placeholder="Search by name, phone, or transaction number..."
                onkeyup="filterTable()"
            />
        </div>

        <!-- Print Button -->
        <div class="print-container">
            <a href="print.php" target="_blank" class="btn print">Print</a>
        </div>

        <!-- Users Table -->
        <table class="users-table">
            <thead>
                <tr>
                    <th>Full Name</th>
                    <th>Phone Number</th>
                    <th>Telegram Username</th>
                    <th>Status</th>
                    <th>transaction number</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($users as $user): ?>
                    <tr class="user-row">
                        <td class="user-name"><?php echo htmlspecialchars($user['full_name']); ?></td>
                        <td class="user-phone"><?php echo htmlspecialchars($user['phone_number']); ?></td>
                        <td><?php echo htmlspecialchars($user['telegram_username']); ?></td>
                        <td><?php echo ucfirst($user['status']); ?></td>
                        <td class="user-transaction"><?php echo htmlspecialchars($user['bank_transaction_number']); ?></td>
                        <td>
                            <?php if ($user['status'] == 'pending'): ?>
                                <form method="POST" style="display:inline;">
                                    <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                                    <button type="submit" name="approve" class="btn approve" onclick="return confirmAction('approve');">Approve</button>
                                    <button type="submit" name="deny" class="btn deny" onclick="return confirmAction('deny');">Deny</button>
                                </form>
                            <?php endif; ?>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                                <button type="submit" name="delete" class="btn delete" onclick="return confirmAction('delete');">Delete</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</body>
</html>
