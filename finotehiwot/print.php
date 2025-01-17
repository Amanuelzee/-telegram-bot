<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "finotehiwot";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch users
$sql = "SELECT full_name, phone_number, bank_transaction_number,registry_number FROM users WHERE status = 'approved'";
$result = $conn->query($sql);
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
    <title>Print Users</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
        .logo { text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="logo">
        <img src="assets/img/2_logo.png" alt="Logo" height="80">
    </div>
    <h1>አቃቂ መንበረ ሕይወት መድኃኔዓለም ፍኖተ ብርሃን ሰ/ት/ቤት<br>የፍኖተ ሕይወት ተጓዞች መመዝገቢያ ቅጽ</h1>
    <table>
        <thead>
            <tr>
                <th>Full Name</th>
                <th>Phone Number</th>
                <th>Bank Transaction Number</th>
                <th>registraion number</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($users as $user): ?>
                <tr>
                    <td><?php echo htmlspecialchars($user['full_name']); ?></td>
                    <td><?php echo htmlspecialchars($user['phone_number']); ?></td>
                    <td><?php echo htmlspecialchars($user['bank_transaction_number']); ?></td>
                    <td><?php echo htmlspecialchars($user['registry_number']); ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
    <script>
        // Automatically trigger print dialog
        window.onload = () => window.print();
    </script>
</body>
</html>
