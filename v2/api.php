<?php
// Create connection
$mysqli = new mysqli("db501482795.db.1and1.com","dbo501482795","mtolive5","db501482795");

/* check connection */
if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$results = array();

$query = "SELECT * FROM logs ORDER BY date DESC LIMIT 48";

if ($result = $mysqli->query($query)) {

  /* fetch associative array */
  while($row = $result->fetch_assoc())
  {
     $results[] = array(
        'id' => $row['id'],
        'date' => $row['date'],
        'num_inserted' => $row['num_inserted'],
        'num_found' => $row['num_found'],
        'num_errors' => $row['num_error'],
     );
  }
  /* free result set */
  $result->free();
}


$json = json_encode($results);
printf("%s",$json);


/* close connection */
$mysqli->close();

?> 